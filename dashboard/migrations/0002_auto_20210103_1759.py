# Generated by Django 2.1.15 on 2021-01-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income_report',
            name='income_total',
            field=models.FloatField(null=True, verbose_name='income_total'),
        ),
        migrations.AlterField(
            model_name='income_report',
            name='month_str',
            field=models.CharField(max_length=100, verbose_name='month_str'),
        ),
    ]
