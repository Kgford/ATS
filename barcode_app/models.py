from django.db import models

# Create your models here.
class Barcodes(models.Model):
    part_number = models.CharField('part_number', max_length=50, blank=False)
    part_desc = models.CharField('part_desc',max_length=200, blank=True)
    barcode = models.ImageField(upload_to='barcodes/', blank=True)
    inventory_id = models.ForeignKey('inventory.Inventory',on_delete=models.CASCADE,)
    created_on = models.DateField(null=True)   
    
    def __str__(self):
        return self.part_number