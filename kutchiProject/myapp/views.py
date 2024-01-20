from django.shortcuts import render, redirect
from .forms import (
    StudentModelForm,
    CourseModelForm,
    SyllabusDownloadForm,
    RemarksForm,
    EnquiryForm,
    FeesInstallmentForm,
    ExamReportsForm,
    ServiceForm,
    contactForm,
)
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
from django.db.models import Sum
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            pass
            # messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            pass
            # messages.error(request, "Username or password is not correct!")

    context = {"page": page}
    # return render(request, "myapp/login.html", context)
    return render(request, "myapp/TestTemplates/new-login.html", context)


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

    # Number of students to display per page
    students_per_page = 10

    # Get the page number from the request's GET parameters
    page = request.GET.get("page", 1)

    # Create a Paginator object
    paginator = Paginator(studentlist, students_per_page)

    try:
        # Get the specified page
        students = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        students = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page
        students = paginator.page(paginator.num_pages)

    for student in students:
        student.remaining_balance = student.coursefees - student.feespaid

    context = {"students": students}
    return render(request, "myapp/Students_comp.html", context)


# @login_required(login_url="login")
def courseTab(request):
    courses = Courses.objects.all()
    context = {"courses": courses}
    return render(request, "myapp/Courses_comp.html", context)


def contactTab(request):
    contactform = contactForm()

    if request.method == "POST":
        contactform = contactForm(request.POST)
        if contactform.is_valid():
            contactform.save()

            # Sending email logic
            name = contactform.cleaned_data.get("name")
            useremail = contactform.cleaned_data.get("useremail")
            user_message = contactform.cleaned_data.get("message")

            subject = "NEW CONTACT MESSAGE!!"
            from_email = useremail
            message = f"New Contact Message from {name}\n\n"
            message += f"User's Name : {name} \n"
            message += f"User's Email : {useremail} \n\n"
            message += f"Message:- \n{user_message}"
            recipient_mail = ["faizkhan.net7@gmail.com"]

            send_mail(subject, message, from_email, recipient_mail, fail_silently=False)

            return redirect("home")

    context = {"form": contactform}
    return render(request, "myapp/TestTemplates/contacttemp.html", context)


def aboutTab(request):
    return render(request, "myapp/about.html")


def enquiryTab(request):
    studentlist = studentsModel.objects.all()
    enquirylist = Enquiry.objects.all()
    context = {"enquirylist": enquirylist, "students": studentlist}
    return render(request, "myapp/enquiry_comp.html", context)


def rules_and_regulations(request):
    return render(request, "myapp/rules_regulation.html")


def faculties(request):
    return render(request, "myapp/faculties_tab.html")


# ---------------NEED WORK-----------------------------------------------


def feesTab(request):
    students = studentsModel.objects.all()

    for student in students:
        # Calculate the total fees paid by summing up the related FeesInstallment amounts
        total_amount_paid = FeesInstallment.objects.filter(student=student).aggregate(
            total=Sum("amount_paid")
        )["total"]

        # Calculate the balance
        if total_amount_paid is not None:
            student.remaining_balance = student.coursefees - total_amount_paid
        else:
            # Handle the case where there are no payments yet
            student.remaining_balance = student.coursefees

    context = {
        "students": students,
    }
    return render(request, "myapp/FeesTab.html", context)


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
            return redirect("student-register", user_id=student.id)
        else:
            messages.error(request, "An error occured during registration")

    context = {"form": signupform}
    return render(request, "myapp/signup.html", context)


def studentRegisterForm(request, user_id):
    page = "registerstudent"
    user = User.objects.get(id=user_id)

    form = StudentModelForm(initial={"user": user})
    if request.method == "POST":
        form = StudentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-tab")

    context = {"form": form, "page": page}
    return render(request, "myapp/studentRegister.html", context)


def studentDetails(request, pk):
    student = studentsModel.objects.get(id=pk)

    # Retrieve the services requested by the specific student
    services = Services.objects.filter(student=student)

    # Retrieve the exam reports for the specific student
    exam_reports = ExamReports.objects.filter(student=student)

    duration = relativedelta(student.completiondate, student.joiningdate)
    remainingBalance = student.coursefees - student.feespaid
    context = {
        "students": student,
        "duration": duration,
        "remainingBalance": remainingBalance,
        "exam_reports": exam_reports,
        "services": services,
    }
    return render(request, "myapp/student_details.html", context)


def deleteStudent(request, pk):
    page = "deletestudent"
    delstudent = studentsModel.objects.get(id=pk)
    if request.method == "POST":
        if delstudent.user:
            delstudent.user.delete()
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

    # Get the list of PDF files from the 'pdfs' folder
    pdf_folder = os.path.join(settings.BASE_DIR, "pdfs")
    pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith(".pdf")]

    if request.method == "POST":
        courseform = CourseModelForm(request.POST)
        if courseform.is_valid():
            courseform.save()

            # After saving, update the list of PDF files
            pdf_files = [
                file for file in os.listdir(pdf_folder) if file.endswith(".pdf")
            ]

            return redirect("course-tab")

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


def search_students(request):
    query = request.GET.get("query")
    students = studentsModel.objects.filter(
        Q(firstname__icontains=query)
        | Q(rollno__icontains=query)  # Search by firstname (case-insensitive)
        | Q(lastname__icontains=query)
        | Q(  # Search by roll no (case-insensitive)
            id__icontains=query
        )  # Search by id (case-insensitive)
    )
    for student in students:
        student.remaining_balance = student.coursefees - student.feespaid
    course = Courses.objects.filter(Q(coursename__icontains=query))
    context = {"students": students, "course": course}
    return render(request, "myapp/Students_comp.html", context)


def search_courses(request):
    query = request.GET.get("query")
    courses = Courses.objects.filter(
        Q(coursename__icontains=query)
        | Q(courseduration__icontains=query)
        | Q(coursefees__icontains=query)
    )
    context = {"courses": courses}
    return render(request, "myapp/Courses_comp.html", context)


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
            user_message = (
                f"Hey {user_name}\n"
                f"Thank you for visiting us and for downloading our syllabus\n"
                f"for more information contact us or visit us"
            )
            send_mail(
                user_subject,
                user_message,
                "faizkhan.net7@gmail.com",
                [user_email],
                fail_silently=False,
            )

            # send mail to admin

            admin_subject = "New Syllabus Download"
            admin_message = (
                f"Name: {user_name}\n"
                f"Email ID: {user_email}\n"
                f"Mobile Number: {user_details.number}\n"
                f"Downloaded Syllabus: {course.coursename}\n"
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


def examReport(request, pk):
    student = studentsModel.objects.get(id=pk)

    if request.method == "POST":
        examform = ExamReportsForm(request.POST)
        if examform.is_valid():
            # Set the 'student' field before saving the form
            examform.instance.student = student
            examform.save()
            return redirect("studentdetails", pk=pk)
    else:
        examform = ExamReportsForm()

    context = {"form": examform, "student": student}
    return render(request, "myapp/exam_reportform.html", context)


def editExamReport(request, pk):
    # Get the exam report instance to edit
    exam_report = ExamReports.objects.get(id=pk)

    if request.method == "POST":
        examform = ExamReportsForm(request.POST, instance=exam_report)
        if examform.is_valid():
            examform.save()
            return redirect("studentdetails", pk=exam_report.student.id)
    else:
        examform = ExamReportsForm(instance=exam_report)

    context = {"form": examform, "exam_report": exam_report.student}
    return render(request, "myapp/exam_reportform.html", context)


def addenquiry(request):
    form = EnquiryForm()
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enquiry")
    context = {"form": form}
    return render(request, "myapp/enquiryform.html", context)


def add_installment(request, pk):
    student = studentsModel.objects.get(id=pk)

    if request.method == "POST":
        form = FeesInstallmentForm(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data["amount_paid"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]

            # Check if this is the first installment (initial payment)
            if student.feespaid == 0:
                initial_amount = student.initial_payment
                if amount_paid > initial_amount:
                    return render(
                        request,
                        "myapp/add_installment.html",
                        {
                            "form": form,
                            "student": student,
                            "error_message": "Amount paid exceeds initial payment.",
                        },
                    )

                FeesInstallment.objects.create(
                    student=student, date=date, time=time, amount_paid=initial_amount
                )

                student.feespaid += initial_amount
            else:
                # Calculate the remaining balance
                remaining_balance = student.coursefees - student.feespaid

                if amount_paid > remaining_balance:
                    return render(
                        request,
                        "myapp/add_installment.html",
                        {
                            "form": form,
                            "student": student,
                            "error_message": "Amount paid exceeds remaining balance.",
                        },
                    )

                FeesInstallment.objects.create(
                    student=student, date=date, time=time, amount_paid=amount_paid
                )

                student.feespaid += amount_paid

            student.save()
            return redirect("student-tab")

    else:
        form = FeesInstallmentForm()

    context = {"form": form, "student": student}
    return render(request, "myapp/add_installment.html", context)


def payment_history(request, pk):
    student = studentsModel.objects.get(id=pk)
    installment_history = FeesInstallment.objects.filter(student=student)

    # Check if initial payment exists and add it to installment history only if there are no installments yet
    if student.feespaid > 0 and not installment_history.exists():
        initial_installment = FeesInstallment.objects.create(
            student=student,
            date=student.joiningdate,
            time=student.joiningtime,
            amount_paid=student.initial_payment,
        )
        installment_history = [initial_installment] + list(installment_history)

    context = {"installment_history": installment_history, "student": student}
    return render(request, "myapp/payment_history.html", context)


def cancel_admission(request, pk):
    page = "canceladmission"
    student = get_object_or_404(studentsModel, id=pk)

    if request.method == "POST":
        student.admissioncancel = True
        student.save()
        return redirect("studentdetails", pk=pk)
    context = {"student": student, "page": page}
    return render(request, "myapp/delete.html", context)


# def service_request(request):
#     context = {}
#     return render(request, "myapp/services_tab.html", context)


@login_required(login_url="login")
def services_form(request):
    # Get the logged-in student
    if request.user.is_superuser:
        services_form = ServiceForm()
    else:
        # Get the logged-in student
        student = studentsModel.objects.get(user=request.user)
        services_form = ServiceForm()

        if request.method == "POST":
            services_form = ServiceForm(request.POST)
            if services_form.is_valid():
                services_form.save()

                # Get the form data
                student_name = services_form.cleaned_data.get("student_name")
                rollno = services_form.cleaned_data.get("rollno")
                coursename = services_form.cleaned_data.get("coursename")
                phoneno = services_form.cleaned_data.get("phoneno")
                request_details = services_form.cleaned_data.get("request_details")
                request_date = (
                    services_form.instance.request_date
                )  # Assuming you have a request_date field in your model

                # Create the email message
                message = f"Student Name: {student_name}\n"
                message += f"Roll Number: {rollno}\n"
                message += f"Course: {coursename}\n"
                message += f"Phone Number: {phoneno}\n"
                message += f"Request Date: {request_date}\n\n"

                message += "Selected Services:\n"
                checkbox_fields = [
                    "change_batch_time",
                    "course_rejoin",
                    "course_break",
                    "name_correction",
                    "duplicate_id",
                    "reissue_book",
                    "recheck_exampaper",
                    "holiday_leave",
                    "cancel_admission",
                    "extend_batch_time",
                    "course_extend",
                    "fast_track",
                    "extend_installment",
                    "duplicate_certificate",
                    "reissue_hall_ticket",
                    "attendance_chart",
                    "change_faculty",
                    "other_services",
                    "special_batch",
                    "course_duration_extend",
                    "extra_practice",
                    "trust_letter",
                    "certificate_marksheet_bypost",
                    "re_exam",
                    "mobile_num_change",
                    "fine_or_penalty_waivedoff",
                ]

                # Check each checkbox field and add it to the message if selected
                for field_name in checkbox_fields:
                    if services_form.cleaned_data.get(field_name):
                        message += field_name.replace("_", " ").title() + "\n"

                message += f"\nRequest Details: {request_details}\n"

                # Send the email
                subject = "Service Form"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [
                    "faizkhan.net7@gmail.com"
                ]  # Replace with your email address

                send_mail(
                    subject, message, from_email, recipient_list, fail_silently=False
                )

                return redirect("home")
            else:
                print(services_form.errors)

        else:
            if not request.user.is_superuser:
                # Initialize the form with default values for regular users
                services_form = ServiceForm(
                    initial={
                        "student": student,
                        "student_name": f"{student.firstname} {student.lastname}",
                        "rollno": student.rollno,
                        "coursename": student.coursename.coursename,
                        "phoneno": student.phoneno,
                    }
                )

    context = {"form": services_form}
    return render(request, "myapp/services_form.html", context)


# --------------------------------------------------------------------------------


@login_required(login_url="login")
def loggedin_student_details(request):
    studentlist = studentsModel.objects.get(user=request.user)
    duration = relativedelta(studentlist.completiondate, studentlist.joiningdate)
    remainingBalance = studentlist.coursefees - studentlist.feespaid
    # exam_reports = ExamReports.objects.filter(student=mystudent)
    courses = Courses.objects.all()

    context = {
        "students": studentlist,
        "courses": courses,
        "duration": duration,
        "remainingBalance": remainingBalance,
        # "exam_reports": exam_reports,
    }
    return render(request, "myapp/loggedin_student_details.html", context)


# for Testing Only
@login_required(login_url="login")
def print_exam_reports(request):
    # Get the student associated with the currently logged-in user
    user = request.user
    try:
        studentlist = studentsModel.objects.get(user=user)
    except studentsModel.DoesNotExist:
        studentlist = None

    if studentlist:
        exam_reports = ExamReports.objects.filter(student=studentlist)
    else:
        exam_reports = []

    context = {"exam_reports": exam_reports}
    return render(request, "myapp/loggedin_student_Examreport.html", context)


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


@login_required(login_url="login")
def enquiries_inside_enquirytab(request):
    enquirylist = Enquiry.objects.all()
    print(enquirylist)
    context = {"enquirylist": enquirylist}
    return render(request, "myapp/enquiries_inside_enquirytab.html", context)
