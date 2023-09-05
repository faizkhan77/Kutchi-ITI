from django.forms import ModelForm, DateInput
from .models import studentsModel, Courses, SyllabusDownloadRecord
from django import forms


class StudentModelForm(ModelForm):
    class Meta:
        model = studentsModel
        fields = "__all__"
        exclude = ["completiondate", "coursefees", "exam_date", "exam_given"]
        widgets = {
            "joiningdate": DateInput(attrs={"type": "date"}),
            "completiondate": DateInput(attrs={"type": "date"}),
        }


class CourseModelForm(ModelForm):
    file_path = forms.FilePathField(path="pdfs/", required=False)

    class Meta:
        model = Courses
        fields = "__all__"


class SyllabusDownloadForm(forms.ModelForm):
    class Meta:
        model = SyllabusDownloadRecord
        fields = ["name", "email", "number"]