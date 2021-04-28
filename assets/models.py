from django.db import models
from datetime import datetime
import imghdr # Used to validate images
import urllib.request # Used to download images
from io import StringIO # Used to imitate reading from byte file
from PIL import Image # Holds downloaded image and verifies it
import copy # Copies instances of Image
from django.core.files import File


class Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    user_id = models.IntegerField(null=False,unique=False)
    year = models.IntegerField(null=False,unique=False)
    image = models.ImageField(upload_to='personnel/', null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    def __str__(self):
        return "%i %s %s" % (self.year, self.model, self.type)

class Personnel_Insurance(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=False)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Personnel', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost    
        
class Personnel_Overhead(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Personnel', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost    

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    inventory_id = models.IntegerField(null=True,unique=False)
    equipment_id = models.IntegerField(null=True,unique=False)
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    year = models.IntegerField(null=False,unique=False)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    def __str__(self):
        return "%i %s %s" % (self.year, self.model, self.type)
        
class Product_Storage(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Product', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost 

class Product_shipping(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Product', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost     
        
class Product_Insurance(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=False,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Product', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost       

class Vehical(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("name",max_length=50,null=True,unique=True) 
    make = models.CharField("make",max_length=50,null=False,unique=False,default='N/A') 
    model = models.CharField("model",max_length=50,null=False,unique=False,default='N/A') 
    type = models.CharField("type",max_length=50,null=False,unique=False,default='N/A') 
    year = models.IntegerField(null=True,unique=False)
    original_miles = models.FloatField("original_miles", null=True,unique=False)
    active_miles = models.FloatField("active_miles", null=True,unique=False)
    monthy_miles = models.FloatField("monthy_miles", null=True,unique=False)
    image = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    ownership = models.CharField("ownership",max_length=50,null=False,unique=False,default='N/A') 
    last_update = models.DateField(null=True) 
    original_value = models.FloatField("original_value", null=True,unique=False)
    load_limit = models.FloatField("load_limit", null=True,unique=False)
    business_use = models.BooleanField("business_use",unique=False,default=False)
    print('year=',year)
    def __str__(self):
        return "%s %s" % (self.name, self.model)
   
 
class Business_Space(models.Model):#commercial building space  
    id = models.AutoField(primary_key=True)
    building = models.CharField("buildings",max_length=50,null=False,unique=False,default='N/A') 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    image = models.ImageField(upload_to='buildings/', null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    space_percentage = models.FloatField("space_percentage", null=True,unique=False,default=0)
    power_percentage = models.FloatField("power_percent", null=True,unique=False,default=0)
    internet_percentage = models.FloatField("internet_percentage", null=True,unique=False,default=0)
    insurance_percentage = models.FloatField("insurance_percentage", null=True,unique=False,default=0)
    fuel_percentage = models.FloatField("fuel_percentage", null=True,unique=False,default=0)
    sqr_feet = models.FloatField("sqr_feet", null=True,unique=False,default=100)
    payment_cost = models.FloatField("payment_cost", null=True,unique=False,default=100)
    power_cost = models.FloatField("power_cost", null=True,unique=False,default=100)
    internet_cost = models.FloatField("internet_cost", null=True,unique=False,default=100)
    fuel_cost = models.FloatField("fuel_cost", null=True,unique=False,default=100)
    maintenance_cost = models.FloatField("maintenance_cost", null=True,unique=False,default=100)
    last_update = models.DateField(null=True) 
    def __str__(self):
        return "%s %s" % (self.building, self.type)
        

    
   