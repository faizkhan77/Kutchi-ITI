# Generated by Django 4.2.4 on 2023-09-28 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_services_coursename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='coursename',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='services',
            name='rollno',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='services',
            name='student_name',
            field=models.CharField(max_length=100),
        ),
    ]