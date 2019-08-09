from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.
ROLE_CHOICES = (
    ('student','Student'),
    ('teacher','Teacher'),
)
class Role(models.Model):
    u = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roly')
    my_role = models.CharField(max_length=50, choices=ROLE_CHOICES, null = True, blank = True)

    def __str__(self):
        return self.u.get_full_name()
    


class Student(models.Model):
    u = models.ForeignKey(User,related_name="stdnt_info",on_delete=models.CASCADE)
    code_count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.u.get_full_name()


class Teacher(models.Model):
    u = models.ForeignKey(User, related_name="tchr_info",on_delete=models.CASCADE)
    search_count = models.IntegerField(blank=True, null = True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.u.get_full_name()


class Search_Code(models.Model):
    u = models.ForeignKey(User, related_name="my_srch_code", on_delete=models.CASCADE)
    code = models.CharField(max_length = 200)
    rating = models.BooleanField(default=False)
    accessed_by = models.ManyToManyField(User, related_name="accessed_codes", blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.u.get_full_name()


class Rating(models.Model):
    u = models.ForeignKey(User, related_name="my_rating", on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, related_name="given_rating", on_delete=models.CASCADE)
    rating = models.IntegerField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.u.get_full_name()
