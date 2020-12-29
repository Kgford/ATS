from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from background_task import background
from accounts.models import Expenses
import datetime
from django.db.models.functions import Extract

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
        split_date = sale_datee.split("-")
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
def update_income_report():
    year = timestamp.year
    month_num= timestamp.month
    print('year =',year)
    months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
    month = months[str(month_num)]
    print('month =',month)
    return HttpResponse("Hello world !")
    
    
    

def background_view(request):
	return HttpResponse("Hello world !")   
    
    
    
    
    
    