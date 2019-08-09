"""ProjectCappuchino URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import capchine.views as cv
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('',cv.dashboard,name='dashboard'),
	path('student_dashboard/',cv.student_dashboard, name="student_dashboard"),
	path('teacher_dashboard/',cv.teacher_dashboard, name="teacher_dashboard"),
	
	path('search_student/',cv.search_student, name='search_student'),
	path('student_rating/', cv.student_rating, name="student_rating"),
	
	
	path('login/',cv.user_login,name="login"),
	path('logout/',auth_views.LogoutView.as_view() ,{"next_page": "/login"}, name="logout" ),
	path('signup/',cv.user_registration,name="signup"),
	path('edit/',cv.edit, name="edit"),
	re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', cv.activate_account, name='activate'),
    
	
	
	path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
	path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
	path('generate_code/',cv.create_code, name="generate_code"),
	path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
	path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
	
	
	
	
	
	path('admin/', admin.site.urls),
]
