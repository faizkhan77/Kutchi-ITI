# Generated by Django 4.2.4 on 2024-02-09 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0075_alter_courses_image_1_alter_courses_image_2_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courses",
            name="image_1",
        ),
        migrations.RemoveField(
            model_name="courses",
            name="image_2",
        ),
        migrations.RemoveField(
            model_name="courses",
            name="image_3",
        ),
        migrations.RemoveField(
            model_name="courses",
            name="image_4",
        ),
    ]