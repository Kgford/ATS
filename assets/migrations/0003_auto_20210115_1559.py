# Generated by Django 2.1.15 on 2021-01-15 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20210105_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_space',
            name='percent',
        ),
        migrations.AddField(
            model_name='business_space',
            name='fuel_percentage',
            field=models.FloatField(null=True, verbose_name='fuel_percentage'),
        ),
        migrations.AddField(
            model_name='business_space',
            name='image_file',
            field=models.CharField(max_length=20, null=True, verbose_name='Image_file'),
        ),
        migrations.AddField(
            model_name='business_space',
            name='insurance_percentage',
            field=models.FloatField(null=True, verbose_name='insurance_percentage'),
        ),
        migrations.AddField(
            model_name='business_space',
            name='internet_percentage',
            field=models.FloatField(null=True, verbose_name='power_percentage'),
        ),
        migrations.AddField(
            model_name='business_space',
            name='name',
            field=models.CharField(default='N/A', max_length=50, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='business_space',
            name='power_percentage',
            field=models.FloatField(null=True, verbose_name='power_percent'),
        ),
        migrations.AddField(
            model_name='business_space',
            name='space_percentage',
            field=models.FloatField(null=True, verbose_name='space_percentage'),
        ),
        migrations.AlterField(
            model_name='building_repair',
            name='name',
            field=models.CharField(default='N/A', max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='name',
            field=models.CharField(default='N/A', max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='type',
            field=models.CharField(default='N/A', max_length=50, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='prouct_insurance',
            name='type',
            field=models.CharField(max_length=50, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehical',
            name='model',
            field=models.CharField(default='N/A', max_length=50, verbose_name='model'),
        ),
        migrations.AlterField(
            model_name='vehical',
            name='name',
            field=models.CharField(default='N/A', max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='vehical',
            name='type',
            field=models.CharField(default='N/A', max_length=50, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='vehical',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
