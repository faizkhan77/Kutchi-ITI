from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date

# Create your models here.


class Courses(models.Model):
    coursename = models.CharField(max_length=100)
    coursedetails = models.TextField(null=True, blank=True)
    courseduration = models.PositiveIntegerField(default=0)
    coursefees = models.IntegerField()
    file_path = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.coursename


class studentsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phoneno = models.BigIntegerField()
    emailid = models.EmailField()
    address = models.TextField(null=True, blank=True)
    coursename = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)
    joiningdate = models.DateField()
    completiondate = models.DateField()
    exam_date = models.DateField(null=True, blank=True)
    exam_given = models.BooleanField(default=False)
    coursefees = models.IntegerField()
    feespaid = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.coursename:
            # Autofill coursefees from related Courses
            self.coursefees = self.coursename.coursefees

        if self.joiningdate and self.coursename and self.coursename.courseduration:
            # Calculate completion date by adding course duration (in months)
            self.completiondate = self.joiningdate + relativedelta(
                months=self.coursename.coursedurationmk
            )

        # Always set exam date as 1 day after completion date
        if self.completiondate:
            self.exam_date = self.completiondate + timedelta(days=1)

        if self.exam_date and self.exam_date <= date.today():
            self.exam_given = True
        else:
            self.exam_given = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.firstname


class StudentRemarks(models.Model):
    student = models.ForeignKey(studentsModel, on_delete=models.SET_NULL, null=True)
    remark_date = models.DateField()
    remarks = models.CharField(max_length=500)


class SyllabusDownloadRecord(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    download_time = models.DateTimeField(auto_now_add=True)
