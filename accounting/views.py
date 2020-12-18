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
from client.models import Clients
from inventory.models import Inventory, Events
from accounting.models import Expenses, Invoice_Item, Charge_Code, Income, Invoices
from vendor.models import Vendor
from contractors.models import Contractors
from django.views import View
import datetime
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear 


class ExpensesView(View):
  
    template_name = "expense.html"
    success_url = reverse_lazy('accounting:expenses')
    def get(self, *args, **kwargs):
        try:
            year = datetime.date.today().year
            print('year',year)
            desc_list=-1
            type_list=-1
            item_name_list=-1
            item_desc_list=-1
            total=0
            expense_type =-1
            expense_desc =-1
            item_name = -1
            item_desc =-1
            operator = str(self.request.user)
            desc_list = Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            type_list = Expenses.objects.order_by('expense_type').values_list('expense_type', flat=True).distinct()
            item_name_list = Expenses.objects.order_by('item').values_list('item', flat=True).distinct()
            item_desc_list = Expenses.objects.order_by('item_desc').values_list('item_desc', flat=True).distinct()
            years = Expenses.objects.order_by('sale_date').values_list('sale_date', flat=True).distinct()
            year_list=[]
            for year1 in years:
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
            print("in GET")
            expense_list = Expenses.objects.all()
            for expense in expense_list:
                total=round(total+float(expense.total_cost),2)
            print(total)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/expense.html",{"expense_list": expense_list, "desc_list":desc_list, "type_list":type_list,"item_name_list":item_name_list, "expense_type":expense_type,
                        "expense_desc":expense_desc, "item_name":item_name, "item_desc":item_desc, "item_desc_list":item_desc_list, "year_list":year_list, "operator":operator, 'total':total, 'year':year})
    
    def post(self, request, *args, **kwargs):
        try: 
            #print("in POST")
            operator = str(self.request.user)
            type_list = []
            inv_list = []
            inv = []
            total=0
            search = request.POST.get('search', -1)
            print('search =',search)
            vendor = request.POST.get('_vendor', -1)
            expense_type = request.POST.get('_exp_type', -1)
            print('expense_type = ',expense_type)
            expense_desc = request.POST.get('_exp_desc', -1)
            print('expense_desc =',expense_desc)
            item_name = request.POST.get('_item_name', -1)
            print('item_name =',item_name)
            item_desc = request.POST.get('_item_desc', -1)
            print('item_desc =',item_desc)
            year_c = request.POST.get('_year', -1)
            if year_c ==-1:
                year_c = datetime.date.today().year
            print('year =',year_c)
            year = datetime.date.today().year
            desc_list = Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            type_list = Expenses.objects.order_by('expense_type').values_list('expense_type', flat=True).distinct()
            item_name_list = Expenses.objects.order_by('item').values_list('item', flat=True).distinct()
            item_desc_list = Expenses.objects.order_by('item_desc').values_list('item_desc', flat=True).distinct()
            years = Expenses.objects.order_by('sale_date').values_list('sale_date', flat=True).distinct()
            year_list=[]
            for year1 in years:
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
            print("year_list",year_list) 
            print('year',year_c)
            success = True
            #expense_list = Expenses.objects.all() 
            if not search ==-1:
                if  Expenses.objects.filter(vendor_id__icontains=search).exists():
                    expense_list = Expenses.objects.filter(vendor_id__icontains=search).all()
                    print('search 1=',expense_list)
                elif  Expenses.objects.filter(expense_type__icontains=search).exists():
                    expense_list = Expenses.objects.filter(expense_type__icontains=search).all()
                    print('search 2=',expense_list)
                elif Expenses.objects.filter(expense_description__icontains=search).exists():
                    expense_list = Expenses.objects.filter(expense_description__icontains=search).all() 
                    print('search 3=',expense_list)
                elif Expenses.objects.filter(item__icontains=search).exists():
                    expense_list = Expenses.objects.filter(item__icontains=search).all()
                    print('search 4=',expense_list)
                elif Expenses.objects.filter(item_desc__icontains=search).exists():
                    expense_list = Expenses.objects.filter(item_desc__icontains=search).all()
                    print('search 5=',expense_list)
                elif Expenses.objects.filter(item_cost__icontains=search).exists():
                    expense_list = Expenses.objects.filter(item_cost__contains=search).all()
                    print('search 6=',expense_list)
                elif Expenses.objects.filter(sale_date__contains=search).exists():
                    expense_list = Expenses.objects.filter(sale_date__contains=search).all()
                    print('esearch 7=',expense_list)
            elif not expense_type =="select menu": 
                if expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(expense_type=expense_type).all()
                if not expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                print('expense_type =',expense_list)
            elif not expense_desc =="select menu": 
                if expense_type == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(expense_description=expense_desc).all()
                if not expense_type == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc).all()  
                if not expense_type == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not expense_type == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                print('expense_desc =',expense_list)
            elif not item_name =="select menu": 
                if item_name == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(item=item_name).all()
                if not item_name == "select menu" and expense_desc == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(item=item_name, expense_description__contains=expense_desc).all()  
                if not item_name == "select menu" and not expense_desc == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not item_name == "select menu" and not expense_desc == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all()
                print('item_name =',expense_list)
            elif not item_desc =="select menu": 
                if expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(item_desc=item_desc).all()
                if not expense_desc == "select menu" and item_name == "select menu" and expense_type == "select menu":  
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and expense_type == "select menu": 
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc, item__contains=item_name).all()  
                if not expense_desc == "select menu" and not item_name == "select menu" and not expense_type == "select menu": 
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc, item__contains=item_name, expense_type__contains=expense_type).all() 
                print('item_desc =',expense_list)
            #print('desc_list =',desc_list)
            #print('expense_list =',expense_list)
            for expense in expense_list:
                total=round(total+float(expense.total_cost),2)
            print(total)
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        #print('expense_list',expense_list)
        return render (self.request,"accounting/expense.html",{"expense_list": expense_list, "desc_list":desc_list, "type_list":type_list,"item_name_list":item_name_list, "expense_type":expense_type,
                        "expense_desc":expense_desc, "item_name":item_name, "item_desc":item_desc, "item_desc_list":item_desc_list, "year_list":year_list, "operator":operator, 'total':total, 'year':year})
           
           
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
            vendor_list =  Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
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
                vendor = Vendor.objects.filter(id=vendor_id)
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
            vendor_list =  Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
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
                ven = Vendor.objects.filter(name=vendor)
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
                    ven = Vendor.objects.filter(name=vendor)
                    vendor_id = ven[0].id
                    print('vendor_id=',vendor_id)
                    Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc, sale_date=sale_date, item=item_name, item_desc=item_desc,
                                          quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=interval_save, reoccuring_interval=interval_time, operator=operator, last_update=timestamp)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, "desc_list":desc_list, "exp":exp, "vendor":vendor, "operator":operator})     
        
class InvoiceItemView(View):
    template_name = "invoice_item.html"
    success_url = reverse_lazy('accounting:invoice_item')
    def get(self, *args, **kwargs):
        try:
            contractor = -1
            client = -1
            item = -1
            charge = -1
            active = 'off'
            item_id = self.request.GET.get('item_id', -1)
            charge_id = self.request.GET.get('charge_id', -1)
            client_id = self.request.GET.get('client_id', -1)
            if item_id !=-1:
                item = Invoice_Item.objects.filter(id=item_id)
                item = item[0] 
                active = item.active
                if active=='on':
                    active = True
                contractor_id = item.contractor_id
                contractor = Contractors.objects.filter(id=contractor_id)
                contractor = contractor[0].name
                cust_id = item.client_id
                client = Clients.objects.filter(id=cust_id)
                client = client[0].name
            if charge_id !=-1:   
                charge = Charge_Code.objects.filter(id=charge_id)
                charge = charge[0].charge
                print('charge=',charge)
            if client_id !=-1:
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
            else:
                client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
                
            operator = str(self.request.user)
            if client_id !=-1:
                charge_list =  Charge_Code.objects.filter(client_id=client_id).values_list('charge', flat=True).distinct()
            else:
                charge_list =  Charge_Code.objects.order_by('charge').values_list('charge', flat=True).distinct()
                
            contractor_list =  Contractors.objects.order_by('name').values_list('name', flat=True).distinct()
            
            item_list = Invoice_Item.objects.all()
            print('item_list =',item_list)
            print('item_id =',item_id)
            print('charge_id =',charge_id)
            print('contractor=',contractor)
            print('client=',client)    
            print('item=', item)
            print("in GET")
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/invoice_item.html",{"charge_list": charge_list, "id":id, "contractor_list":contractor_list, 'client_list':client_list, 'item_list':item_list,
                        'charge':charge, 'client':client, "item":item, 'contractor':contractor, "operator":operator,'active':active,'item_id':item_id})

    def post(self, request, *args, **kwargs):
        contractor_list = []
        expense_list =[]
        desc_list = []
        item_id = -1
        exp =-1
        vendor =-1
        
        try: 
            print("in POST")
            timestamp = date.today()
            operator = str(self.request.user)
            charge_list =  Charge_Code.objects.order_by('charge').values_list('charge', flat=True).distinct()
            contractor_list =  Contractors.objects.order_by('name').values_list('name', flat=True).distinct()
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            item_list = Invoice_Item.objects.all()  
                        
            search = request.POST.get('search', -1)
            print('search =',search)
            item_id = request.POST.get('_item_id', -1 )
            print('item_id =',item_id)
            contractor = request.POST.get('_contractor', -1 )#service_provider
            print('contractor = ',contractor)
            service_type = request.POST.get('_service_type', -1)
            print('service_type = ',service_type)
            resource_type = request.POST.get('_res_type', -1)
            print('resource_type = ',resource_type)
            client = request.POST.get('_cust', -1)
            print('client =',client)
            charge = request.POST.get('_charge', -1)
            print('charge =',charge)
            item_desc = request.POST.get('_item_desc', -1)
            print('item_desc =',item_desc)
            cost_type = request.POST.get('_item_cost_type', -1)
            print('cost_type =',cost_type)
            quantity = request.POST.get('_quantity', -1)
            print('quantity =',quantity)
            rate = request.POST.get('_item_cost', -1)
            print('rate =',rate)
            total_cost = request.POST.get('_total_cost', -1)
            print('total_cost =',total_cost)
            item_date = request.POST.get('_item_date', -1)
            print('item_date =',item_date)
            invoice = request.POST.get('_invoice', -1)
            print('invoice =',invoice)
            active = request.POST.get('_active', False)
            print('active =',active)
            
            save_item = request.POST.get('_save', -1)
            print('save_item =',save_item)
            update_item = request.POST.get('_update', -1)
            print('update_exp =',update_item)
            del_item = request.POST.get('_delete', -1)
            print('del_item =',del_item)
            quantity = request.POST.get('_quantity', -1)
            print('quantity =',quantity)
            success = True
                       
            if active =='on':
                active_save = True
            else:
                active_save = False
                
                
            client_id = Clients.objects.filter(name=client).first()
            client_id = client_id.id
            contractor_id = Contractors.objects.filter(name=contractor).first()
            contractor_id = contractor_id.id
            charge_id = Charge_Code.objects.filter(charge=charge).first()
            charge_id = charge_id.id
            item = Invoice_Item.objects.all()
            item = item[0]
            
                                
            print('active_save=',active_save)
            if not del_item==-1:
                try:
                   #update item	
                    Invoice_Item.objects.filter(id=item_id).delete()
                    print('delete complete')
                    item=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
                    return HttpResponseRedirect(reverse('accounting:expenses'))
            elif not update_item==-1:
                #update item	
                print('client_id=',client_id)
                print('contractor_id=',contractor_id)
                print('charge_id=',charge_id)
                Invoice_Item.objects.filter(id=item_id).update(client_id=client_id,charge_id=charge_id, contractor_id=contractor_id,resource_type=resource_type,service_type=service_type, 
                                        cost_type=cost_type,item_date=item_date,item_desc=item_desc, rate=rate, quantity=quantity ,total=total_cost, active=active_save, last_update=timestamp)
                exp=-1
            elif not save_item==-1:
                if Invoice_Item.objects.filter(id=item_id).exists():
                    return render (self.request,"accounting/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'contractor':contractor, "operator":operator})
                else:
                   #save item	
                    print('client_id=',client_id)
                    print('contractor_id=',contractor_id)
                    print('charge_id=',charge_id)
                    Invoice_Item.objects.create(client_id=client_id,charge_id=charge_id, contractor_id=contractor_id, resource_type=resource_type,service_type=service_type, 
                                        cost_type=cost_type,item_date=item_date,item_desc=item_desc, rate=rate, quantity=quantity ,total=total_cost, active=active_save, last_update=timestamp)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return HttpResponseRedirect(reverse('accounting:invoice_item'))
                        
                        
                        
class Charge_codeView(View):
    template_name = "charge.html"
    success_url = reverse_lazy('accounting:charge_code')
    def get(self, *args, **kwargs):
        try:
            client = -1
            item = -1
            charge = -1
            charge_desc = -1
            item_id = self.request.GET.get('code_id', -1)
            client_id = self.request.GET.get('client_id', -1)
            if item_id !=-1:
                item = Charge_Code.objects.filter(id=item_id)
                item = item[0]
                print('start_date=',item.start_date)
            if client_id !=-1:
                client = Clients.objects.filter(id=client_id)
                client = client[0].name
                print('client=',client)
                
            operator = str(self.request.user)
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            charge_list =  Charge_Code.objects.all()
            print('charge_list = ',charge_list)
            print('item_id =',item_id)
            print('client_id =',client_id)
            print('item=', item)
            print("in GET")
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/charge_code.html",{'charge_list':charge_list,'client_list':client_list, "operator":operator,'item_id':item_id, 'item':item, 'client':client})

    def post(self, request, *args, **kwargs):
        contractor_list = []
        expense_list =[]
        desc_list = []
        item_id = -1
        exp =-1
        vendor =-1
        
        try: 
            print("in POST")
            timestamp = date.today()
            operator = str(self.request.user)
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            charge_list =  Charge_Code.objects.all()
            print('charge_list = ',charge_list)
            item_id = request.POST.get('_item_id', -1 )
            print('item_id =',item_id)
            charge_type = request.POST.get('_charge_type', -1)
            print('charge_type = ',charge_type)
            client = request.POST.get('_client', -1)
            print('client =',client)
            charge = request.POST.get('_charge_code', -1)
            print('charge =',charge)
            charge_desc = request.POST.get('_charge_desc', -1)
            print('charge_desc =',charge_desc)
            start_date = request.POST.get('_start_date', -1)
            print('start_date =',start_date)
            end_date = request.POST.get('_end_date', -1)
            print('end_date =',end_date)
            
            
            save_item = request.POST.get('_save', -1)
            print('save_item =',save_item)
            update_item = request.POST.get('_update', -1)
            print('update_exp =',update_item )
            del_item = request.POST.get('_delete', -1)
            print('del_item =',del_item)
            success = True
                       
            client_id = Clients.objects.filter(name=client).first()
            print('client_id=',client_id)
            client_id = client_id.id
            print('client_id=',client_id)
            item = Charge_Code.objects.filter(id=item_id)
            print('item=',item)
           
            if not del_item==-1:
                try:
                   #update item	
                    Charge_Code.objects.filter(id=item_id).delete()
                    print('delete complete')
                    item=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
                    return HttpResponseRedirect(reverse('accounting:charge_code'))
            elif not update_item==-1:
                #update item	
                Charge_Code.objects.filter(id=item_id).update(charge_type=charge_type, client_id=client_id, charge=charge, charge_desc=charge_desc, start_date=start_date, end_date=end_date,last_update=timestamp)
            elif not save_item==-1:
                if Charge_Code.objects.filter(charge=charge).exists():
                    return render (self.request,"accounting/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'contractor':contractor, "operator":operator})
                else:
                   #save item	
                    Charge_Code.objects.create(charge_type=charge_type, client_id=client_id, charge=charge, charge_desc=charge_desc, start_date=start_date, end_date=end_date,last_update=timestamp)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return HttpResponseRedirect(reverse('accounting:charge_code'))

        
def save_expenses_csv(delete):               
    #~~~~~~~~~~~Load vendor database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'C:\\SRC\\ATS\\accounting\\Expenses.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    # Vendor.objects.all().delete()
       
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for vendor, expense_type, expense_desc, sale_date, item_name, item_desc, quantity, item_cost, total_cost, interval_save, interval_time in reader:
        if vendor=='ï»¿N/A':
            vendor='N/A'
        print('vendor=',vendor)
        print('expense_type=',expense_type)
        print('expense_desc=',expense_desc)
        format_str = '%m/%d/%Y' # The format
        sale_date = datetime.datetime.strptime(sale_date, format_str)
        print('sale_date=',sale_date)
        
        
        print('item_name=',item_name)
        print('item_desc=',item_desc)
        print('quantity=',quantity)
        print('item_cost=',item_cost)
        print('total_cost=',total_cost)
        print('interval_save=',interval_save)
        print('interval_time=',interval_time)
        ven = Vendor.objects.filter(name=vendor)
        print('ven=',ven)
        vendor_id = ven[0].id
        print('vendor_id=',vendor_id)
        if interval_save=='FALSE':
            interval_save = False
        else:
            interval_save = True
        print('interval_save=',interval_save)
        Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc, sale_date=sale_date, item=item_name, item_desc=item_desc,
                                     quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=interval_save, reoccuring_interval=interval_time, operator=operator, last_update=timestamp)
                                     

class IncomeView(View):
  
    template_name = "income.html"
    success_url = reverse_lazy('accounting:income')
    def get(self, *args, **kwargs):
        try:
            income_id = self.request.GET.get('income_id', -1)
            invoice_id = self.request.GET.get('invoice_id', -1)
            client_id = self.request.GET.get('client_id', -1)
            desc_list=-1
            type_list=-1
            item_name_list=-1
            item_desc_list=-1
            total=0
            income_type =-1
            income_desc =-1
            invoice =-1
            operator = str(self.request.user)
            year = datetime.date.today().year
            print('year',year)
            if client_id !=-1:
                client_list =  Income.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                client = Clients.objects.filter(id=client_id).first()
                client = client[0]
                desc_list = Income.objects.filter(id=client_id).order_by('income_description').values_list('income_description', flat=True).distinct()
                type_list = Income.objects.filter(id=client_id).order_by('income_type').values_list('income_type', flat=True).distinct()
                years = Income.objects.filter(id=client_id).order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
            else:
                client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
                client = -1
                desc_list = Income.objects.order_by('income_description').values_list('income_description', flat=True).distinct()
                type_list = Income.objects.order_by('income_type').values_list('income_type', flat=True).distinct()
                years = Income.objects.order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
                
            if invoice_id !=-1:
                invoice = Invoices.objects.filter(id=invoice_id).first()
                invoice=invoice[0].invoice_desc
            
            
            year_list=[]
            for year1 in years:
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
            print("in GET")
            income_list = Income.objects.all()
            for income in income_list:
                total=round(total+float(income.total_cost),2)
            print(total)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/income.html",{"income_list":income_list, "desc_list":desc_list, "type_list":type_list, "client_list":client_list, "income_type":income_type,
                                    "income_desc":income_desc, "year_list":year_list, "operator":operator, "invoice":invoice, "total":total, "year":year})
    
    def post(self, request, *args, **kwargs):
        try: 
            #print("in POST")
            operator = str(self.request.user)
            type_list = []
            inv_list = []
            inv = []
            total=0
            search = request.POST.get('search', -1)
            print('search =',search)
            vendor = request.POST.get('_vendor', -1)
            income_type = request.POST.get('_inc_type', -1)
            print('income_type = ',income_type)
            income_desc = request.POST.get('_inc_desc', -1)
            print('income_desc =',income_desc)
            year_c = request.POST.get('_year', -1)
            if year_c ==-1:
                year_c = datetime.date.today().year
            print('year =',year_c)
            year = datetime.date.today().year
            desc_list = Income.objects.order_by('income_description').values_list('income_description', flat=True).distinct()
            type_list = Income.objects.order_by('income_type').values_list('income_type', flat=True).distinct()
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            years = Income.objects.order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
            year_list=[]
            for year1 in years:
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
            print("year_list",year_list) 
            print('year',year_c)
            success = True
            #income_list = Income.objects.all() 
            if not search ==-1:
                if  Income.objects.filter(vendor_id__icontains=search).exists():
                    income_list = Income.objects.filter(vendor_id__icontains=search).all()
                    print('search 1=',income_list)
                elif  Income.objects.filter(income_type__icontains=search).exists():
                    income_list = Income.objects.filter(income_type__icontains=search).all()
                    print('search 2=',income_list)
                elif Income.objects.filter(income_description__icontains=search).exists():
                    income_list = Income.objects.filter(income_description__icontains=search).all() 
                    print('search 3=',income_list)
                elif Income.objects.filter(item_cost__icontains=search).exists():
                    income_list = Income.objects.filter(item_cost__contains=search).all()
                    print('search 6=',income_list)
                elif Income.objects.filter(sale_date__contains=search).exists():
                    income_list = Income.objects.filter(invoice_date__contains=search).all()
                    print('esearch 7=',income_list)
            elif not income_type =="select menu": 
                if income_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    income_list = Income.objects.filter(income_type=income_type).all()
                if not income_desc == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    income_list = Income.objects.filter(income_type=income_type, income_description__contains=income_desc).all()  
                if not income_desc == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    income_list = Income.objects.filter(income_type=income_type, income_description__contains=income_desc, item__contains=item_name).all()  
                if not income_desc == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    income_list = Income.objects.filter(income_type=income_type, income_description__contains=income_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                print('income_type =',income_list)
            elif not income_desc =="select menu": 
                if income_type == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    income_list = Income.objects.filter(income_description=income_desc).all()
                if not income_type == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    income_list = Income.objects.filter(income_type=income_type, income_description__contains=income_desc).all()  
                if not income_type == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    income_list = Income.objects.filter(income_type=income_type, income_description__contains=income_desc, item__contains=item_name).all()  
                if not income_type == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    income_list = Income.objects.filter(income_type=income_type, income_description__contains=income_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                print('income_desc =',income_list)
            #print('desc_list =',desc_list)
            #print('income_list =',income_list)
            for income in income_list:
                total=round(total+float(income.total_cost),2)
            print(total)
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        #print('income_list',income_list)
        return render (self.request,"accounting/income.html",{"income_list":income_list, "desc_list":desc_list, "type_list":type_list, "client_list":client_list, "income_type":income_type,
                                    "income_desc":income_desc, "year_list":year_list, "operator":operator, "invoice":invoice, "total":total, "year":year})
           
           
class SaveIncomeView(View):
    template_name = "save_income.html"
    success_url = reverse_lazy('accounting:new_income')
    def get(self, *args, **kwargs):
        try:
            invoice = -1
            inc = -1
            interval = 'off'
            income_id = self.request.GET.get('income_id', -1)
            client_id = self.request.GET.get('client_id', -1)
            invoice_id = self.request.GET.get('invoice_id', -1)
            print('income_id =',income_id)
            print('invoice_id =',invoice_id)
            operator = str(self.request.user)
            print('inc=',inc)
            desc_list =  Income.objects.order_by('income_description').values_list('income_description', flat=True).distinct()
            invoice_list =  Invoices.objects.order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
            print('invoice_list =',invoice_list)
            if income_id !=-1:
                inc = Income.objects.filter(id=income.id).first
            if client_id !=-1:
                client_list =  Income.objects.filter(client_id=client_id).order_by('name').values_list('name', flat=True).distinct()
                client = Clients.objects.filter(id=client_id).first()
                client = client[0]
                years = Income.objects.filter(id=client_id).order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
            else:
                client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
                client = -1
                years = Income.objects.order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
            if invoice_id !=-1:
                invoice = Invoices.objects.filter(id=invoice_id)
                invoice = invoice[0].name
                print('invoice=',invoice)
            
            
            print('inc=', inc)
            print("in GET")
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/save_income.html",{"id":id, "inc":inc, 'invoice':invoice, "client_list":client_list, "invoice_list":invoice_list, 'desc_list':desc_list,"inc":inc, 'invoice':invoice, "client":client, "operator":operator})

    def post(self, request, *args, **kwargs):
        invoice_list = []
        income_list =[]
        desc_list = []
        inc =-1
        invoice =-1
        
        try: 
            print("in POST")
            timestamp = date.today()
            operator = str(self.request.user)
            inc_id = request.POST.get('e_id', -1)
            print('inc_id =',inc_id)
            income_list = Income.objects.all()
            desc_list =  Income.objects.order_by('income_description').values_list('income_description', flat=True).distinct()
            invoice_list =  Invoices.objects.order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
            if inc_id !=-1:
                inc = Income.objects.filter(id=inc_id).all()
            
            
            search = request.POST.get('search', -1)
            print('search =',search)
            invoice = request.POST.get('_invoice', -1)
            print('invoice = ',invoice)
            income_type = request.POST.get('_inc_type', -1)
            print('income_type = ',income_type)
            income_desc = request.POST.get('_inc_desc', -1)
            print('income_desc =',income_desc)
            total_charge = request.POST.get('_total_charge', -1)
            print('total_charge =',total_charge)
            sale_date = request.POST.get('_sale_date', -1)
            print('sale_date =',sale_date)
            invoice = request.POST.get('_invoice', -1)
            print('invoice =',invoice)
            client = request.POST.get('_client', -1)
            print('client =',invoice)
            
            
            save_inc = request.POST.get('_save', -1)
            print('save_inc =',save_inc)
            update_inc = request.POST.get('_update', -1)
            print('update_inc =',update_inc)
            del_inc = request.POST.get('_delete', -1)
            print('del_inc =',del_inc)
            success = True
            
            if not del_inc==-1:
                try:
                   #update item	
                    Income.objects.filter(id=income_id).delete()
                    print('delete complete')
                    inc=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
                    return HttpResponseRedirect(reverse('accounting:income'))
            elif not update_inc==-1:
                #update item	
                cli = Vendor.objects.filter(name=invoice)
                client_id = cli[0].id
                print('client_id=',client_id)
                Income.objects.filter(id=inc_id).update(client_id=client_id,invoice_id=invoice_id, income_type=income_type,income_description=income_desc,
                                       total=total_charge, operator=operator,last_update=timestamp)
                inc=-1
            elif not save_inc==-1:
                if Income.objects.filter(item=item_name).exists():
                    inc = Income.objects.filter(item=item_name).all()
                    return render (self.request,"accounting/save_income.html",{"income_list": income_list, "id":id, "invoice_list":invoice_list, 'desc_list':desc_list,"inc":inc, 'invoice':invoice, "operator":operator})
                else:
                   #save item	
                    cli = Vendor.objects.filter(name=invoice)
                    client_id = cli[0].id
                    print('client_id=',client_id)
                    Income.objects.create(client_id=client_id, income_type=income_type, income_description=income_desc, sale_date=sale_date, item=item_name, item_desc=item_desc,
                                          quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_income=interval_save, reoccuring_interval=interval_time, operator=operator, last_update=timestamp)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounting/save_income.html",{"income_list": income_list, "id":id, "inc":inc, 'invoicd':invoice, "invoice_list":invoice_list, 'desc_list':desc_list,"inc":inc, 'invoice':invoice, "client":client, "operator":operator})           