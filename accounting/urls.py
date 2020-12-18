from django.urls import path
from datetime import datetime
from django.contrib.auth import views as auth_views
from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from accounting.views import (
    ExpensesView,
    SaveExpensesView,
    IncomeView,
    SaveIncomeView,
    InvoiceItemView,
    Charge_codeView,
)

app_name = "accounting"

urlpatterns =[
    path('expenses', login_required(ExpensesView.as_view(template_name="expense.html")), name='expenses'),
    path('new_expense', login_required(SaveExpensesView.as_view(template_name="save_expenses.html")), name='new_expense'),
    path('income', login_required(IncomeView.as_view(template_name="income.html")), name='income'),
    path('new_income', login_required(SaveIncomeView.as_view(template_name="save_income.html")), name='new_income'),
    path('invoice_item', login_required(InvoiceItemView.as_view(template_name="invoice_item.html")), name='invoice_item'),
    path('charge_code', login_required(Charge_codeView.as_view(template_name="charge_code.html")), name='charge_code'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)