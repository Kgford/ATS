# Generated by Django 3.1.6 on 2021-02-26 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0019_auto_20210223_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehical',
            name='image',
        ),
        migrations.AddField(
            model_name='vehical',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='assets/'),
        ),
    ]