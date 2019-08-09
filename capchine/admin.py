from django.contrib import admin
from .models import Student, Teacher, Search_Code, Rating, Role



# Register your models here.

admin.site.register(Role)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Search_Code)
admin.site.register(Rating)
