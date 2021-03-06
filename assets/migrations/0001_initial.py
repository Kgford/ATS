# Generated by Django 2.1.15 on 2021-01-03 22:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='name')),
                ('state', models.CharField(max_length=10, verbose_name='name')),
                ('zip_code', models.CharField(max_length=50, verbose_name='name')),
                ('address', models.CharField(max_length=50, verbose_name='name')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
            ],
        ),
        migrations.CreateModel(
            name='Building_Fuel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
            ],
        ),
        migrations.CreateModel(
            name='Building_mantainance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('vendor_id', models.IntegerField()),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('date', models.DateField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Building_repair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('vendor_id', models.IntegerField()),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('date', models.DateField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Business_Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('percent', models.FloatField(null=True, verbose_name='percent')),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space')),
            ],
        ),
        migrations.CreateModel(
            name='Internet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('internet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('user_id', models.IntegerField()),
                ('year', models.IntegerField()),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel_Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Personnel')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel_Overhead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Personnel')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space')),
            ],
        ),
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('power', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('inventory_id', models.IntegerField(null=True)),
                ('equipment_id', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('year', models.IntegerField()),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
            ],
        ),
        migrations.CreateModel(
            name='Prouct_Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Prouct_shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Prouct_Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Vehical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('year', models.IntegerField()),
                ('active_miles', models.FloatField(null=True, verbose_name='active_miles')),
                ('monthy_miles', models.FloatField(null=True, verbose_name='monthy_miles')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_Fuel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_load',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('max', models.FloatField(null=True, verbose_name='max')),
                ('on_board', models.FloatField(null=True, verbose_name='on_board')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('oil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_mantainance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('vendor_id', models.IntegerField()),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('date', models.DateField(default=datetime.datetime.now, null=True)),
                ('repair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_oil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('oil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_repair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('vendor_id', models.IntegerField()),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('date', models.DateField(default=datetime.datetime.now, null=True)),
                ('repair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_Tire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('cost', models.FloatField(null=True, verbose_name='cost')),
                ('tires', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Vehical')),
            ],
        ),
        migrations.AddField(
            model_name='building_repair',
            name='repair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space'),
        ),
        migrations.AddField(
            model_name='building_mantainance',
            name='repair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space'),
        ),
        migrations.AddField(
            model_name='building_fuel',
            name='building_fuel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space'),
        ),
        migrations.AddField(
            model_name='building',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Business_Space'),
        ),
    ]
