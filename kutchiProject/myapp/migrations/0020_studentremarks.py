# Generated by Django 4.2.4 on 2023-09-05 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_rename_student_exam_date_studentsmodel_exam_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentRemarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark_date', models.DateField()),
                ('remarks', models.CharField(max_length=500)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.studentsmodel')),
            ],
        ),
    ]
