# Generated by Django 3.1.6 on 2021-03-28 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210124_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='expense_description',
            field=models.CharField(default='N/A', max_length=355, null=True, verbose_name='expense_description'),
        ),
    ]