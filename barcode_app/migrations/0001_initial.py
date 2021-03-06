# Generated by Django 3.1.6 on 2021-02-15 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barcodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=50, verbose_name='part_number')),
                ('part_desc', models.CharField(blank=True, max_length=200, verbose_name='part_desc')),
                ('image', models.BinaryField(blank=True, editable=True, null=True)),
                ('created_on', models.DateField(null=True)),
                ('inventory_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory')),
            ],
        ),
    ]
