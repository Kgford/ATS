from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from background_task import background
from accounts.models import Expenses, Invoice_Item, Charge_Code, Income, Invoice
from dashboard.models import Income_report
import datetime
from django.db.models.functions import Extract
import time

# Create your views here.
@background(schedule=5)
def update_reoccuring_expenses():
    print('reocurring expenses')
    timestamp = date.today()
    dt = datetime.datetime.today()
    thisyear = dt.year
    thismonth = dt.month
    thisday = dt.day
    expenses = Expenses.objects.filter(reoccuuring_expenses=True).order_by('expense_description').values_list('expense_description', flat=True).distinct()
    print('expense list=',expenses)
    for desc in expenses:
        expense = Expenses.objects.filter(expense_description=desc).last()
        print('expensee =',expense)
        expense_type = expense.expense_type
        print('expense_type =',expense_type)
        expense_description = expense.expense_description
        print('expense_description =',expense_description)
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
        split_date = sale_date.split("-")
        year = int(split_charge[0])
        print('year =',syear)
        month = int(split_charge[2])
        print('month =',month)
        day = int(split_charge[2])
        print('day =',day)
        temp_year = year
        temp_month = month
        temp_date = thisyear + "-" + thismonth  + "-" + day
        print('temp_date =',temp_date)
        if temp_year<thisyear: # this catches up all entries from the start date
            temp_month = 1
            while temp_month<=month:
                temp_date = temp_year + "-" + temp_month  + "-" + day
                Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc, sale_date=temp_date, item=item_name,
                                          item_desc=item_desc,quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=True, 
                                          reoccuring_interval=interval_time,operator=operator, last_update=timestamp)
                temp_month +=1
            temp_year +=1
            print('updated all reoccuring ',desc,' expenses for year ',temp_year)
        elif temp_month<thismonth: # this catches up on all months for this year
            while temp_month<=month:
                temp_date = temp_year + "-" + temp_month  + "-" + day
                Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc, sale_date=temp_date, item=item_name,
                                          item_desc=item_desc,quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=True, 
                                          reoccuring_interval=interval_time,operator=operator, last_update=timestamp)
                temp_month +=1
                print('updated all reoccuring ',desc,' expenses for date: ',temp_date)
        else: # this updates for the month if not done already
            temp_date = thisyear + "-" + thismonth  + "-" + day
            if not Expenses.objects.filter(expense_description=expense_desc, sale_date=temp_date).exists():
                Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc, sale_date=temp_date, item=item_name,
                                          item_desc=item_desc,quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=True, 
                                          reoccuring_interval=interval_time,operator=operator, last_update=timestamp)
                print('updated reoccuring expenses for date: ',temp_date)
            else:
                print('No reoccuring ',desc,' expenses required at this time')

@background(schedule=5)
def update_Income_report():
    timestamp = date.today()
    dt = datetime.datetime.today()
    thisyear = dt.year
    thismonth = dt.month
    thisday = dt.day
    months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
    monthstr = months[str(thismonth)]
    invoices = Invoice.objects.all()
    print('invoices=',invoices)
    for y in range(2017, int(dt.year)):
        for m in range(1, int(dt.month)):
            temp_date = str(y) + "-" + str(m)  + "-" + str(1)
            invoices = Invoice_Item.objects.filter(item_date__month=m, item_date__year=y).all()
            print(invoices)
            total=0
            if invoices:
                for inv in invoices:
                    total = inv.total
                    invoice_date = inv.item_date
                    print('invoice_date =',invoice_date)
                    client_id = inv.client_id
                    print('client_id =',client_id)
                    if inv.total:
                        total = total + float(inv.total)
                    print('total =',total)
                    paid = True
                    print('paid =',paid)
                    income = total
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
                
                print('temp_date =',temp_date)
                print('income_total =',income)
                time.sleep(3)
                
                if temp_year<thisyear: # this catches up all entries from the start date
                    temp_month = 1
                    while temp_month<=month:
                        temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                        if not Income_report.objects.filter(month=temp_month, year=thisyear).exists():
                            Income_report.objects.create(client_id=client_id, month_str=monthstr, month=temp_month, year=thisyear,
                                                  income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                        else:
                            Income_report.objects.filter(month=temp_month, year=thisyear).update(income_total=income, income_paid=income_paid)
                                                  
                        temp_month +=1
                    temp_year +=1
                    print('updated income report for date: ',temp_date)
                elif temp_month<thismonth: # this catches up on all months for this year
                    while temp_month<=month:
                        temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                        if not Income_report.objects.filter(month=temp_month, year=thisyear).exists():
                            Income_report.objects.create(client_id=client_id, month_str=monthstr, month=temp_month, year=thisyear,
                                                  income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                        else:
                            Income_report.objects.filter(month=temp_month, year=thisyear).update(income_total=income, income_paid=income_paid)
                        
                        temp_month +=1
                        print('updated income report for date: ',temp_date)
                else: # this updates for the month if not done already
                    temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                    if not Income_report.objects.filter(month=temp_month, year=thisyear).exists():
                        Income_report.objects.create(client_id=client_id, month_str=monthstr, month=temp_month, year=thisyear,
                                              income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                    else:
                        Income_report.objects.filter(month=temp_month, year=thisyear).update(income_total=income, income_paid=income_paid)
                        print('updated income report for date: ',temp_date)
        
    
    for y in range(2017, int(dt.year)):
        for m in range(1, int(dt.month)):
            expenses = Expenses.objects.filter(sale_date__month=m, sale_date__year=y).all()
            temp_date = str(y) + "-" + str(m)  + "-" + str(1)
            print('expenses=',expenses)
            total = 0
            if expenses:
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
                    temp_date = str(thisyear) + "-" + str(temp_month)  + "-" + str(day)
                    print('temp_date =',temp_date)
                    print('total =',total)
                    
                time.sleep(3)
                Income_report.objects.filter(month=temp_month, year=thisyear).update(expense=total)
                print('updated income report expenses for date: ',temp_date)
    
    
    
    

def background_view(request):
	return HttpResponse("Hello world !")   
    
    
    
    
    
    