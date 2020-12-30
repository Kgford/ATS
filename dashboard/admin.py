from django.contrib import admin
from .models import Income_report,IncomeExpense_report, Purchased_products, Alerts

admin.site.register(Income_report)
admin.site.register(IncomeExpense_report)
admin.site.register(Purchased_products)
admin.site.register(Alerts)
