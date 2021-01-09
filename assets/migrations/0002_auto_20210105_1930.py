# Generated by Django 2.1.15 on 2021-01-06 00:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='building_fuel',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='building_mantainance',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='building_repair',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='internet',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='internet',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='image_file',
            field=models.CharField(max_length=20, null=True, verbose_name='Image_file'),
        ),
        migrations.AddField(
            model_name='personnel_insurance',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='personnel_overhead',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='power',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='power',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_file',
            field=models.CharField(max_length=20, null=True, verbose_name='Image_file'),
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='prouct_insurance',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='prouct_insurance',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='prouct_shipping',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='prouct_shipping',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='prouct_storage',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='prouct_storage',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehical',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='vehical',
            name='image_file',
            field=models.CharField(max_length=20, null=True, verbose_name='Image_file'),
        ),
        migrations.AddField(
            model_name='vehical',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehicle_fuel',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='vehicle_fuel',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehicle_insurance',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='vehicle_load',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehicle_mantainance',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehicle_oil',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='vehicle_oil',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehicle_repair',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AddField(
            model_name='vehicle_tire',
            name='date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='vehicle_tire',
            name='model',
            field=models.CharField(max_length=50, null=True, verbose_name='model'),
        ),
        migrations.AlterField(
            model_name='building',
            name='address',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building',
            name='city',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building',
            name='state',
            field=models.CharField(max_length=10, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building',
            name='zip_code',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building_fuel',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building_fuel',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='building_mantainance',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building_mantainance',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='building_repair',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='building_repair',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='business_space',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='internet',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='internet',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='personnel_insurance',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='personnel_insurance',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='personnel_overhead',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='personnel_overhead',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='power',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='power',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='prouct_insurance',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='prouct_insurance',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='prouct_shipping',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='prouct_shipping',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='prouct_storage',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='prouct_storage',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehical',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehical',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_fuel',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_fuel',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_insurance',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_insurance',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_load',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_load',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_mantainance',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_mantainance',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_oil',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_oil',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_repair',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_repair',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehicle_tire',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehicle_tire',
            name='type',
            field=models.CharField(max_length=50, null=True, verbose_name='type'),
        ),
    ]