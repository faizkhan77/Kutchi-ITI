# Generated by Django 4.2.4 on 2024-02-09 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0070_delete_courseimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="image_1",
            field=models.ImageField(
                blank=True,
                default="2.jpg",
                null=True,
                upload_to="images/course-images/",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="image_2",
            field=models.ImageField(
                blank=True,
                default="2.jpg",
                null=True,
                upload_to="images/course-images/",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="image_3",
            field=models.ImageField(
                blank=True,
                default="2.jpg",
                null=True,
                upload_to="images/course-images/",
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="image_4",
            field=models.ImageField(
                blank=True,
                default="2.jpg",
                null=True,
                upload_to="images/course-images/",
            ),
        ),
    ]
