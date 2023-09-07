from django.urls import path
from myapp import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("", views.index, name="home"),
    path("studentregister/", views.studentRegisterForm, name="student-register"),
    path("studentsignup/", views.studentSignup, name="studentsignup"),
    path("studentdetails/<int:pk>/", views.studentDetails, name="studentdetails"),
    path("deletestudent/<int:pk>/", views.deleteStudent, name="delete"),
    path("editstudent/<int:pk>/", views.editStudent, name="edit"),
    path("addcourse/", views.addCourse, name="addcourse"),
    path("coursedetails/<int:pk>/", views.courseDetails, name="coursedetails"),
    path("deletecourse/<int:pk>/", views.courseDelete, name="delete-course"),
    path("updatecourse/<int:pk>/", views.courseUpdate, name="update-course"),
    path("student-tab/", views.studentTab, name="student-tab"),
    path("course-tab/", views.courseTab, name="course-tab"),
    path("contact-tab/", views.contactTab, name="contact"),
    path("about-tab/", views.aboutTab, name="about"),
    path("enquiry-tab/", views.enquiryTab, name="enquiry"),
    path("sidebar/", views.sidebarmenu, name="sidebar"),
    path(
        "loggedin-students-details/",
        views.loggedin_student_details,
        name="loggedin-students-details",
    ),
    path(
        "studentlist_inside_studenttab/",
        views.studentlist_inside_studenttab,
        name="studentlist_inside_studenttab",
    ),
    path(
        "courselist_inside_coursetab/",
        views.courselist_inside_coursetab,
        name="courselist_inside_coursetab",
    ),
    path(
        "enquiries_inside_enquirytab/",
        views.enquiries_inside_enquirytab,
        name="enquiries_inside_enquirytab",
    ),
    path("syllabus/<int:pk>/", views.DownloadSyllabus, name="syllabusdownload"),
    path("download-pdf/<int:pk>/", views.download_pdf, name="download-pdf"),
    path("remarks/<int:pk>/", views.StudentRemark, name="remarks"),
    path("addenquiry", views.addenquiry, name="addenquiry"),
]
