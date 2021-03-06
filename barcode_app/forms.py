from django.forms import ModelForm
from .models import Barcodes

class BarcodeForm(ModelForm):
    class Meta:
        model = Barcodes
        fields = ('part_number','image', 'standard')