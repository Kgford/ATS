from django import forms
from .models import Vehical,Personnel,Product,Business_Space

  
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehical
        fields = ('name', 'image')
        widgets = {'name': forms.HiddenInput()}
      
class Business_SpaceForm(forms.ModelForm):
    class Meta:
        model = Business_Space
        fields = ('type', 'image')
        widgets = {'type': forms.HiddenInput()}
 
'''      
class PersonnelForm(ModelForm):
  class Meta:
      model = Personnel
      image = CloudinaryFileField(
        attrs = { 'style': "margin-top: 30px" }, 
        options = { 
          'tags': "directly_uploaded",
          'crop': 'limit', 'width': 1000, 'height': 1000,
          'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
        })
      
class ProductForm(ModelForm):
  class Meta:
      model = Product
      image = CloudinaryFileField(
        attrs = { 'style': "margin-top: 30px" }, 
        options = { 
          'tags': "directly_uploaded",
          'crop': 'limit', 'width': 1000, 'height': 1000,
          'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
        })
      

      
'''    
      
      
      
      