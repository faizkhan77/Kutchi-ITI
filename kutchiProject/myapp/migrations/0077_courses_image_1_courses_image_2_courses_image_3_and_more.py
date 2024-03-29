# Generated by Django 4.2.4 on 2024-02-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0076_remove_courses_image_1_remove_courses_image_2_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="image_1",
            field=models.ImageField(
                blank=True,
                default="default-course-img1.jpg",
                null=True,
                upload_to="course-images/",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="image_2",
            field=models.ImageField(
                blank=True,
                default="default-course-img2.jpg",
                null=True,
                upload_to="course-images/",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="image_3",
            field=models.ImageField(
                blank=True,
                default="default-course-img3.jpg",
                null=True,
                upload_to="course-images/",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="image_4",
            field=models.ImageField(
                blank=True,
                default="default-course-img4.jpg",
                null=True,
                upload_to="course-images/",
            ),
        ),
    ]
