# Generated by Django 2.1.15 on 2021-01-17 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20210117_1554'),
        ('accounts', '0007_auto_20210117_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='v_inspection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='v_inspection', to='assets.Vehical'),
        ),
    ]