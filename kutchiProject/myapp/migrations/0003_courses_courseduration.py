# Generated by Django 4.2.4 on 2023-08-29 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_studentsmodel_feespaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='courseduration',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
