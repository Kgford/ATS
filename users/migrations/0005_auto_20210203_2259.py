# Generated by Django 2.1.15 on 2021-02-04 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210203_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_developer',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_developer'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_help_desk',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_help_deskp'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_manager',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_manager'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_marketing',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_marketing'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_sales',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_sales'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_security',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_security'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_social_media',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_social_media'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='alerts_web_monitor',
            field=models.BooleanField(default=False, null=True, verbose_name='alerts_web_monitor'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'User'), (2, 'Supervisor'), (3, 'Manager'), (4, 'Owner'), (5, 'Engineer'), (6, 'Technician'), (7, 'Contractor'), (8, 'Developer'), (9, 'Marketing'), (10, 'Sales'), (11, 'Social_Media'), (12, 'Web_Monitor'), (13, 'Help_Desk'), (14, 'Security')], null=True),
        ),
    ]
