# Generated by Django 2.1.15 on 2021-01-17 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_auto_20210117_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehical',
            name='last_update',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vehical',
            name='ownership',
            field=models.CharField(default='N/A', max_length=50, verbose_name='ownership'),
        ),
    ]
