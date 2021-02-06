# Generated by Django 3.1.6 on 2021-02-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atspublic', '0003_visitor_blocked_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitor',
            old_name='user_ip',
            new_name='visitor_ip',
        ),
        migrations.AlterField(
            model_name='visitor',
            name='client_id',
            field=models.CharField(blank=True, max_length=100, verbose_name='client_id'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, verbose_name='session_id'),
        ),
    ]
