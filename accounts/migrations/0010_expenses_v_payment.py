# Generated by Django 2.1.15 on 2021-01-20 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_auto_20210117_2154'),
        ('accounts', '0009_expenses_v_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='v_payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='v_payment', to='assets.Vehical'),
        ),
    ]