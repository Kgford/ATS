# Generated by Django 2.1.15 on 2021-01-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='shelf',
        ),
        migrations.AddField(
            model_name='location',
            name='type',
            field=models.CharField(default='N/A', max_length=25, null=True, verbose_name='type'),
        ),
    ]