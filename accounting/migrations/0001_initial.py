# Generated by Django 2.1.15 on 2020-12-17 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client_id', models.IntegerField(null=True)),
                ('charge_code', models.CharField(default='N/A', max_length=100, null=True, verbose_name='charge')),
                ('charge_desc', models.CharField(default='N/A', max_length=255, null=True, verbose_name='charge')),
                ('service_type', models.CharField(default='N/A', max_length=100, null=True, verbose_name='service type')),
                ('active_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassCodes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ClassCode', models.CharField(default='N/A', max_length=50, null=True, verbose_name='class code')),
                ('InventoryClass', models.CharField(default='N/A', max_length=50, null=True, verbose_name='inv class')),
                ('Client', models.CharField(default='N/A', max_length=50, null=True, verbose_name='client')),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contractor_Quote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('InvoiceID', models.IntegerField(null=True)),
                ('ResourceID', models.IntegerField(null=True)),
                ('CustomerID', models.IntegerField(null=True)),
                ('ResourceName', models.CharField(default='N/A', max_length=100, null=True, verbose_name='resource name')),
                ('ResourceType', models.CharField(default='N/A', max_length=100, null=True, verbose_name='resource type')),
                ('ResourceDept', models.CharField(default='N/A', max_length=100, null=True, verbose_name='resource dept')),
                ('InvoiceDate', models.DateField(null=True)),
                ('ChargeCode', models.CharField(default='N/A', max_length=100, null=True, verbose_name='charge code')),
                ('Quantity', models.FloatField(null=True, verbose_name='quantity')),
                ('Rate', models.FloatField(null=True, verbose_name='rate')),
                ('Total', models.FloatField(null=True, verbose_name='total')),
                ('Client', models.CharField(default='N/A', max_length=50, null=True, verbose_name='client')),
                ('StaffID', models.CharField(default='N/A', max_length=50, null=True, verbose_name='staff id')),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contractor_QuoteID',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('InvoiceReference', models.CharField(default='N/A', max_length=50, null=True, verbose_name='invoice ref')),
                ('Customer', models.CharField(default='N/A', max_length=50, null=True, verbose_name='client')),
                ('InvoiceDate', models.DateField(null=True)),
                ('Paid', models.BooleanField(default=True, null=True, verbose_name='paid')),
                ('Client', models.CharField(default='N/A', max_length=50, null=True, verbose_name='client')),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vendor_id', models.CharField(default='N/A', max_length=50, null=True, verbose_name='vendor id')),
                ('expense_type', models.CharField(default='N/A', max_length=50, null=True, verbose_name='expense type')),
                ('expense_description', models.CharField(default='N/A', max_length=355, null=True, verbose_name='expense desc')),
                ('sale_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('item', models.CharField(default='N/A', max_length=50, null=True, verbose_name='item')),
                ('item_desc', models.CharField(default='N/A', max_length=355, null=True, verbose_name='item desc')),
                ('quantity', models.CharField(default='N/A', max_length=50, null=True, verbose_name='quantity')),
                ('item_cost', models.CharField(default='N/A', max_length=50, null=True, verbose_name='item cost')),
                ('total_cost', models.CharField(default='N/A', max_length=50, null=True, verbose_name='total cost')),
                ('reoccuuring_expenses', models.BooleanField(default=False, null=True, verbose_name='reoccuuring_expenses')),
                ('reoccuring_interval', models.CharField(default='N/A', max_length=255, null=True, verbose_name='reoccuring interval')),
                ('invoice_id', models.CharField(default='N/A', max_length=255, null=True, verbose_name='invoiceID')),
                ('operator', models.CharField(default='N/A', max_length=50, null=True, verbose_name='staff id')),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client_id', models.CharField(default='N/A', max_length=50, null=True, verbose_name='vendor id')),
                ('invoice_id', models.CharField(default='N/A', max_length=50, null=True, verbose_name='vendor id')),
                ('income_type', models.CharField(default='N/A', max_length=50, null=True, verbose_name='expense type')),
                ('income_description', models.CharField(default='N/A', max_length=355, null=True, verbose_name='expense desc')),
                ('invoice_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('payment_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('total', models.FloatField(null=True, verbose_name='total')),
                ('operator', models.CharField(default='N/A', max_length=50, null=True, verbose_name='staff id')),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoiceItem_id', models.IntegerField(null=True)),
                ('client_id', models.IntegerField(null=True)),
                ('item_id', models.IntegerField(null=True)),
                ('staff_id', models.IntegerField(null=True)),
                ('charge_code', models.CharField(default='N/A', max_length=100, null=True, verbose_name='resource name')),
                ('paid', models.BooleanField(default=True, null=True, verbose_name='paid')),
                ('payment_date', models.DateField(null=True)),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client_id', models.IntegerField(null=True)),
                ('charge_id', models.IntegerField(null=True)),
                ('vendor_id', models.IntegerField(null=True)),
                ('resource_type', models.CharField(default='N/A', max_length=100, null=True, verbose_name='resource type')),
                ('service_type', models.CharField(default='N/A', max_length=100, null=True, verbose_name='service type')),
                ('service_provider', models.CharField(default='N/A', max_length=100, null=True, verbose_name='service provider')),
                ('cost_type', models.CharField(default='N/A', max_length=100, null=True, verbose_name='cost type')),
                ('item_date', models.DateField(null=True)),
                ('item_desc', models.CharField(default='N/A', max_length=100, null=True, verbose_name='item description')),
                ('rate', models.FloatField(null=True, verbose_name='rate')),
                ('quantity', models.IntegerField(null=True)),
                ('total', models.FloatField(null=True, verbose_name='total')),
                ('last_update', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ZipCode', models.CharField(default='N/A', max_length=50, null=True, verbose_name='ZipCode')),
                ('PlaceName', models.CharField(default='N/A', max_length=50, null=True, verbose_name='PlaceName')),
                ('StateAbreviation', models.CharField(default='N/A', max_length=50, null=True, verbose_name='StateAbreviation')),
                ('County', models.CharField(default='N/A', max_length=50, null=True, verbose_name='County')),
                ('Latitude', models.CharField(default='N/A', max_length=50, null=True, verbose_name='Latitude')),
                ('Longitude', models.CharField(default='N/A', max_length=50, null=True, verbose_name='Longitude')),
                ('StateTax', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='StateTax')),
                ('LocalTax', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='LocalTax')),
                ('TotalTax', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='TotalTax')),
                ('FiscalDate', models.DateField(null=True)),
                ('backup_index', models.IntegerField(null=True)),
            ],
        ),
    ]
