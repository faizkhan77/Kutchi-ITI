# Generated by Django 4.2.4 on 2023-09-13 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_examreports'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsmodel',
            name='joiningtime',
            field=models.TimeField(auto_now_add=True, default='00:00:00'),
            preserve_default=False,
        ),
    ]
