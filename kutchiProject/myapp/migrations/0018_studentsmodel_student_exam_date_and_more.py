# Generated by Django 4.2.4 on 2023-09-01 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_remove_studentsmodel_exam_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsmodel',
            name='student_exam_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentsmodel',
            name='student_exam_given',
            field=models.BooleanField(default=False),
        ),
    ]
