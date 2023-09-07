from django.contrib import admin
from .models import studentsModel, Courses, Enquiry

# Register your models here.

admin.site.register(studentsModel)
admin.site.register(Courses)
admin.site.register(Enquiry)
