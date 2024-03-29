from django.forms import ModelForm, DateInput
from .models import (
    studentsModel,
    Courses,
    SyllabusDownloadRecord,
    StudentRemarks,
    Enquiry,
    FeesInstallment,
    ExamReports,
    Services,
    contact,
)
from django import forms
from django.forms.widgets import ClearableFileInput


class StudentModelForm(ModelForm):
    class Meta:
        model = studentsModel
        fields = "__all__"
        exclude = [
            "completiondate",
            "coursefees",
            "exam_date",
            "exam_given",
            "feespaid",
        ]
        widgets = {
            "image": ClearableFileInput(attrs={"class": "form-control"}),
            "joiningdate": DateInput(attrs={"type": "date"}),
            "status": forms.Select(choices=studentsModel.STATUS_CHOICES),
            "completiondate": DateInput(attrs={"type": "date"}),
        }

    coursename = forms.ModelChoiceField(queryset=Courses.objects.all())


import os


class CourseModelForm(ModelForm):
    # image_folder = "static/images/course-images/"
    file_path = forms.FilePathField(path="pdfs/", required=False)

    # image_files = [
    #     file
    #     for file in os.listdir(image_folder)
    #     if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    # ]

    # image_path = forms.ChoiceField(
    #     choices=[(file, file) for file in image_files], required=False
    # )

    class Meta:
        model = Courses
        fields = "__all__"


class SyllabusDownloadForm(forms.ModelForm):
    class Meta:
        model = SyllabusDownloadRecord
        fields = ["name", "email", "number"]


class RemarksForm(ModelForm):
    class Meta:
        model = StudentRemarks
        fields = ["remarks"]


class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = "__all__"


class FeesInstallmentForm(forms.ModelForm):
    class Meta:
        model = FeesInstallment
        fields = ["date", "time", "amount_paid"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class ExamReportsForm(forms.ModelForm):
    class Meta:
        model = ExamReports
        fields = "__all__"
        exclude = ["student", "coursename"]

    exam_status = forms.BooleanField(
        required=False,  # Checkbox field is not required
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class ServiceForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(ServiceForm, self).__init__(*args, **kwargs)

    #     # Disable the "Student" dropdown field
    #     self.fields['student'].widget.attrs['disabled'] = 'disabled'
    class Meta:
        model = Services
        fields = "__all__"


class contactForm(ModelForm):
    class Meta:
        model = contact
        fields = "__all__"
