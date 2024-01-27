# Generated by Django 4.2.4 on 2024-01-26 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0056_alter_studentsmodel_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentsmodel",
            name="image",
            field=models.ImageField(
                blank=True,
                default="student_images/default-student.png",
                null=True,
                upload_to="test/",
            ),
        ),
    ]
