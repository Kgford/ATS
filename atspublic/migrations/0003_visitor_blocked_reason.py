# Generated by Django 3.1.6 on 2021-02-06 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atspublic', '0002_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='blocked_reason',
            field=models.CharField(blank=True, max_length=200, verbose_name='blocked_reason'),
        ),
    ]