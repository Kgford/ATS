from django.urls import path
from datetime import datetime
from django.contrib.auth import views as auth_views
from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from accounts.views import (
    ExpensesView,
    SaveExpensesView,
    IncomeView,
    InvoiceItemView,
    CreateInvoiceView,
    SearchInvoiceView,
    ReconsileInvoiceView,
    QuoteItemView,
    CreateQuoteView,
    SearchQuoteView,
    ReconsileQuoteView,
    Charge_codeView,
    ReportView,
    UserLogin
)

app_name = "accounts"

urlpatterns =[
    path('expenses', login_required(ExpensesView.as_view(template_name="expense.html")), name='expenses'),
    path('new_expense', login_required(SaveExpensesView.as_view(template_name="save_expenses.html")), name='new_expense'),
    path('income', login_required(IncomeView.as_view(template_name="income.html")), name='income'),
        
    path('invoice', login_required(SearchInvoiceView.as_view(template_name="invoice.html")), name='invoice'),
    path('invoice_item', login_required(InvoiceItemView.as_view(template_name="invoice_item.html")), name='invoice_item'),
    path('new_invoice', login_required(CreateInvoiceView.as_view(template_name="create_invoice.html")), name='new_invoice'),
    path('invoice_update', login_required(ReconsileInvoiceView.as_view(template_name="reconsile_invoice.html")), name='invoice_update'),
    path('report/', login_required(ReportView.as_view(template_name="report.html")), name='report'),
    
    path('quote', login_required(SearchQuoteView.as_view(template_name="quote.html")), name='quote'),
    path('quote_item', login_required(QuoteItemView.as_view(template_name="quote_item.html")), name='quote_item'),
    path('new_quote', login_required(CreateQuoteView.as_view(template_name="create_quote.html")), name='new_quote'),
    path('quote_update', login_required(ReconsileQuoteView.as_view(template_name="reconsile_quote.html")), name='quote_update'),
    
    path('charge_code', login_required(Charge_codeView.as_view(template_name="charge_code.html")), name='charge_code'),
    path('login', login_required(UserLogin.as_view(template_name="user_login.html")), name='login'),
    path('staff/', include("users.urls")),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)