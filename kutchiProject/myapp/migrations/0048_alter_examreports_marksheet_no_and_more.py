# Generated by Django 4.2.4 on 2023-10-06 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0047_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examreports',
            name='marksheet_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='examreports',
            name='percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='examreports',
            name='practical_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='examreports',
            name='theory_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='examreports',
            name='total_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
