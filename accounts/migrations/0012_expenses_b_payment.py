# Generated by Django 2.1.15 on 2021-01-23 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0015_auto_20210123_1422'),
        ('accounts', '0011_auto_20210121_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='b_payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='b_payment', to='assets.Business_Space'),
        ),
    ]
