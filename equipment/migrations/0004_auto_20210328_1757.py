# Generated by Django 3.1.6 on 2021-03-28 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_auto_20210306_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='equipment/'),
        ),
    ]
