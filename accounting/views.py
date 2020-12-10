from django import forms
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from datetime import date
from django.urls import reverse, reverse_lazy
from equipment.models import Model
from locations.models import Location
from inventory.models import Inventory, Events
from accounting.models import Expenses
from vendors.models import Vendors
from django.views import View
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear 

class ExpensesView(View):
  
    template_name = "expense.html"
    success_url = reverse_lazy('accounting:expenses')
    def get(self, *args, **kwargs):
        try:
            desc_list=-1
            type_list=-1
            item_name_list=-1
            item_desc_list=-1
            operator = str(self.request.user)
            desc_list = Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            type_list = Expenses.objects.order_by('expense_type').values_list('expense_type', flat=True).distinct()
            item_name_list = Expenses.objects.order_by('item').values_list('item', flat=True).distinct()
            item_desc_list = Expenses.objects.order_by('item_desc').values_list('item_desc', flat=True).distinct()
            #year_list = [d.year for d in Expenses.objects.all().datetimes('sale_date', 'year')]
            years = Expenses.objects.order_by('sale_date').values_list('sale_date', flat=True).distinct()
            year_list=[]
            for year in years:
                dt = year.split('-')
                print(dt[0])
                year_list.append(dt[0])
               
                
            print("year_list",year_list)           
            print("in GET")
            expense_list = Expenses.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/expense.html",{"expense_list": expense_list, "desc_list":desc_list, "type_list":type_list,"item_name_list":item_name_list, "item_desc_list":item_desc_list, "year_list":year_list, "operator":operator})
    
    def post(self, request, *args, **kwargs):
        try: 
            #print("in POST")
            operator = str(self.request.user)
            type_list = []
            inv_list = []
            inv = []
            search = request.POST.get('search', -1)
            #print('search =',search)
            vendor = request.POST.get('_vendor', -1)
            expense_type = request.POST.get('_exp_type', -1)
            #print('expense_type = ',expense_type)
            expence_desc = request.POST.get('_exp_desc', -1)
            #print('expence_desc =',expence_desc)
            item_name = request.POST.get('_item_name', -1)
            #print('item_name =',item_name)
            item_desc = request.POST.get('_item_desc', -1)
            #print('item_desc =',item_desc)
              
            desc_list = Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            type_list = Expenses.objects.order_by('expense_type').values_list('expense_type', flat=True).distinct()
            item_name_list = Expenses.objects.order_by('item').values_list('item', flat=True).distinct()
            item_desc_list = Expenses.objects.order_by('item_desc').values_list('item_desc', flat=True).distinct()
            #year_list = [d.year for d in Expenses.objects.all().datetimes('sale_date', 'year')]
            year_list = Expenses.objects.order_by('sale_date').values_list('sale_date', flat=True).distinct()
           
                        
            success = True
            if not search ==-1:
                expense_list = Expenses.objects.filter(vendor_id__icontains=search) | Expenses.objects.filter(expense_type__icontains=search) | Expenses.objects.filter(expense_description__icontains=search) | Expenses.objects.filter(item_name__icontains=search) | Expenses.objects.filter(item_desc__icontains=search) | Expenses.objects.filter(item_cost__contains=search) | Expenses.objects.filter(expense_date__contains=search) | Expenses.objects.filter(invoice__icontains=search).all()
            elif not expense_type =="select menu": 
                if expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(expense_type=expense_type).all()
                if not expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
            elif not expense_desc =="select menu": 
                if expense_type == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(expense_description=expense_desc).all()
                if not expense_type == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc).all()  
                if not expense_type == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not expense_type == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
            elif not item_name =="select menu": 
                if item_name == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(item=item_name).all()
                if not item_name == "select menu" and expense_desc == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(item=item_name, expense_description__contains=expense_desc).all()  
                if not item_name == "select menu" and not expense_desc == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not item_name == "select menu" and not expense_desc == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all()
            elif not item_desc =="select menu": 
                if expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(item_desc=item_desc).all()
                if not expense_desc == "select menu" and item_name == "select menu" and expense_type == "select menu":  
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and expense_type == "select menu": 
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and not expense_type == "select menu": 
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc, item__contains=item_name, expense_type__contains=expense_type).all() 
            else:
                expense_list = Expenses.objects.all()
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('expense_list',expense_list)
        return render (self.request,"accounting/expense.html",{"expense_list": expense_list, "desc_list":desc_list, "type_list":type_list,"item_name_list":item_name_list, "item_desc_list":item_desc_list, "year_list":year_list, "operator":operator})
           
           
class SaveExpensesView(View):
    template_name = "save_expenses.html"
    success_url = reverse_lazy('accounting:new_expense')
    def get(self, *args, **kwargs):
        try:
            vendor = -1
            interval = 'off'
            exp_id = self.request.GET.get('expense_id', -1)
            vendor_id = self.request.GET.get('vendor_id', -1)
            print('exp_id =',exp_id)
            print('vendor_id =',vendor_id)
            operator = str(self.request.user)
            expense_list = Expenses.objects.all()
            desc_list =  Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            vendor_list =  Vendors.objects.order_by('name').values_list('name', flat=True).distinct()
            print('vendor_list =',vendor_list)
            if exp_id !=-1:
                exp = Expenses.objects.filter(id=exp_id)
                exp = exp[0]
                if exp.reoccuuring_expenses == True:
                    interval = 'on'
                else:
                    interval = 'off'
                print('exp=',exp.sale_date)
            else:
                exp =-1
                
            if vendor_id !=-1:
                vendor = Vendors.objects.filter(id=vendor_id)
                vendor = vendor[0].name
                print('vendor=',vendor)
            
            print('exp=', exp)
            print("in GET")
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'vendor':vendor, "operator":operator,'interval':interval})

    def post(self, request, *args, **kwargs):
        vendor_list = []
        expense_list =[]
        desc_list = []
        exp =-1
        vendor =-1
        
        try: 
            print("in POST")
            timestamp = date.today()
            operator = str(self.request.user)
            exp_id = request.POST.get('e_id', -1)
            print('exp_id =',exp_id)
            expense_list = Expenses.objects.all()
            desc_list =  Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            vendor_list =  Vendors.objects.order_by('name').values_list('name', flat=True).distinct()
            if exp_id !=-1:
                exp = Expenses.objects.filter(id=exp_id).all()
            
            
            search = request.POST.get('search', -1)
            print('search =',search)
            vendor = request.POST.get('_vendor', -1)
            print('vendor = ',vendor)
            expense_type = request.POST.get('_exp_type', -1)
            print('expense_type = ',expense_type)
            expense_desc = request.POST.get('_exp_desc', -1)
            print('expense_desc =',expense_desc)
            item_name = request.POST.get('_item_name', -1)
            print('item_name =',item_name)
            item_desc = request.POST.get('_item_desc', -1)
            print('item_desc =',item_desc)
            quantity = request.POST.get('_quantity', -1)
            print('quantity =',quantity)
            item_cost = request.POST.get('_item_cost', -1)
            print('item_cost =',item_cost)
            total_cost = request.POST.get('_total_cost', -1)
            print('total_cost =',total_cost)
            sale_date = request.POST.get('_sale_date', -1)
            print('sale_date =',sale_date)
            invoice = request.POST.get('_invoice', -1)
            print('invoice =',invoice)
            interval = request.POST.get('_interval', False)
            print('interval =',interval)
            
            interval_time = request.POST.get('_interval_time', -1)
            print('interval_time =',interval_time)
            save_exp = request.POST.get('_save', -1)
            print('save_exp =',save_exp)
            update_exp = request.POST.get('_update', -1)
            print('update_exp =',update_exp)
            del_exp = request.POST.get('_delete', -1)
            print('del_exp =',del_exp)
            quantity = request.POST.get('_quantity', -1)
            print('quantity =',quantity)
            success = True
            if interval_time=='select option':
                interval_time = "N/A"
           
            print('interval=',interval)    
            if interval =='on':
                interval_save = True
            else:
                interval_save = False
            
            print('interval=',interval)
            if not del_exp==-1:
                try:
                   #update item	
                    Expenses.objects.filter(id=expense_id).delete()
                    print('delete complete')
                    exp=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
                    return HttpResponseRedirect(reverse('accounting:expenses'))
            elif not update_exp==-1:
                #update item	
                ven = Vendors.objects.filter(name=vendor)
                vendor_id = ven[0].id
                print('vendor_id=',vendor_id)
                Expenses.objects.filter(id=exp_id).update(vendor_id=vendor_id,expense_type=expense_type,expense_description=expense_desc,sale_date=sale_date,item=item_name,item_desc=item_desc,
                                        quantity=quantity,item_cost=item_cost,total_cost=total_cost,reoccuuring_expenses=interval_save,reoccuring_interval=interval_time,operator=operator,last_update=timestamp)
                exp=-1
            elif not save_exp==-1:
                if Expenses.objects.filter(item=item_name).exists():
                    exp = Expenses.objects.filter(item=item_name).all()
                    return render (self.request,"accounting/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'vendor':vendor, "operator":operator})
                else:
                   #save item	
                    ven = Vendors.objects.filter(name=vendor)
                    vendor_id = ven[0].id
                    print('vendor_id=',vendor_id)
                    Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc, sale_date=sale_date, item=item_name, item_desc=item_desc,
                                          quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=interval_save, reoccuring_interval=interval_time, operator=operator, last_update=timestamp)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, "desc_list":desc_list, "exp":exp, "vendor":vendor, "operator":operator})     
        