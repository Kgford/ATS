# Generated by Django 3.1.6 on 2021-02-28 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0020_auto_20210226_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehical',
            old_name='image_file',
            new_name='image',
        ),
    ]
