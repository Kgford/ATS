# Generated by Django 3.1.6 on 2021-02-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210206_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_help_desk',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_help_desk'),
        ),
    ]
