# Generated by Django 4.2.4 on 2023-08-30 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_pdffile_syllabuspdffile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyllabusDownloadRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('number', models.CharField(max_length=20)),
                ('download_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
