# Generated by Django 2.1.15 on 2021-01-17 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_auto_20210117_1232'),
        ('accounts', '0004_auto_20210115_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='insurance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical'),
        ),
    ]
