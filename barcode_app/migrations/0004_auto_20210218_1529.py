# Generated by Django 3.1.6 on 2021-02-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode_app', '0003_remove_barcodes_inventory_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcodes',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='barcodes',
            name='part_desc',
        ),
        migrations.AddField(
            model_name='barcodes',
            name='standard',
            field=models.CharField(blank=True, max_length=50, verbose_name='standard'),
        ),
    ]
