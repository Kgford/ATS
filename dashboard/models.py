from django.db import models
from datetime import datetime

class Income_report(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True,unique=False)
    month_str = models.CharField("month_str",max_length=100,null=False,unique=False) 
    month = models.IntegerField(null=False,unique=False)
    year = models.IntegerField(null=False,unique=False)
    income_paid = models.FloatField("income_paid", null=True,unique=False)
    income_unpaid = models.FloatField("income_unpaid", null=True,unique=False)
    income_total = models.FloatField("income_total", null=True,unique=False)
    expense = models.FloatField("expense",max_length=100,null=True,unique=False) 
    last_update = models.DateField(default=datetime.now,null=True)
    
class IncomeExpense_report(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True,unique=False)
    month_str = models.CharField("charge_type",max_length=100,null=False,unique=False) 
    month = models.IntegerField(null=False,unique=False)
    year = models.IntegerField(null=False,unique=False)
    income_paid = models.FloatField("income_paid", null=True,unique=False)
    income_unpaid = models.FloatField("income_unpaid", null=True,unique=False)
    income_total = models.FloatField("income", null=True,unique=False)
    expense = models.FloatField("expense",max_length=100,null=True,unique=False) 
    last_update = models.DateField(default=datetime.now,null=True)



class Purchased_products(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.IntegerField(null=True,unique=False)
    month_str = models.CharField("charge_type",max_length=100,null=False,unique=False) 
    month = models.IntegerField(null=False,unique=False)
    year = models.IntegerField(null=False,unique=False)
    product = models.CharField("product",max_length=100,null=False,unique=False) 
    income = models.FloatField("income_paid", null=True,unique=False)
    
    
    
class Alerts(models.Model):
    id = models.AutoField(primary_key=True)
    month_str = models.CharField("charge_type",max_length=100,null=False,unique=False) 
    month = models.IntegerField(null=False,unique=False)
    year = models.IntegerField(null=False,unique=False)
    alert_type = models.CharField("product",max_length=50,null=False,unique=False) 
    message = models.CharField("product",max_length=200,null=False,unique=False) 
    last_update = models.DateField(default=datetime.now,null=True)
    