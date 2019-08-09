from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistrationForm, EditForm, RatingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from .models import Student, Teacher, Search_Code, Rating, Role
import random, string
import datetime
from django.utils import timezone



# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return redirect('/login')



def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request, "Authenticated Successfully.")
                    return redirect("/")

                    return 
                else:
                    messages.error(request, "Disabled Account.")
                    return redirect('/login')
            else:
                messages.error(request, "Invalid login.")
                return redirect('/login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html',{'form':form})


def user_registration(request):
    if request.method=='POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            u_role = request.POST['role']
            print(u_role)
            if u_role =='student':
                Student.objects.create(u = new_user)
                Role.objects.create(u = new_user, my_role = 'student')
            else:
                Teacher.objects.create(u = new_user)
                Role.objects.create(u=new_user, my_role='teacher')


            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('registration/activate_account.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'account/register_done.html',{'new_user':new_user})
        else:
            user_form = RegistrationForm()
            return render(request,'account/register.html',{'user_form':user_form})
    user_form = RegistrationForm()
    return render(request, 'account/register.html',{'user_form':user_form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')




@login_required
def admin_dashboard(request):
    cd = None
    role = 'Admin'
    return render(request,'account/dashboard.html',{'role':role,'cd':cd})

@login_required
def student_dashboard(request):
    cd = None
    rating = False
    role = 'Student'
    if len(Search_Code.objects.filter(u__id=request.user.id))>0:
        sc = Search_Code.objects.filter(u__id = request.user.id).order_by('-created')[0]
        rating = sc.rating
        #sc = Search_Code.objects.get(u__id = request.user.id)
        now = timezone.now()
        diff = now - sc.created
        seconds = diff.seconds
        seconds = seconds/60/60
        print("Seconds:", seconds)
        if seconds > 10.0:
            cd = 'Code has been expired.'
        else:
            cd = sc.code
    std = Student.objects.get(u__id=request.user.id)
    if std.code_count == None:
        code_count = 0
    else:
        code_count = std.code_count
    accessed_by = sc.accessed_by.all()
    ratings = Rating.objects.filter(u = request.user, active=True).order_by('-created')[:5]
    return render(request,'account/dashboard.html',{'role':role,'code_count':code_count,'cd':cd,
    'rating':rating,'accessed_by':accessed_by, 'ratings':ratings, 'sc':sc,
})


@login_required
def teacher_dashboard(request):
    cd = None
    rating = False
    role = 'Teacher'
    tchr = Teacher.objects.filter(u__id=request.user.id)
    if tchr != []:
        print('Teacher:',tchr)
        if tchr[0].search_count == None:
            search_count = 0 
        else:
            search_count = tchr[0].search_count
    accessed_profiles = request.user.accessed_codes.all()
    rating_profiles = request.user.given_rating.filter(active=True)


    return render(request,'account/dashboard.html',{'role':role,'search_count':search_count,'cd':cd,'rating':rating,
    'accessed_profiles':accessed_profiles, 'rating_profiles':rating_profiles}) 


@login_required
def dashboard(request):
    cd = None
    if request.user.is_superuser:
        return redirect('admin/')
    
    elif request.user.roly.my_role =='student':
        return redirect('student_dashboard/')
    else:
        return redirect('teacher_dashboard/')

    
        



@login_required
def edit(request):
    if request.method=='POST':
        user_form = EditForm(instance = request.user, data = request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,"Changes saved successfully.")
            return redirect('/edit')
        else:
            messages.error(request,"Please enter correct values.")
            user_form = EditForm(instance = request.user)
    user_form = EditForm(instance = request.user)
    return render(request, 'account/edit.html',{'user_form':user_form})


@login_required
def create_code(request):
    random_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
    r = False
    if request.GET.get('rating') =='Yes':
        r = True
    srch_code = Search_Code.objects.create(u= request.user, code = random_code, rating = r)
    messages.success(request,"Search code generated.")

    return redirect('/')



@login_required
def search_student(request):
    if request.user.roly.my_role =='teacher':
        s = request.GET.get('searching')
        print(request.GET)
        
        sc = get_object_or_404(Search_Code, code=s)
        
        now = timezone.now()
        diff = now - sc.created
        seconds = diff.seconds
        seconds = seconds/60/60
        print("Seconds:", seconds)
        if seconds > 10.0:
            messages.error(request,'Code has been expired')
            return redirect('teacher_dashboard')
        

        

        #sc = Search_Code.objects.get(code=s)
        print('Code User: ',sc.u)
        std = sc.u
        t = Teacher.objects.get(u = request.user)
        s_count = t.search_count
        if s_count ==None:
            s_count = 0
        s_count +=1
        t.search_count = s_count
        t.save()

        student = Student.objects.get(u = sc.u)
        ca_count = student.code_count
        print("CA count", ca_count)
        if ca_count == None:
            ca_count = 0
        ca_count +=1
        student.code_count = ca_count
        student.save()
        sc.accessed_by.add(request.user)

        ratings = Rating.objects.filter(u = sc.u, active=True).order_by('-created')[:5]
        
    return render(request,'account/student_profile.html',{'sc':sc,'std':std,'ratings':ratings})



@login_required
def student_rating(request):
    if request.user.roly.my_role == 'teacher':
        r = request.GET.get('ratings')
        print(r)
        custId = request.GET.get('custId')
        print('CustId: ',custId)
        s = get_object_or_404(Search_Code, code = custId)
        Rating.objects.create(u = s.u, teacher = request.user, rating = r)
        return redirect('teacher_dashboard')

