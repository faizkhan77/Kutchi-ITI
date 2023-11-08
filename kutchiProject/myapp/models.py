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
    # updated = models.DateTimeField(auto_now=True)
    # created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coursename


class Batch(models.Model):
    batch_day = models.CharField(max_length=100, null=True, blank=True)
    batch_time = models.CharField(max_length=100, default="8:30 pm - 10:30 pm")

    def __str__(self):
        return f"{self.batch_day} - {self.batch_time}"


class studentsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    rollno = models.IntegerField(default=0)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    occupation = models.CharField(max_length=200, default="Student")
    phoneno = models.BigIntegerField()
    emailid = models.EmailField()
    address = models.TextField(null=True, blank=True)
    coursename = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)
    joiningdate = models.DateField()
    joiningtime = models.TimeField(auto_now_add=True)
    completiondate = models.DateField()
    extendeddate = models.DateField(null=True, blank=True)
    exam_date = models.DateField(null=True, blank=True)
    exam_given = models.BooleanField(default=False)
    coursefees = models.IntegerField()
    batch_day = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        related_name="students_with_batch_day",
        blank=True,
    )
    batch_time = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        related_name="students_with_batch_time",
    )
    initial_payment = models.IntegerField(default=0)
    feespaid = models.IntegerField(default=0)
    admissioncancel = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.coursename:
            # Autofill coursefees from related Courses
            self.coursefees = self.coursename.coursefees

        if not self.feespaid:
            self.feespaid = self.initial_payment

        if self.joiningdate and self.coursename and self.coursename.courseduration:
            # Calculate completion date by adding course duration (in months)
            self.completiondate = self.joiningdate + relativedelta(
                months=self.coursename.courseduration
            )

        # Always set exam date as 1 day after completion date
        if self.completiondate:
            self.exam_date = self.completiondate + timedelta(days=1)

        if self.exam_date and self.exam_date <= date.today():
            self.exam_given = True
        else:
            self.exam_given = False

        super().save(*args, **kwargs)

    def is_admission_canceled(self):
        return self.admissioncancel

    def __str__(self):
        return self.firstname


class StudentRemarks(models.Model):
    student = models.ForeignKey(studentsModel, on_delete=models.SET_NULL, null=True)
    remark_date = models.DateField()
    remarks = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        # Automatically set the remark_date to the current date if not provided
        if not self.remark_date:
            self.remark_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Remark for {self.student.firstname} on {self.remark_date}"


class contact(models.Model):
    name = models.CharField(max_length=100)
    useremail = models.EmailField()
    message = models.TextField()


class SyllabusDownloadRecord(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    download_time = models.DateTimeField(auto_now_add=True)


class Enquiry(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phoneno = models.BigIntegerField()
    address = models.TextField(null=True, blank=True)
    reference = models.CharField(max_length=50)

    def __str__(self):
        return self.firstname + self.lastname


class FeesInstallment(models.Model):
    student = models.ForeignKey(studentsModel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)


class ExamReports(models.Model):
    student = models.ForeignKey(studentsModel, on_delete=models.CASCADE)
    coursename = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)
    exam_status = models.BooleanField(default=False)  # Use BooleanField for checkbox
    theory_marks = models.DecimalField(max_digits=5, decimal_places=2)
    practical_marks = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    marksheet_no = models.IntegerField()
    hallticket_no = models.IntegerField(default=0)


class Services(models.Model):
    student = models.ForeignKey(
        studentsModel, on_delete=models.SET_NULL, null=True, default=None
    )

    student_name = models.CharField(max_length=100)
    rollno = models.IntegerField()
    coursename = models.CharField(max_length=100)
    phoneno = models.BigIntegerField()
    request_date = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    # Servives
    change_batch_time = models.BooleanField(default=False)
    extend_batch_time = models.BooleanField(default=False)
    special_batch = models.BooleanField(default=False)
    course_rejoin = models.BooleanField(default=False)
    course_extend = models.BooleanField(default=False)
    course_duration_extend = models.BooleanField(default=False)
    course_break = models.BooleanField(default=False)
    fast_track = models.BooleanField(default=False)
    extra_practice = models.BooleanField(default=False)
    name_correction = models.BooleanField(default=False)
    installment_extend = models.BooleanField(default=False)
    trust_letter = models.BooleanField(default=False)
    duplicate_id = models.BooleanField(default=False)
    duplicate_certificate = models.BooleanField(default=False)
    certificate_marksheet_bypost = models.BooleanField(default=False)
    reissue_book = models.BooleanField(default=False)
    reissue_hall_ticket = models.BooleanField(default=False)
    re_exam = models.BooleanField(default=False)
    recheck_exampaper = models.BooleanField(default=False)
    attendance_chart = models.BooleanField(default=False)
    mobile_num_change = models.BooleanField(default=False)
    holiday_leave = models.BooleanField(default=False)
    change_faculty = models.BooleanField(default=False)
    fine_or_penalty_waivedoff = models.BooleanField(default=False)
    cancel_admission = models.BooleanField(default=False)
    other_services = models.BooleanField(default=False)
    # request details
    request_details = models.TextField(null=True, blank=True, default=None)
    # agreement
    policy_agreement = models.BooleanField(default=False)

    def __str__(self):
        return f"Service Request for {self.student}"
