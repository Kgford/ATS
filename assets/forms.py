from django import forms 
from .models import *
  
class VehicleForm(forms.ModelForm): 
  
    class Meta: 
        model = Vehical 
        fields = ['name', 'image_file'] 
        
        
class SpaceForm(forms.ModelForm): 
  
    class Meta: 
        model = Business_Space 
        fields = ['building', 'image_file'] 