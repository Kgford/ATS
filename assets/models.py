from django.db import models
from datetime import datetime

class Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    user_id = models.IntegerField(null=False,unique=False)
    year = models.IntegerField(null=False,unique=False)
    image_file = models.CharField("Image_file",max_length=20,null=True,unique=False) 
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
    image_file = models.CharField("Image_file",max_length=20,null=True,unique=False) 
    cost = models.FloatField("cost", null=True,unique=False)
    def __str__(self):
        return "%i %s %s" % (self.year, self.model, self.type)
        
class Prouct_Storage(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Product', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost 

class Prouct_shipping(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Product', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost     
        
class Prouct_Insurance(models.Model):
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
    image_file = models.CharField("Image_file",max_length=20,null=True,unique=False) 
    cost = models.FloatField("cost", null=True,unique=False)
    ownership = models.CharField("ownership",max_length=50,null=False,unique=False,default='N/A') 
    last_update = models.DateField(null=True) 
    original_value = models.FloatField("original_value", null=True,unique=False)
    load_limit = models.FloatField("load_limit", null=True,unique=False)
    def __str__(self):
        return "%i %s %s" % (self.year, self.model, self.type)


class Business_Space(models.Model):#commercial building space  
    id = models.AutoField(primary_key=True)
    name = models.CharField("name",max_length=50,null=False,unique=False,default='N/A') 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    image_file = models.CharField("Image_file",max_length=20,null=True,unique=False) 
    space_percentage = models.FloatField("space_percentage", null=True,unique=False)
    power_percentage = models.FloatField("power_percent", null=True,unique=False)
    internet_percentage = models.FloatField("power_percentage", null=True,unique=False)
    insurance_percentage = models.FloatField("insurance_percentage", null=True,unique=False)
    fuel_percentage = models.FloatField("fuel_percentage", null=True,unique=False)
    
class Building(models.Model):
    address = models.CharField("name",max_length=100,null=True,unique=False)
    city = models.CharField("name",max_length=50,null=True,unique=False)
    state = models.CharField("name",max_length=10,null=True,unique=False)
    zip_code = models.CharField("name",max_length=50,null=True,unique=False)
    address = models.CharField("name",max_length=50,null=True,unique=False)
    cost = models.FloatField("cost", null=True,unique=False)
    building = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)  
    def __unicode__(self):
        return self.address 
    
class Insurance(models.Model):
    name = models.CharField("name",max_length=50,null=False,unique=False,default='N/A') 
    type = models.CharField("type",max_length=50,null=False,unique=False,default='N/A') 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    insurance = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost      
    
class Power(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    power = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost  
        
class Internet(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    internet = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost  
        
class Building_Fuel(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    cost = models.FloatField("cost", null=True,unique=False)
    building_fuel = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost  
        
class Phone(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False) 
    date = models.DateField(default=datetime.now,null=True)
    cost = models.FloatField("cost", null=True,unique=False)
    phone = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost  
        
class Building_repair(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False,default='N/A') 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False)
    date = models.DateField(default=datetime.now,null=True)
    vendor_id = models.IntegerField(null=False,unique=False)
    cost = models.FloatField("cost", null=True,unique=False)
    date = models.DateField(default=datetime.now,null=True)
    repair = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost 
        
class Building_mantainance(models.Model):
    name = models.CharField("name",max_length=50,null=True,unique=False) 
    model = models.CharField("model",max_length=50,null=True,unique=False) 
    type = models.CharField("type",max_length=50,null=True,unique=False)
    date = models.DateField(default=datetime.now,null=True)
    vendor_id = models.IntegerField(null=False,unique=False)
    cost = models.FloatField("cost", null=True,unique=False)
    date = models.DateField(default=datetime.now,null=True)
    repair = models.ForeignKey('assets.Business_Space', on_delete=models.CASCADE)
    def __unicode__(self):
        return self.cost 
    
   