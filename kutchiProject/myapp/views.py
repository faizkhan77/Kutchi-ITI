from django.shortcuts import render, redirect
from .forms import StudentModelForm, CourseModelForm, SyllabusDownloadForm, RemarksForm
from .models import studentsModel, Courses, SyllabusDownloadRecord, StudentRemarks
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.urls import reverse
from django.template.loader import render_to_string
import os
from django.conf import settings


# Create your views here.

# -----------------------------AUTHENTICATION------------------------------------------


def loginPage(request):
    page = "login"
    # so user cant go to login page from the link, if they do, redirect them to home
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            # messages.error(request, "User exist")
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is not correct!")

    context = {"page": page}
    return render(request, "myapp/login.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def is_superuser(user):
    return user.is_superuser


# -------------------------------------------------------------------------------


@login_required(login_url="login")
def index(request):
    studentlist = studentsModel.objects.all()
    duration = None
    remainingBalance = None
    if not request.user.is_superuser:
        studentlist = studentsModel.objects.get(user=request.user)
        duration = relativedelta(studentlist.completiondate, studentlist.joiningdate)
        remainingBalance = studentlist.coursefees - studentlist.feespaid
    courses = Courses.objects.all()

    context = {
        "students": studentlist,
        "courses": courses,
        "duration": duration,
        "remainingBalance": remainingBalance,
    }
    return render(request, "myapp/home.html", context)


# ---------------------------TABS-----------------------------------------------


@login_required(login_url="login")
@user_passes_test(is_superuser, login_url="home")
def studentTab(request):
    studentlist = studentsModel.objects.all()
    for student in studentlist:
        student.remaining_balance = student.coursefees - student.feespaid
    context = {"students": studentlist}
    return render(request, "myapp/Students_comp.html", context)


@login_required(login_url="login")
def courseTab(request):
    courses = Courses.objects.all()
    context = {"courses": courses}
    return render(request, "myapp/Courses_comp.html", context)


def contactTab(request):
    return render(request, "myapp/contact.html")


def aboutTab(request):
    return render(request, "myapp/about.html")


# ------------------------FUNCTIONS-------------------------------------------


def studentSignup(request):
    signupform = UserCreationForm()
    if request.method == "POST":
        signupform = UserCreationForm(request.POST)
        if signupform.is_valid():
            student = signupform.save(commit=False)
            student.username = student.username.lower()
            student.save()
            # login(request, student)
            return redirect("student-register")
        else:
            messages.error(request, "An error occured during registration")

    context = {"form": signupform}
    return render(request, "myapp/signup.html", context)


def studentRegisterForm(request):
    page = "registerstudent"
    form = StudentModelForm()
    if request.method == "POST":
        form = StudentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-tab")

    context = {"form": form, "page": page}
    return render(request, "myapp/studentRegister.html", context)


def studentDetails(request, pk):
    student = studentsModel.objects.get(id=pk)
    duration = relativedelta(student.completiondate, student.joiningdate)
    remainingBalance = student.coursefees - student.feespaid
    context = {
        "students": student,
        "duration": duration,
        "remainingBalance": remainingBalance,
    }
    return render(request, "myapp/student_details.html", context)


def deleteStudent(request, pk):
    page = "deletestudent"
    delstudent = studentsModel.objects.get(id=pk)
    if request.method == "POST":
        delstudent.delete()
        return redirect("student-tab")
    context = {"student": delstudent, "page": page}
    return render(request, "myapp/delete.html", context)


def editStudent(request, pk):
    studentedit = studentsModel.objects.get(id=pk)
    editform = StudentModelForm(instance=studentedit)
    if request.method == "POST":
        editform = StudentModelForm(request.POST, instance=studentedit)
        if editform.is_valid():
            editform.save()
            return redirect("student-tab")
        else:
            print(editform.errors)
    context = {"form": editform, "studentedit": studentedit}
    return render(request, "myapp/studentRegister.html", context)


def addCourse(request):
    page = "addcourse"
    courseform = CourseModelForm()

    if request.method == "POST":
        courseform = CourseModelForm(request.POST)
        if courseform.is_valid():
            courseform.save()
            return redirect("course-tab")

    pdf_folder = os.path.join(settings.BASE_DIR, "pdfs")
    pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith(".pdf")]

    context = {"form": courseform, "pdf_files": pdf_files, "page": page}
    return render(request, "myapp/courseform.html", context)


def courseDetails(request, pk):
    course = Courses.objects.get(id=pk)
    context = {"obj": course}
    print(course.file_path)
    return render(request, "myapp/coursedetails.html", context)


def courseDelete(request, pk):
    page = "deletecourse"
    delcourse = Courses.objects.get(id=pk)
    if request.method == "POST":
        delcourse.delete()
        return redirect("course-tab")
    context = {"student": delcourse, "page": page}
    return render(request, "myapp/delete.html", context)


def courseUpdate(request, pk):
    page = "editcourse"
    updatecourse = Courses.objects.get(id=pk)
    updateform = CourseModelForm(instance=updatecourse)
    if request.method == "POST":
        updateform = CourseModelForm(request.POST, instance=updatecourse)
        if updateform.is_valid():
            updateform.save()
            return redirect("coursedetails", pk=updatecourse.id)
    context = {"form": updateform, "page": page}
    return render(request, "myapp/courseform.html", context)

    # def upload_pdf(request):
    #     form = UploadPDFForm()  # Create an instance of the form

    #     if request.method == "POST":
    #         form = UploadPDFForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             pdf_file = form.cleaned_data["pdf_file"]
    #             title = pdf_file.name
    #             pdf_path = (
    #                 f"pdfs/{title}"  # Store PDFs in 'pdfs' folder within your media root
    #             )

    #             with open(pdf_path, "wb") as destination:
    #                 for chunk in pdf_file.chunks():
    #                     destination.write(chunk)

    #             SyllabusPDFFile.objects.create(title=title, file_path=pdf_path)
    # return redirect("upload_success")  # Redirect to a success page

    # context = {"form": form}
    # return render(request, "myapp/upload_pdf.html", context)


# Form syllabus download
def DownloadSyllabus(request, pk):
    course = get_object_or_404(Courses, id=pk)
    email_sent = False

    if request.method == "POST":
        form = SyllabusDownloadForm(request.POST, request.FILES)
        if form.is_valid():
            user_name = form.cleaned_data["name"]
            user_details = form.save()

            # send mail to user
            user_email = user_details.email
            user_subject = "Kutchi ITI"
            user_message = f"Thank you for visiting us and for downloading our syllabus"
            send_mail(
                user_subject,
                user_message,
                "faizkhan.net7@gmail.com",
                [user_email],
                fail_silently=False,
            )

            admin_subject = "New Syllabus Download"
            admin_message = (
                f"Name: {user_name}\n"
                f"Email ID: {user_email}\n"
                f"Mobile Number: {user_details.number}\n"
                f"Download time and date : {user_details.download_time}"
            )
            send_mail(
                admin_subject,
                admin_message,
                "faizkhan.net7@gmail.com",
                ["faizkhan.net7@gmail.com"],
                fail_silently=False,
            )
            email_sent = True

            if course.file_path:
                pdf_path = course.file_path

                # Use the FileResponse to serve the PDF file as a response
                try:
                    response = FileResponse(
                        open(pdf_path, "rb"), content_type="application/pdf"
                    )
                    response[
                        "Content-Disposition"
                    ] = f'attachment; filename="{course.coursename}_syllabus.pdf"'
                    return response
                except FileNotFoundError:
                    # Handle if the file is not found
                    pass
            # Redirect or show an error message if the file path is not available
            return redirect("home")
    else:
        form = SyllabusDownloadForm()
    context = {"form": form, "email_sent": email_sent}
    return render(request, "myapp/downloadsyllabus.html", context)


# for direct syllabus download
def download_pdf(request, pk):
    course = get_object_or_404(Courses, pk=pk)

    if course.file_path:
        pdf_path = course.file_path

        # Use the FileResponse to serve the PDF file as a response
        try:
            response = FileResponse(
                open(pdf_path, "rb"), content_type="application/pdf"
            )
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{course.coursename}.pdf"'
            return response
        except FileNotFoundError:
            # Handle if the file is not found
            pass

    # Redirect or show an error message if the file path is not available
    return redirect("home")


def StudentRemark(request, pk):
    students = studentsModel.objects.get(id=pk)
    form = RemarksForm()
    if request.method == "POST":
        form = RemarksForm(request.POST)
        if form.is_valid():
            remarks = form.cleaned_data["remarks"]
            StudentRemarks.objects.create(student=students, remarks=remarks)
            return redirect("studentdetails", pk=pk)
        else:
            form = RemarksForm()
    context = {"form": form, "students": students}
    return render(request, "myapp/remarksForm.html", context)


# --------------------------------------------------------------------------------


@login_required(login_url="login")
def loggedin_student_details(request):
    # studentlist = studentsModel.objects.all()
    # duration = None
    # remainingBalance = None
    # if not request.user.is_superuser:
    studentlist = studentsModel.objects.get(user=request.user)
    duration = relativedelta(studentlist.completiondate, studentlist.joiningdate)
    remainingBalance = studentlist.coursefees - studentlist.feespaid
    courses = Courses.objects.all()

    context = {
        "students": studentlist,
        "courses": courses,
        "duration": duration,
        "remainingBalance": remainingBalance,
    }
    return render(request, "myapp/loggedin_student_details.html", context)


@login_required(login_url="login")
def studentlist_inside_studenttab(request):
    studentlist = studentsModel.objects.all()
    for student in studentlist:
        student.remaining_balance = student.coursefees - student.feespaid
    context = {"students": studentlist}
    return render(request, "myapp/studentlist_inside_studenttab.html", context)


@login_required(login_url="login")
def courselist_inside_coursetab(request):
    courses = Courses.objects.all()
    context = {"courses": courses}
    return render(request, "myapp/courselist_inside_coursetab.html", context)


def sidebarmenu(request):
    context = {}
    return render(request, "myapp/sidebar_comp.html", context)
