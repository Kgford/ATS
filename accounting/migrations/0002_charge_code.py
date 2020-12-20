# Generated by Django 2.1.15 on 2020-12-17 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charge_Code',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('charge_type', models.CharField(default='N/A', max_length=100, null=True, verbose_name='charge_type')),
                ('client_id', models.IntegerField(null=True)),
                ('charge', models.CharField(default='N/A', max_length=100, null=True, verbose_name='charge code')),
                ('charge_desc', models.CharField(default='N/A', max_length=100, null=True, verbose_name='charge_desc')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('last_update', models.DateField(null=True)),
            ],
        ),
    ]