# Generated by Django 4.2.4 on 2023-09-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_feesinstallment'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsmodel',
            name='initial_payment',
            field=models.IntegerField(default=0),
        ),
    ]
