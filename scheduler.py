from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from background_task import background
from accounts.models import Expenses, Invoice_Item, Charge_Code, Income, Invoice
from dashboard.models import Income_report
import datetime
from django.db.models.functions import Extract
import time

def update_reoccuring_expenses():
    print('reocurring expenses')
    timestamp = datetime.date.today()
    dt = datetime.datetime.today()
    thisyear = dt.year
    thismonth = dt.month
    thisday = dt.day
    expenses = Expenses.objects.filter(reoccuuring_expenses=True, sale_date__month=thismonth-1, sale_date__year=thisyear).order_by('expense_description').values_list('expense_description', flat=True).distinct()
    print('expense list=',expenses)
    for desc in expenses:
        expense = Expenses.objects.filter(expense_description=desc).last()
        print('expenses =',expense)
        expense_type = expense.expense_type
        print('expense_type =',expense_type)
        expense_description = expense.expense_description
        print('expense_description =',expense_description)
        vendor_id = expense.vendor_id
        item = expense.item
        print('item =',item)
        item_desc = expense.item_desc
        print('item_desc =',item_desc)
        quantity = expense.quantity
        print('quantity =',quantity)
        item_cost = expense.item_cost
        print('item_cost =',item_cost)
        total_cost = expense.total_cost
        print('total_cost =',total_cost)
        operator = expense.operator
        print('operator =',operator)
        interval = expense.reoccuring_interval
        print('interval =',interval)
        sale_date = expense.sale_date
        print('sale_date =',sale_date)
        split_date = str(sale_date).split("-")
        split_date2 = str(split_date[2]).split(" ")
        print('split_date=',split_date)
        print('split_date2=',split_date2)
        syear = int(split_date[0])
        print('year =',syear)
        month = int(split_date[1])
        print('month =',month)
        day = int(split_date2[0])
        print('day =',day)
        temp_year = syear
        temp_month = month
        print('temp_month =',temp_month)
        temp_date = str(thisyear) + "-" + str(thismonth)  + "-" + str(day)
        print('temp_date =',temp_date)
        temp_date = str(thisyear) + "-" + str(thismonth)  + "-" + str(day)
        if not Expenses.objects.filter(expense_description=expense_description, sale_year__month=thisyear, sale_date__month=thismonth, sale_date__day=thisday).exists():
            Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_description, sale_date=temp_date, item=item,
                                      item_desc=item_desc,quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=True, 
                                      reoccuring_interval=interval,operator=operator, last_update=timestamp)
            print('updated reoccuring expenses for date: ',temp_date)
        else:
            print('No reoccuring ',desc,' expenses required at this time')

def update_Income_report():
    timestamp = datetime.date.today()
    dt = datetime.datetime.today()
    thisyear = dt.year
    thismonth = dt.month
    thisday = dt.day
    months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
    monthstr = months[str(thismonth)]
    invoices = Invoice.objects.all()
    print('invoices=',invoices)
    print('updating income report data')
    for y in range(2017, int(dt.year) + 1):
        for m in range(1, int(dt.month) + 1):
            temp_date = str(y) + "/" + str(m) 
            print('temp_date=',temp_date)
            invoices = Invoice.objects.filter(invoice_date__month=m).filter(invoice_date__year=y).all()
            invoice_count = Invoice.objects.filter(invoice_date__month=m).filter(invoice_date__year=y).count()
            print('invoices=',invoices)
            print('invoice_count=',invoice_count)
            total=0
            if invoices:
                for inv in invoices:
                    print('single total =',inv.total)
                    invoice_date = inv.invoice_date
                    print('invoice_date =',invoice_date)
                    client_id = inv.client_id
                    print('client_id =',client_id)
                    if inv.total:
                        total = total + float(inv.total)
                        print('total =',total)
                    paid = True
                    print('paid =',paid)
                    income = total
                    print('income =',income)
                    if paid:
                        income_paid = total
                        income_unpaid = 0
                    else:
                        income_paid = 0
                        income_unpaid = total
                    
                    print('invoice_date =',invoice_date)
                    invoice_date=str(invoice_date)
                    split_date = invoice_date.split("-")
                    year = int(split_date[0])
                    print('year =',year)
                    month = int(split_date[1])
                    print('month =',month)
                    day = int(split_date[2])
                    print('day =',day)
                    temp_year = year
                    temp_month = month
                    monthstr = months[str(temp_month)]
                    temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                                      
                monthstr = months[str(m)]
                temp_date = str(y) + "-" + str(m)  + "-" + str(day)
                if not Income_report.objects.filter(month=m).filter(year=y).exists():
                    Income_report.objects.create(client_id=client_id, month_str=monthstr, month=m, year=y,
                                          income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                    print('saving income total',income,' Date =',temp_date)
                else:
                    Income_report.objects.filter(month=m).filter(year=y).update(income_total=income, income_paid=income_paid, income_unpaid=income_unpaid)
                    print('updating income total',income,' Date =',temp_date)
                    
                if not Income_report.objects.filter(month=m).filter(year=y).exists():
                    Income_report.objects.create(client_id=client_id, month_str=monthstr, month=m, year=y,
                                          income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                    print('saving income total',income,' Date =',temp_date)
                else:
                    Income_report.objects.filter(month=m).filter(year=y).update(income_total=income, income_paid=income_paid, income_unpaid=income_unpaid)
                    print('updating income total',income,' Date =',temp_date)
                
                print('income_total =',income,' Date =',temp_date)                          
                print('updated income report for date: ',temp_date)
                
       
    
    for y in range(2017, int(dt.year) + 2):
        for m in range(1, int(dt.month) + 2):
            expenses = Expenses.objects.filter(sale_date__month=m, sale_date__year=y).all()
            temp_date = str(y) + "-" + str(m)  + "-" + str(1)
            print('expenses=',expenses)
            if expenses:
                total = 0
                for exp in expenses:
                    sale_date = exp.sale_date
                    print('sale_date =',sale_date)
                    if exp.total_cost:
                        total = total + float(exp.total_cost)
                    print('expense_total =',total)
                    sale_date=str(sale_date)
                    split_date = sale_date.split("-")
                    year = int(split_date[0])
                    print('year =',year)
                    month = int(split_date[1])
                    print('month =',month)
                    day = 1
                    print('day =',day)
                    temp_year = year
                    temp_month = month
                    temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                    print('temp_date =',temp_date)
                    print('total =',total)
                    
                
                Income_report.objects.filter(month=m, year=y).update(expense=total)
                print('updated income report expenses for date: ',temp_date)
                print('total =',total)
                  
    
    
    

def background_view(request):
	return HttpResponse("Hello world !")   
    
    
    
    
    
    