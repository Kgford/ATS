from django.db import models
import barcode                      # additional imports
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

# Create your models here.
class Barcodes(models.Model):
    part_number = models.CharField('part_number', max_length=50, blank=False)
    barcode = models.ImageField(upload_to='barcodes/', blank=True)
    standard = models.CharField('standard', max_length=50, blank=True)
    print('standard in class=',standard)
   
    
    def __str__(self):
        return self.part_number
        
    def save(self, *args, **kwargs):          # overriding save() 
        rv = BytesIO()
        print('standard in save=',self.standard)
        print('self.part_number in save=',self.part_number)
        if self.standard =='code39':
             CODE39 = barcode.get_barcode_class('code39')
             code = CODE39(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='code128':
             CODE128 = barcode.get_barcode_class('code128')
             print('CODE128=',CODE128)
             code = CODE128(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='ean':
             EAN = barcode.get_barcode_class('ean')    
             code = EAN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='ean13':
             EAN13 = barcode.get_barcode_class('ean13')       
             code = EAN13(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='ean8':
             EAN8 = barcode.get_barcode_class('ean8') 
             code = EAN8(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='gs1':
             GS1 = barcode.get_barcode_class('gs1')    
             code = GS1(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='gtin':
             GTIN = barcode.get_barcode_class('gtin')  
             code = GTIN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='isbn':
             ISBN = barcode.get_barcode_class('isbn')  
             code = ISBN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='isbn10':
             ISBN10 = ISBN10.get_barcode_class('isbn10')
             code = COD128(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='isbn13':
             ISBN13 = barcode.get_barcode_class('isbn13')
             code = ISBN13(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='issn':
             ISSN = barcode.get_barcode_class('issn')
             code = ISSN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='jan':
             JAN = barcode.get_barcode_class('jan')
             code = JAN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='pzn':
             PZN = barcode.get_barcode_class('pzn')
             code = PZN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='upc':
             UPC = barcode.get_barcode_class('upc')
             code = UPC(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)
        elif self.standard =='upcn':
             UPCN = barcode.get_barcode_class('upcn')
             code = UPCN(f'{self.part_number}', writer=ImageWriter()).write(rv)
             self.barcode.save(f'{self.part_number}.png', File(rv), save=False)
             return super().save(*args, **kwargs)             