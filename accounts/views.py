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
from accounts.models import Expenses, Invoice_Item, Charge_Code, Invoice
from dashboard.models import Income_report
from vendor.models import Vendor
from contractors.models import Contractors
from django.views import View
import datetime
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from ATS.overhead import Equations
from re import search

class UserLogin(View):
    template_name = "user_login.html"
    success_url = reverse_lazy('client:login')
        
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user)
        
        except IOError as e:
           print('error = ',e) 
        return render(request, 'client/user_login.html', {})
 
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    redirect_to = resolve_url(LOGIN_REDIRECT_URL)
                    print('redirect =',LOGIN_REDIRECT_URL)
                    return render(request,'client/index.html')
                else:
                    return render(request, 'client/user_login.html', {'message':'Login Failed!!'})
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
            return render(request, 'client/user_login.html', {'message':'Login Failed!!'})
        else:
            return render(request, 'client/user_login.html', {})


class ExpensesView(View):
  
    template_name = "expense.html"
    success_url = reverse_lazy('accounts:expenses')
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user)
            contSuccess = 0
            year = datetime.date.today().year
            print('year=',year)
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
                year1 = str(year1)
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
            print("in GET")
            
            expense_list = Expenses.objects.filter(sale_date__icontains=year).all()
            for expense in expense_list:
                total=round(total+float(expense.total_cost),2)
            print(total)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/expense.html",{"expense_list": expense_list, "desc_list":desc_list, "type_list":type_list,"item_name_list":item_name_list, "expense_type":expense_type,
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
                year = datetime.date.today().year
            else:
                year=year_c
            desc_list = Expenses.objects.order_by('expense_description').values_list('expense_description', flat=True).distinct()
            type_list = Expenses.objects.order_by('expense_type').values_list('expense_type', flat=True).distinct()
            item_name_list = Expenses.objects.order_by('item').values_list('item', flat=True).distinct()
            item_desc_list = Expenses.objects.order_by('item_desc').values_list('item_desc', flat=True).distinct()
            years = Expenses.objects.order_by('sale_date').values_list('sale_date', flat=True).distinct()
            if year_c != 'all years':
                expense_list = Expenses.objects.filter(sale_date__icontains=year).all()
            else:
                expense_list = Expenses.objects.all()
                
            year_list=[]
            for year1 in years:
                year1 = str(year1)
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
            print("year_list",year_list) 
            print('year_c=',year_c)
            print('year=',year)
            success = True
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
                elif Expenses.objects.filter(year_c__contains=search).exists():
                    expense_list = Expenses.objects.filter(year_c__contains=search).all()
                    print('esearch 7=',expense_list)
                  
            elif not year_c == 'all years': 
                if not year_c == 'all years' and expense_type == "select menu"  and expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(sale_date__icontains=year).all()
                elif  not year_c == 'all years' and not expense_type == "select menu"  and expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(sale_date__icontains=year, expense_type=expense_type).all()
                elif  not year_c == 'all years' and not expense_type == "select menu"   and not expense_desc == "select menu" and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(sale_date__icontains=year, expense_type=expense_type, expense_description__contains=expense_desc).all()  
                elif  not year_c == 'all years' and not expense_type == "select menu"   and not expense_desc == "select menu" and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(sale_date__icontains=year, expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                elif  not year_c == 'all years' and not expense_type == "select menu"   and not expense_desc == "select menu" and not item_name == "select menu" and not item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(sale_date__icontains=year, expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                print('expense_type =',expense_list)
            elif not expense_type =="select menu": 
                if expense_desc == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(expense_type=expense_type).all()
                elif not expense_desc == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc).all()  
                elif not expense_desc == "select menu" and not expense_type == "select menu"   and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                elif not expense_desc == "select menu" and not expense_type == "select menu"   and not item_name == "select menu" and not item_desc == "select menu" and not year_c == 'all years': 
                    expense_list = Expenses.objects.filter(sale_date__icontains=year_c, expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                print('expense_type =',expense_list)
            elif not expense_desc =="select menu": 
                if expense_type == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(expense_description=expense_desc).all()
                elif not expense_type == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc).all()  
                elif not expense_type == "select menu" and not expense_type == "select menu"   and not item_name == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                elif not expense_type == "select menu" and not item_name == "select menu" and not item_desc == "select menu" and not year_c == 'all years': 
                    expense_list = Expenses.objects.filter(sale_date__icontains=year_c, expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all() 
                elprint('expense_desc =',expense_list)
            elif not item_name =="select menu": 
                if item_name == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(item=item_name).all()
                elif not item_name == "select menu" and not expense_type == "select menu"   and expense_desc == "select menu" and item_desc == "select menu":  
                    expense_list = Expenses.objects.filter(item=item_name, expense_description__contains=expense_desc).all()  
                elif not item_name == "select menu" and not expense_type == "select menu"   and not expense_desc == "select menu" and item_desc == "select menu": 
                    expense_list = Expenses.objects.filter(expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name).all()  
                elif not item_name == "select menu" and not expense_type == "select menu"   and not expense_desc == "select menu" and not item_desc == "select menu"  and not year_c == 'all years': 
                    expense_list = Expenses.objects.filter(sale_date__icontains=year_c, expense_type=expense_type, expense_description__contains=expense_desc, item__contains=item_name, item_desc__contains=item_desc).all()
                print('item_name =',expense_list)
            elif not item_desc =="select menu": 
                if expense_desc == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and item_desc == "select menu" :
                    expense_list = Expenses.objects.filter(item_desc=item_desc).all()
                elif not expense_desc == "select menu" and not expense_type == "select menu"   and item_name == "select menu" and expense_type == "select menu":  
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc).all()  
                elif not expense_desc == "select menu" and not expense_type == "select menu"   and not item_name == "select menu" and expense_type == "select menu": 
                    expense_list = Expenses.objects.filter(item_desc=item_desc, expense_description__contains=expense_desc, item__contains=item_name).all()  
                elif not expense_desc == "select menu" and not expense_type == "select menu"   and not item_name == "select menu" and not expense_type == "select menu"  and not year_c == 'all years': 
                    expense_list = Expenses.objects.filter(sale_date__icontains=year_c, item_desc=item_desc, expense_description__contains=expense_desc, item__contains=item_name, expense_type__contains=expense_type).all() 
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
        return render (self.request,"accounts/expense.html",{"expense_list": expense_list, "desc_list":desc_list, "type_list":type_list,"item_name_list":item_name_list, "expense_type":expense_type,
                        "expense_desc":expense_desc, "item_name":item_name, "item_desc":item_desc, "item_desc_list":item_desc_list, "year_list":year_list, "operator":operator, 'total':total, 'year':year})
           
           
class SaveExpensesView(View):
    template_name = "save_expenses.html"
    success_url = reverse_lazy('accounts:new_expense')
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
        return render (self.request,"accounts/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'vendor':vendor, "operator":operator,'interval':interval})

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
            if exp_id !=-1 and exp_id != '':
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
            if not del_exp==-1 and (exp_id !=-1 and exp_id != ''):
                try:
                   #update item	
                    Expenses.objects.filter(id=expense_id).delete()
                    print('delete complete')
                    exp=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
                    return HttpResponseRedirect(reverse('accounts:expenses'))
            elif not update_exp==-1 and (exp_id !=-1 and exp_id != ''):
                #update item	
                ven = Vendor.objects.filter(name=vendor)
                vendor_id = ven[0].id
                print('vendor_id=',vendor_id)
                Expenses.objects.filter(id=exp_id).update(vendor_id=vendor_id,expense_type=expense_type,expense_description=expense_desc,sale_date=sale_date,item=item_name,item_desc=item_desc,
                                        quantity=quantity,item_cost=item_cost,total_cost=total_cost,reoccuuring_expenses=interval_save,reoccuring_interval=interval_time,operator=operator,last_update=timestamp)
                exp=-1
            elif not save_exp==-1 or (exp_id !=-1 and exp_id != ''):
                if Expenses.objects.filter(item=item_name).exists():
                    exp = Expenses.objects.filter(item=item_name).all()
                    return render (self.request,"accounts/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'vendor':vendor, "operator":operator})
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
        return render (self.request,"accounts/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, "desc_list":desc_list, "exp":exp, "vendor":vendor, "operator":operator})     
        

class InvoiceItemView(View):
    template_name = "invoice_item.html"
    success_url = reverse_lazy('accounts:invoice_item')
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
                date= item.item_date
                print('date=',date)
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
        return render (self.request,"accounts/invoice_item.html",{"charge_list": charge_list, "id":id, "contractor_list":contractor_list, 'client_list':client_list, 'item_list':item_list,
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
            invoice_id = request.POST.get('_invoice_id', -1)
            print('invoice_id  =',invoice_id )
            
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
            if item:
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
                    return HttpResponseRedirect(reverse('accounts:expenses'))
            elif not update_item==-1:
                #update item	
                print('client_id=',client_id)
                print('contractor_id=',contractor_id)
                print('charge_id=',charge_id)
                Invoice_Item.objects.filter(id=item_id).update(client_id=client_id,charge_id=charge_id, contractor_id=contractor_id,resource_type=resource_type,service_type=service_type, invoice_id=invoice_id, 
                                        cost_type=cost_type,item_date=item_date,item_desc=item_desc, rate=rate, quantity=quantity ,total=total_cost, active=active_save, last_update=timestamp)
                exp=-1
            elif not save_item==-1:
                if Invoice_Item.objects.filter(id=item_id).exists():
                    return render (self.request,"accounts/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'contractor':contractor, "operator":operator})
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
        return HttpResponseRedirect(reverse('accounts:invoice_item'))

class SearchInvoiceView(View):
    template_name = "invoice.html"
    success_url = reverse_lazy('accounts:invoice')
    def get(self, *args, **kwargs):
        try:
            
            invoice_list =[]
            invoice = -1
            client_list = -1
            client = -1
            client_id = -1
            desc_list = -1
            id_list =-1
            year =-1
            paid =-1
            timestamp = date.today()
            operator = str(self.request.user)
            invoice_list = Invoice.objects.all()
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            desc_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            years = Invoice.objects.order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
            print('years=',years)
            year_list=[]
            for year1 in years:
                year1 = str(year1)
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
                      
            print("in GET")
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/invoice.html",{"invoice_list": invoice_list, "client_list":client_list, "desc_list":desc_list, "id_list":id_list, "year_list":year_list,
                        "invoice":invoice, 'client':client, "year":year, "paid":paid})

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
            invoice_list =[]
            invoice = -1
            client_list = -1
            client = -1
            client_id = -1
            desc_list = -1
            id_list =-1
            year =-1
            paid =-1
            save_paid = "No"
            timestamp = date.today()
            operator = str(self.request.user)
            invoice_list = Invoice.objects.all()
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            desc_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            years = Invoice.objects.order_by('invoice_date').values_list('invoice_date', flat=True).distinct()
            print('years=',years)
            year_list=[]
            for year1 in years:
                year1 = str(year1)
                dt = year1.split('-')
                year_list.append(dt[0])
            year_list = list(OrderedDict.fromkeys(year_list))
                        
            search = request.POST.get('search', -1)
            print('search =',search)
            invoice_id = request.POST.get('_invoice_id', -1 )
            print('invoice_id =',invoice_id)
            invoice_desc = request.POST.get('_invoice_desc', -1 )
            print('invoice_desc =',invoice_desc)
            client = request.POST.get('_client', -1)
            print('client =',client)
            if client != 'Search by Client':
                client_id = Clients.objects.filter(name=client).all()
                print('client_id =',client_id)
                client_id = client_id[0].id
            print('client_id =',client_id)
            paid = request.POST.get('_paid', -1 )#service_provider
            print('paid  = ',paid )
            if paid =='Paid':
                save_paid=True
            else:
                save_paid=False
            print('save_paid  = ',save_paid )    
            year = request.POST.get('_year', -1)
            print('year = ',year)
             
            clear = request.POST.get('_clear', -1)
            print('clear =',clear)
            success = True
                 
            if not clear==-1:
                return HttpResponseRedirect(reverse('accounts:invoice'))
            
            
            if not search ==-1:
                if  Invoice.objects.filter(id__icontains=search).exists():
                    invoice_list = Invoice.objects.filter(client_id__icontains=search).all()
                    print('search 1=',invoice_list)
                elif  Invoice.objects.filter(staff_id__icontains=search).exists():
                    invoice_list = Invoice.objects.filter(expense_type__icontains=search).all()
                    print('search 2=',invoice_list)
                elif Invoice.objects.filter(invoice_desc__icontains=search).exists():
                    invoice_list = Invoice.objects.filter(expense_description__icontains=search).all() 
                    print('search 3=',invoice_list)
                elif Invoice.objects.filter(charge_code__icontains=search).exists():
                    invoice_list = Invoice.objects.filter(item__icontains=search).all()
                    print('search 4=',invoice_list)
                elif Invoice.objects.filter(paid__icontains=search).exists():
                    invoice_list = Invoice.objects.filter(item_desc__icontains=search).all()
                    print('search 5=',invoice_list)
                elif Invoice.objects.filter(invoice_date__icontains=search).exists():
                    invoice_list = Invoice.objects.filter(item_cost__contains=search).all()
                    print('search 6=',invoice_list)
                elif Invoice.objects.filter(payment_date__contains=search).exists():
                    invoice_list = Invoice.objects.filter(sale_date__contains=search).all()
                    print('search 7=',invoice_list)
                elif Invoice.objects.filter(total__contains=search).exists():
                    invoice_list = Invoice.objects.filter(sale_date__contains=search).all()
                    print('search 8=',invoice_list)
                elif Invoice.objects.filter(last_update__contains=search).exists():
                    invoice_list = Invoice.objects.filter(sale_date__contains=search).all()
                    print('search 9=',invoice_list)
            elif not invoice_id =="select": 
                invoice_list = Invoice.objects.filter(id=invoice_id).all()
            elif not invoice_desc =="Search by Title": 
                if not invoice_desc == "Search by Title" and client == "Search by Client" and paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc).all()
                if not invoice_desc == "Search by Title" and not client == "Search by Client" and paid == "Search by paid or unpaid" and year =='All years': 
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id).all()  
                if not invoice_desc == "Search by Title" and not client == "Search by Client" and not paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid).all()  
                if not invoice_desc == "Search by Title" and  not client == "Search by Client" and  not paid == "Search by paid or unpaid" and not year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid, invoice_date__contains=year).all() 
            elif not client =="Search by Client": 
                if not client == "Search by Client" and invoice_desc == "Search by Title" and paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(client_id__contains=client_id).all()
                if not invoice_desc == "Search by Title" and not client == "Search by Client" and paid == "Search by paid or unpaid" and year =='All years': 
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id).all()  
                if not invoice_desc == "Search by Title" and not client == "Search by Client" and not paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid).all()  
                if not invoice_desc == "Search by Title" and  not client == "Search by Client" and  not paid == "Search by paid or unpaid" and not year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid, invoice_date__contains=year).all()     
            elif not year =="All years": 
                if  client == "Search by Client" and invoice_desc == "Search by Title" and paid == "Search by paid or unpaid" and not year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_date__contains=year).all()
                if not invoice_desc == "Search by Title" and not client == "Search by Client" and paid == "Search by paid or unpaid" and not year =='All years': 
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, invoice_date__contains=year).all()  
                if not invoice_desc == "Search by Title" and not client == "Search by Client" and not paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid).all()  
                if not invoice_desc == "Search by Title" and  not client == "Search by Client" and  not paid == "Search by paid or unpaid" and not year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid, invoice_date__contains=year).all()   
            elif not paid == "Search by paid or unpaid": 
                if invoice_desc == "Search by Title" and client == "Search by Client" and not paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(paid=save_paid).all()
                if invoice_desc == "Search by Title" and not client == "Search by Client" and  not paid == "Search by paid or unpaid" and year =='All years': 
                    invoice_list = Invoice.objects.filter(paid__contains=save_paid, client_id__contains=client_id).all()  
                if invoice_desc == "Search by Title" and not client == "Search by Client" and not paid == "Search by paid or unpaid" and year =='All years':
                    invoice_list = Invoice.objects.filter(paid__contains=save_paid, client_id__contains=client_id, invoice_desc=invoice_desc).all()  
                if not invoice_desc == "Search by Title" and  not client == "Search by Client" and  not paid == "Search by paid or unpaid" and not year =='All years':
                    invoice_list = Invoice.objects.filter(invoice_desc=invoice_desc, client_id__contains=client_id, paid__contains=save_paid, invoice_date__contains=year).all()
                    
            print('invoice_list =',invoice_list)
            print('paid =',paid)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/invoice.html",{"invoice_list": invoice_list, "client_list":client_list, "desc_list":desc_list, "id_list":id_list, "year_list":year_list,
                        "invoice":invoice, 'client':client, "year":year, "paid":paid})                       

class CreateInvoiceView(View):
    template_name = "create_invoice.html"
    success_url = reverse_lazy('accounts:new_invoice')
    def get(self, *args, **kwargs):
        try:
            contractor = -1
            client = -1
            invoice = -1
            client_id = -1
            invoice_id_list =  [] 
            invoice_list = []
            invoice_item_list = []
            invoice = -1
            invoice_item = -1
            total = -1
            charge_code = -1
            operator = str(self.request.user)
            invoice_id = self.request.GET.get('invoice_id', -1)
            item_id = self.request.GET.get('item_id', -1)
            active = self.request.GET.get('active', -1)
            item_invoice = self.request.GET.get('item_invoice', -1)
            client_list =  Clients.objects.order_by('name').values_list('name', flat=True).distinct()
            total=0
            
            if invoice_id !=-1:
                invoice = Invoice.objects.filter(id=invoice_id)
                invoice = invoice[0] 
                item = Invoice_Item.objects.filter(id=item_id)
                item = item[0] 
                item_desc = item.item_desc
                item_date = item.item_date
                print('item_date=',item_date)
                resource_type = item.resource_type
                contractor_id = item.contractor_id
                client_id = item.client_id
                client = Clients.objects.filter(id=client_id)
                client = client[0].name
                Invoice_Item.objects.filter(id=item_id).update(active=active,invoice_id=item_invoice)# Update Invoice_Item
                # Add travel costs to Expenses if required
                print('resource_type.upper()=',resource_type.upper())
                print(search(resource_type.upper(),'SITE'))
                if search('SITE', resource_type.upper()) or search('SITE', item_desc.upper()):
                    travel_rate = 0.545
                    get_distance = Equations(client_id,contractor_id)
                    distance = get_distance.travel_distance()
                    print('distance =',distance)
                    expense_type = 'Travel Expenses'
                    expense_description = 'Travel to ' + client
                    item_desc = 'Travel Distance = ', round(distance, 2)
                    exp_item = 'Travel'
                    quantity = 1
                    item_cost =  round(distance * travel_rate, 3)
                    total_cost = item_cost
                    if Expenses.objects.filter(expense_type=expense_type, item=exp_item, sale_date=item_date, vendor_id=contractor_id).exists():
                        print('expense exists. update existing')
                        if active==False:
                            Expenses.objects.filter(expense_type=expense_type, item=exp_item, sale_date=item_date, vendor_id=contractor_id).delete()
                        else:
                            Expenses.objects.filter(expense_type=expense_type, item=exp_item, sale_date=item_date, vendor_id=contractor_id).update(expense_description=expense_description,item_desc=item_desc,quantity=quantity,item_cost=item_cost,total_cost=total_cost)
                    else:
                        print('expense does not exist. create new')
                        Expenses.objects.create(expense_description=expense_description,expense_type=expense_type, item=exp_item, sale_date=item_date, vendor_id=contractor_id, item_desc=item_desc,quantity=quantity,item_cost=item_cost,total_cost=total_cost)
                        
                    
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_id_list =  Invoice.objects.filter(id=client_id).order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
                invoice_item_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=0).all()
                print('invoice_item_list =',invoice_item_list)
                invoice_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                print('invoice_list =',invoice_list)
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                invoice = Invoice.objects.filter(client_id=client_id, id=invoice_id).all()
                if invoice:
                    invoice=invoice[0]
                total=0
                for subtotal in invoice_item:
                    total=round(total+float(subtotal.total),2)
                    print(total)
                
                                    
            print('active =',active)
            print('client_list =',client_list)
            print('invoice_list =',invoice_list)
            print('invoice_list =',invoice_list)
            print('invoice_id_list =',invoice_id_list)
            print('invoice_id =',invoice_id)
            print('client=',client)    
            print('invoice=', invoice)
            print("in GET")
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/create_invoice.html",{"invoice_id_list": invoice_id_list, 'client_list':client_list, 'invoice_list':invoice_list, 'invoice_item_list':invoice_item_list,
                        'charge_code':charge_code, 'invoice':invoice, 'client':client, "invoice_item":invoice_item, "operator":operator,'invoice_id':invoice_id, 'total':total, 'client':client})

    def post(self, request, *args, **kwargs):
        try: 
            contractor = -1
            client = -1
            invoice = -1
            invoice_id = -1
            client_id = -1
            invoice_id_list =  [] 
            invoice_list = []
            invoice_item_list = []
            client_list = []
            invoice = -1
            invoice_item = -1
            total = -1
            
            charge_code = -1
            paid = False            
            print("in POST")
            timestamp = date.today()
            operator = str(self.request.user)
            
            invoice_id = request.POST.get('_invoice_id',-1)
            print('invoice_id=',invoice_id)
            client = request.POST.get('_client', -1)
            print('client =',client)
                      
            
            invoice_desc = request.POST.get('_invoice_desc',-1)
            print('invoice_desc =',invoice_desc)
            invoice_charge = request.POST.get('_invoice_charge',-1)
            print('invoice_charge =',invoice_charge)
            charge_code = invoice_charge
            invoice_date = request.POST.get('_invoice_date',-1)
            print('invoice_date =',invoice_date)
            if charge_code =="":
                split_charge = invoice_date.split("-")
                print('split_charge =',split_charge)
                charge_code = split_charge[1] + split_charge[2] + split_charge[0]
                print('charge_code =',charge_code)
            
            invoice = request.POST.get('_invoice',-1)
            print('invoice =',invoice)
            active = request.POST.get('_active', False)
            print('active =',active)
            
            save_invoice = request.POST.get('_save',-1)
            print('save_invoice =',save_invoice)
            update_invoice = request.POST.get('_update',-1)
            print('update_exp =',update_invoice)
            del_invoice = request.POST.get('_delete',-1)
            print('del_invoice =',del_invoice)
            clear_invoice = request.POST.get('_clear',-1)
            print('clear_invoice =',clear_invoice)
           

            quantity = request.POST.get('_quantity',-1)
            print('quantity =',quantity)
            success = True
            
            print('invoice_id=',invoice_id)          
            if  invoice_id :
                invoice = Invoice.objects.filter(id=invoice_id)
                invoice = invoice[0] 
                invoice_date = invoice.invoice_date
                print('invoice-',invoice)
                client_id = invoice.client_id
                client = Clients.objects.filter(id=client_id)
                client = client[0].name
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_id_list =  Invoice.objects.filter(id=client_id).order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
                invoice_item_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=0).all()
                print('invoice_item_list =',invoice_item_list)
                invoice_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                print('invoice_list =',invoice_list)
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                invoice = Invoice.objects.filter(client_id=client_id, id=invoice_id).all()
                staff_id=self.request.user.id
                if invoice:
                    invoice=invoice[0]
                total=0
                for subtotal in invoice_item:
                    total=round(total+float(subtotal.total),2)
                    print(total)
                    
            else:
                print('client=',client)
                client_id = Clients.objects.filter(name=client).first()
                client_id = client_id.id
                print('client_id=',client_id)
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, active=True).all()
                staff_id=self.request.user.id
            
            print('client_id =',client_id)
            print('staff_id =',staff_id)
            print('active =',active)
            print('client_list =',client_list)
            print('invoice_list =',invoice_list)
            print('invoice_id_list =',invoice_id_list)
            print('invoice_id =',invoice_id)
            print('client=',client)    
            print('invoice=', invoice)
            
                                
            if not del_invoice==-1:
                try:
                   #reset items	
                    invoice_items = Invoice_item.objects.filter(invoice_id=invoice_id).all()
                    for item in invoice_items:
                        Invoice_Item.objects.filter(id=item.id).update(active=True,invoice_id=0)# Reset Invoice_Item
                    #delete invoice    
                    Invoice.objects.filter(id=invoice_id).delete()
                    print('delete complete')
                    invoice=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
              
            elif not clear_invoice==-1:
                try:
                   #reset items	
                    invoice_items = Invoice_Item.objects.filter(invoice_id=invoice_id).all()
                    for item in invoice_items:
                        Invoice_Item.objects.filter(id=item.id).update(active=True,invoice_id=0)# Reset Invoice_Item
                        print('item ',item.id, ' cleared')
                except IOError as e:
                    print ("Events Save Failure ", e)
                    

            elif not update_invoice==-1:
                #update invoice	
                print('client_id=',client_id)
                Invoice.objects.filter(id=invoice_id).update(client_id=client_id,staff_id=staff_id, invoice_desc=invoice_desc, charge_code=charge_code, paid=paid, invoice_date=invoice_date, last_update=timestamp)
                return HttpResponseRedirect(reverse('accounts:invoice'))
            elif not save_invoice==-1 :
                if Invoice.objects.filter(invoice_desc=invoice_desc, charge_code=charge_code, invoice_date=invoice_date).exists():
                    invoice_id = Invoice.objects.filter(client_id=client_id,staff_id=staff_id, invoice_desc=invoice_desc, charge_code=charge_code, paid=paid, invoice_date=invoice_date, last_update=timestamp).first()  
                    invoice_id = invoice_id.id
                    
                else:
                    print('client_id=',client_id)
                    Invoice.objects.create(client_id=client_id,staff_id=staff_id, invoice_desc=invoice_desc, charge_code=charge_code, paid=paid, invoice_date=invoice_date, last_update=timestamp)
                    invoice_id = Invoice.objects.filter(client_id=client_id,staff_id=staff_id, invoice_desc=invoice_desc, charge_code=charge_code, paid=paid, invoice_date=invoice_date, last_update=timestamp).first()  
                    invoice_id = invoice_id.id
                    
                
                
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_id_list =  Invoice.objects.filter(id=client_id).order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
                invoice_item_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=0).all()
                print('invoice_item_list =',invoice_item_list)
                invoice_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                print('invoice_list =',invoice_list)
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                invoice = Invoice.objects.filter(client_id=client_id, id=invoice_id).all()
                if invoice:
                    invoice=invoice[0]
                total=0
                for subtotal in invoice_item:
                    total=round(total+float(subtotal.total),2)
                    print(total)
                print('client_list=',client_list)
                print('invoice_id_list=',invoice_id_list)
                print('invoice_list=',invoice_list)
                print('invoice_item_list=',invoice_item_list)
                print('invoice=',invoice.id)
                
                                 
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/create_invoice.html",{"invoice_id_list": invoice_id_list, 'client_list':client_list, 'invoice_list':invoice_list, 'invoice_item_list':invoice_item_list,
                        'charge_code':charge_code, 'invoice':invoice, 'client':client, "invoice_item":invoice_item, "operator":operator,'invoice_id':invoice_id, 'total':total, 'client':client})
        
class ReconsileInvoiceView(View):
    template_name = "reconsile_invoice.html"
    success_url = reverse_lazy('accounts:invoice_update')
    def get(self, *args, **kwargs):
        try:
            invoice_item = -1
            client = -1
            invoice = -1
            charge = -1
            client_list = -1
            active = 'off'
            invoice_id_list = -1
            invoice_item_list = []
            invoice_list = []
            total=0
            paid = 'off'
            
            timestamp = date.today()
            operator = str(self.request.user)
            invoice_id = self.request.GET.get('invoice_id', -1)
            
            if invoice_id !=-1:
                invoice = Invoice.objects.filter(id=invoice_id)
                invoice = invoice[0] 
                charge_code = invoice.charge_code
                client_id = invoice.client_id
                client = Clients.objects.filter(id=client_id)
                client = client[0].name
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_id_list =  Invoice.objects.filter(id=client_id).order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
                invoice_item_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=0).all()
                print('invoice_item_list =',invoice_item_list)
                invoice_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                print('invoice_list =',invoice_list)
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                invoice = Invoice.objects.filter(client_id=client_id, id=invoice_id).all()
                if invoice:
                    invoice=invoice[0]
                    this_date = invoice.invoice_date
                    paid=invoice.paid
                    if paid == True:
                        save_paid = 'on'
                    else:
                        save_paid = 'off'
                total=0
                for subtotal in invoice_item:
                    total=round(total+float(subtotal.total),2)
                    print(total)
                print('this_date=',this_date)
                print('paid=', paid)
                print('save_paid=', save_paid)
                
                                    
            print('active =',active)
            print('client_list =',client_list)
            print('invoice_list =',invoice_list)
            print('invoice_item_list=',invoice_item_list)
            print('invoice_id_list =',invoice_id_list)
            print('invoice_id =',invoice_id)
            print('client=',client)    
            print('invoice=', invoice)
            print("in GET")
            
            
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/reconsile_invoice.html",{"invoice_id_list": invoice_id_list, 'client_list':client_list, 'invoice_list':invoice_list, 'invoice_item_list':invoice_item_list,
                        'invoice':invoice, 'client':client, "invoice_item":invoice_item, "operator":operator,'invoice_id':invoice_id, 'total':total, 'client':client, 'paid':save_paid, 'this_date':this_date})

    def post(self, request, *args, **kwargs):
        contractor_list = []
        expense_list =[]
        desc_list = []
        invoice_id = -1
        exp =-1
        vendor =-1
        
        try: 
            client = -1
            invoice = -1
            invoice_id = -1
            client_id = -1
            invoice_id_list =  [] 
            invoice_list = []
            invoice_item_list = []
            client_list = []
            invoice = -1
            invoice_item = -1
            total = -1
            
            charge_code = -1
            print("in POST")
            timestamp = date.today()
            operator = str(self.request.user)
            
            invoice_id = request.POST.get('_invoice_id',-1)
            print('invoice_id=',invoice_id)
            client = request.POST.get('_client', -1)
            print('client =',client)
            client_id = Clients.objects.filter(name=client).all()
            print('client_id =',client_id)
            client_id = client[0]
            print('client_id =',client_id)
            
            
            invoice_desc = request.POST.get('_invoice_desc',-1)
            print('invoice_desc =',invoice_desc)
            invoice_charge = request.POST.get('_invoice_charge',-1)
            print('invoice_charge =',invoice_charge)
            charge_code = invoice_charge
            if charge_code =="":
                split_charge = invoice_date.split("-")
                print('split_charge =',split_charge)
                charge_code = split_charge[1] + split_charge[2] + split_charge[0]
                print('charge_code =',charge_code)
            invoice = request.POST.get('_invoice',-1)
            print('invoice =',invoice)
            active = request.POST.get('_active', False)
            print('active =',active)
            
            paid = request.POST.get('_paid', -1)
            print('paid =',paid)
            if paid=='on':
                save_paid = True
            else:
                save_paid = False
            
            save_invoice = request.POST.get('_save',-1)
            print('save_invoice =',save_invoice)
            update_invoice = request.POST.get('_update',-1)
            print('update_exp =',update_invoice)
            del_invoice = request.POST.get('_delete',-1)
            print('del_invoice =',del_invoice)
            clear_invoice = request.POST.get('_clear',-1)
            print('clear_invoice =',clear_invoice)
           

            quantity = request.POST.get('_quantity',-1)
            print('quantity =',quantity)
            success = True
            
            print('invoice_id=',invoice_id)          
            if  invoice_id :
                invoice = Invoice.objects.filter(id=invoice_id)
                invoice = invoice[0] 
                print('invoice-',invoice)
                client_id = invoice.client_id
                client = Clients.objects.filter(id=client_id)
                client = client[0].name
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_id_list =  Invoice.objects.filter(id=client_id).order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
                invoice_item_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=0).all()
                print('invoice_item_list =',invoice_item_list)
                invoice_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                print('invoice_list =',invoice_list)
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                invoice = Invoice.objects.filter(client_id=client_id, id=invoice_id).all()
                staff_id=self.request.user.id
                if invoice:
                    invoice=invoice[0]
                    this_date = invoice.invoice_date
                total=0
                for subtotal in invoice_item:
                    total=round(total+float(subtotal.total),2)
                    print(total)
                    
            else:
                print('client=',client)
                client_id = Clients.objects.filter(name=client).first()
                client_id = client_id.id
                print('client_id=',client_id)
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, active=True).all()
                staff_id=self.request.user.id
            
            print('staff_id =',staff_id)
            print('active =',active)
            print('client_list =',client_list)
            print('invoice_list =',invoice_list)
            print('invoice_id_list =',invoice_id_list)
            print('invoice_id =',invoice_id)
            print('client=',client)    
            print('invoice=', invoice)
            
                                
            if not del_invoice==-1:
                try:
                   #reset items	
                    invoice_items = Invoice_Item.objects.filter(invoice_id=invoice_id).all()
                    for item in invoice_items:
                        Invoice_Item.objects.filter(id=item.id).update(active=True,invoice_id=0)# Reset Invoice_Item
                        print('item ',item.id, ' cleared')
                    #delete invoice    
                    Invoice.objects.filter(id=invoice_id).delete()
                    print('delete complete')
                    invoice=-1
                except IOError as e:
                    print ("Events Save Failure ", e)
              
            elif not clear_invoice==-1:
                try:
                   #reset items	
                    invoice_items = Invoice_Item.objects.filter(invoice_id=invoice_id).all()
                    for item in invoice_items:
                        Invoice_Item.objects.filter(id=item.id).update(active=True,invoice_id=0)# Reset Invoice_Item
                        print('item ',item.id, ' cleared')
                except IOError as e:
                    print ("Events Save Failure ", e)
                    

            elif not update_invoice==-1:
                #update invoice	
                print('client_id=',client_id)
                Invoice.objects.filter(id=invoice_id).update(total=total, client_id=client_id,staff_id=staff_id, invoice_desc=invoice_desc, charge_code=charge_code, paid=save_paid, invoice_date=this_date, last_update=timestamp)
                
                client_list =  Clients.objects.filter(id=client_id).order_by('name').values_list('name', flat=True).distinct()
                invoice_id_list =  Invoice.objects.filter(id=client_id).order_by('invoice_desc').values_list('invoice_desc', flat=True).distinct()
                invoice_item_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=0).all()
                print('invoice_item_list =',invoice_item_list)
                invoice_list = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                print('invoice_list =',invoice_list)
                invoice_item = Invoice_Item.objects.filter(client_id=client_id, invoice_id=invoice_id).all()
                invoice = Invoice.objects.filter(client_id=client_id, id=invoice_id).all()
                if invoice:
                    invoice=invoice[0]
                total=0
                for subtotal in invoice_item:
                    total=round(total+float(subtotal.total),2)
                    print(total)
                print('client_list=',client_list)
                print('invoice_id_list=',invoice_id_list)
                print('invoice_list=',invoice_list)
                print('invoice_item_list=',invoice_item_list)
                print('invoice=',invoice.id)
                return HttpResponseRedirect(reverse('accounts:invoice'))
                                 
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/reconsile_invoice.html",{"invoice_id_list": invoice_id_list, 'client_list':client_list, 'invoice_list':invoice_list, 'invoice_item_list':invoice_item_list,
                        'invoice':invoice, 'client':client, "invoice_item":invoice_item, "operator":operator,'invoice_id':invoice_id, 'total':total, 'client':client, 'paid':paid, 'this_date':this_date})
                        
                        
class Charge_codeView(View):
    template_name = "charge.html"
    success_url = reverse_lazy('accounts:charge_code')
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
        return render (self.request,"accounts/charge_code.html",{'charge_list':charge_list,'client_list':client_list, "operator":operator,'item_id':item_id, 'item':item, 'client':client})

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
                    return HttpResponseRedirect(reverse('accounts:charge_code'))
            elif not update_item==-1:
                #update item	
                Charge_Code.objects.filter(id=item_id).update(charge_type=charge_type, client_id=client_id, charge=charge, charge_desc=charge_desc, start_date=start_date, end_date=end_date,last_update=timestamp)
            elif not save_item==-1:
                if Charge_Code.objects.filter(charge=charge).exists():
                    return render (self.request,"accounts/save_expenses.html",{"expense_list": expense_list, "id":id, "vendor_list":vendor_list, 'desc_list':desc_list,"exp":exp, 'contractor':contractor, "operator":operator})
                else:
                   #save item	
                    Charge_Code.objects.create(charge_type=charge_type, client_id=client_id, charge=charge, charge_desc=charge_desc, start_date=start_date, end_date=end_date,last_update=timestamp)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return HttpResponseRedirect(reverse('accounts:charge_code'))

        
def save_expenses_csv(delete):               
    #~~~~~~~~~~~Load expense database from csv. must put this somewhere else later"
    operator = str(self.request.user)
    import csv
    timestamp  = date.today()
    CSV_PATH = 'C:\\src\\ats\\accounts\\Expenses.csv'
    print('csv = ',CSV_PATH)
    
    # Remove all data from Table
    if delete=='yes':
        Expenses.objects.all().delete()
        
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for id, vendor, expense_type, expense_desc, sale_date, item_name, item_desc, quantity, item_cost, total_cost, interval_save, interval_time in reader:
        print('ID=',id)
        if vendor=='ï»¿Vani Kapor':
            vendor='Vani Kapor'
        print('vendor=',vendor)
        print('expense_type=',expense_type)
        print('expense_desc=',expense_desc)
        split_date = sale_date.split("/")
        print('split_date =',split_date)
        
        sale_date = split_date[2] + "-" + split_date[0] + "-" + split_date[1] # Formate 'YYYY-MM-DD'
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
        Expenses.objects.create(vendor_id=vendor_id, expense_type=expense_type, expense_description=expense_desc,  item=item_name, item_desc=item_desc, sale_date=sale_date,
                            quantity=quantity,item_cost=item_cost, total_cost=total_cost, reoccuuring_expenses=interval_save, reoccuring_interval=interval_time, operator=operator, last_update=timestamp)
                             
                                   

def save_invoices_csv(delete):               
    #~~~~~~~~~~~Load expense database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'C:\\src\\ats\\accounts\\Invoices.csv'
    print('csv = ',CSV_PATH)
   
   # Remove all data from Table
    if delete=='yes':
        Invoice.objects.all().delete()
      
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for id, invoice_desc, client_id, staff_id, invoice_date, paid in reader:
        print('id=',id)
        print('client_id=',client_id)
        print('staff_id=',staff_id)
        print('invoice_date=',invoice_date)
        print('paid=',paid)
        split_date = invoice_date.split("/")
        print('split_date =',split_date)
        
        invoice_date = split_date[2] + "-" + split_date[0] + "-" + split_date[1] # Formate 'YYYY-MM-DD'
        charge_code =  split_date[0] + split_date[1] + split_date[2] # Format 'MMDDYYYY'
        print('invoice_date =',invoice_date)
        print('charge_code =',charge_code)
        
        
        if paid=='FALSE':
            paid = False
        else:
            paid = True
        print('interval_save=',interval_save)
        Invoice.objects.create(client_id=client_id, staff_id=staff_id, invoice_desc=invoice_desc,  charge_code=charge_code, paid=paid, invoice_date=invoice_date, last_update=timestamp)
        
def save_invoice_item_csv(delete):               
    #~~~~~~~~~~~Load expense database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'C:\\src\\ats\\accounts\\Invoce_items.csv'
    print('csv = ',CSV_PATH)
   
         
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for id, invoice_id, contractor_id, client_id, staff_id, charge_code, resource_name, resource_type, service_type, item_date, quantity, rate, total, active in reader:
        print('id=',id)
        print('contractor_id=',contractor_id)
        print('invoice id=',invoice_id)
        print('client_id=',client_id)
        print('staff_id=',staff_id)
        print('charge_code=',charge_code)
        charge = Charge_Code.objects.filter(charge=charge_code)
        print('charge=',charge)
        charge_id = charge[0].id
        print('charge_id=',charge_id)
        
        service = Contractors.objects.filter(id=contractor_id)
        service_provider= service[0].name
        
        print('resource_name=',resource_name)
        print('resource_type=',resource_type)
        print('service_provider=',service_provider)
        print('service_type=',service_type)
        print('quantity=',quantity)
        print('rate=',rate)
        print('total=',total)
        print('active=',active)
        split_date = item_date.split("/")
        print('split_date =',split_date)
        
        item_date = split_date[2] + "-" + split_date[0] + "-" + split_date[1] # Formate 'YYYY-MM-DD'
        print('item_date=',item_date)
        
        cost_type= 'Per Hour'
        print('cost_type =',cost_type)
        print('charge_code =',charge_code)
        
        
        if active=='FALSE':
            active = False
        else:
            active = True
        
        Invoice_Item.objects.create(invoice_id=invoice_id, client_id=client_id, charge_id=charge_id, contractor_id=contractor_id, resource_type=resource_type,  service_type=service_type,
                                service_provider=service_provider ,cost_type=cost_type,  rate=rate, quantity=quantity, total=total, active=active, item_date=item_date, last_update=timestamp)


class IncomeView(View):
    template_name = "income.html"
    success_url = reverse_lazy('accounts:income')
    def get(self, *args, **kwargs):
        try:
            month = -1
            year = -1
            month_list = -1
            year_list = -1
            year_list=[]
            total = 0
            exp_total = 0
            operator = str(self.request.user)
            timestamp = date.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            thismonth = dt.month
            thisday = dt.day
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            print("in GET")
            income = Income_report.objects.all()
            for inc in income:
                total=round(total+float(inc.income_total),2)
            print(total)
            expense = Expenses.objects.all()
            for exp in expense:
                exp_total=round(exp_total+float(exp.total_cost),2)
            print(total)
            
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/income.html",{'income':income, "year":year, "month":month, "year_list":year_list, "month_list":month_list, "operator":operator, "total":total, 'exp_total':exp_total})
    
    def post(self, request, *args, **kwargs):
        try: 
            month = -1
            year = -1
            month_list = -1
            year_list = -1
            year_list=[]
            income=[]
            total = 0
            exp_total = 0
            operator = str(self.request.user)
            timestamp = date.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            thismonth = dt.month
            thisday = dt.day
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            print("in POST")
            month = request.POST.get('_month', -1)
            print('month =',month)
            year = request.POST.get('_year', -1)
            print('year =',year)
            search = request.POST.get('search', -1)
            print('search =',search)
            if not search ==-1:
                if  Income_report.objects.filter(id__icontains=search).exists():
                    income = Income_report.objects.filter(id__contains=search).all()
                    print('search 1=',income)
                elif  Income_report.objects.filter(month_str__icontains=search).exists():
                    income = Income_report.objects.filter(month_str__icontains=search).all()
                    print('search 2=',income)
                elif Income_report.objects.filter(income_total__icontains=search).exists():
                    income = Income_report.objects.filter(income_total__contains=search).all()
                    print('search 5=',income)
                elif Income_report.objects.filter(expense__contains=search).exists():
                    income = Income_report.objects.filter(expense__contains=search).all()
                    print('search 6=',income)
            elif not month=="all months" and not  year=="all years": 
                income = Income_report.objects.filter(year__contains=year, month__contains=month).all()  
            elif month=="all months" and not  year=="all years": 
                income = Income_report.objects.filter(year__contains=year).all()  
            elif not month=="all months" and  year=="all years": 
                income = Income_report.objects.filter(month_str__contains=month).all()  
            else: 
                income = Income_report.objects.all()
            
            for inc in income:
                total=round(total+float(inc.income_total),2)
            print(total)
            expense = Expenses.objects.all()
            for exp in expense:
                exp_total=round(exp_total+float(exp.total_cost),2)
            print(total)
            
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"accounts/income.html",{'income':income, "year":year, "month":month, "year_list":year_list, "month_list":month_list, "operator":operator, "total":total, 'exp_total':exp_total})
     