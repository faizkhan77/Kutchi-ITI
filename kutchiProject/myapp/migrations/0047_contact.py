# Generated by Django 4.2.4 on 2023-09-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0046_alter_services_coursename_alter_services_rollno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('useremail', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
