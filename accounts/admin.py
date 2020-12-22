from django.contrib import admin
from .models import Charge_Code, ClassCodes, Expenses, Invoice, Invoice_Item, ZipCode, Income

admin.site.register(Charge_Code)
admin.site.register(ClassCodes)
admin.site.register(Expenses)
admin.site.register(Invoice)
admin.site.register(Invoice_Item)
admin.site.register(ZipCode)
admin.site.register(Income)

# Register your models here.
