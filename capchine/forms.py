from django import forms
from django.contrib.auth.models import User
from django_starfield import Stars

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

CHOICES = [('student','Student'),('teacher','Teacher')]

class RegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(label="Select Role", choices=CHOICES, widget=forms.Select(choices=CHOICES))
    password = forms.CharField(label="Password", widget= forms.PasswordInput(attrs={'maxlength':150}))
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')



class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

RATING_CHOICES = [(1,'*'),(2,'**'),(3,'***'),(4,'****'),(5,'*****')]

class RatingForm(forms.Form):
    rating = forms.ChoiceField(label="Rate Student", choices= RATING_CHOICES, widget=forms.Select(choices=RATING_CHOICES))
        
