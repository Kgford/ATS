# Generated by Django 2.1.15 on 2020-12-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='contact_first',
            field=models.CharField(default='N/A', max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='contact_last',
            field=models.CharField(default='N/A', max_length=100, verbose_name='name'),
        ),
    ]