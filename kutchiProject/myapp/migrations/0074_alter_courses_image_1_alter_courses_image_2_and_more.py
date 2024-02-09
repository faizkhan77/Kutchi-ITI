# Generated by Django 4.2.4 on 2024-02-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0073_alter_courses_image_1_alter_courses_image_2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="image_1",
            field=models.ImageField(
                blank=True, default="2.jpg", null=True, upload_to="course-images/"
            ),
        ),
        migrations.AlterField(
            model_name="courses",
            name="image_2",
            field=models.ImageField(
                blank=True, default="2.jpg", null=True, upload_to="course-images/"
            ),
        ),
        migrations.AlterField(
            model_name="courses",
            name="image_3",
            field=models.ImageField(
                blank=True, default="2.jpg", null=True, upload_to="course-images/"
            ),
        ),
        migrations.AlterField(
            model_name="courses",
            name="image_4",
            field=models.ImageField(
                blank=True, default="2.jpg", null=True, upload_to="course-images/"
            ),
        ),
    ]