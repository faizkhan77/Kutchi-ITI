# Generated by Django 4.2.4 on 2023-09-01 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_studentsmodel_student_exam_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentsmodel',
            old_name='student_exam_date',
            new_name='exam_date',
        ),
        migrations.RenameField(
            model_name='studentsmodel',
            old_name='student_exam_given',
            new_name='exam_given',
        ),
    ]
