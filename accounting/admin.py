from django.contrib import admin
from .models import ChargeCodes, ClassCodes, Expenses, Invoice, Invoice_Item, ZipCode

admin.site.register(ChargeCodes)
admin.site.register(ClassCodes)
admin.site.register(Expenses)
admin.site.register(Invoice)
admin.site.register(Invoice_Item)
admin.site.register(ZipCode)

# Register your models here.
