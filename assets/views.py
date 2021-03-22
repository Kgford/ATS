from django import forms
from ATS import settings
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
from assets.models import Personnel, Vehical, Business_Space, Product
from assets.forms import VehicleForm
from cloudinary.forms import cl_init_js_callbacks 
from vendor.models import Vendor
from contractors.models import Contractors
from .forms import *
from django.views import View
import datetime
from collections import OrderedDict
from ATS.overhead import Equations
from re import search
from ATS.overhead import Comunication
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import cloudinary
import cloudinary.uploader
import cloudinary.api

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
            
            

class AssetsView(View):
    template_name = "index.html"
    success_url = reverse_lazy('assets:assests')
    def get(self, *args, **kwargs):
        try:
            veh= []
            assets= []
            vehicles=[]
            spaces=[]
            personnel=[]
            operator = str(self.request.user)
            phone = self.request.user.userprofileinfo.phone
            message = 'hello this is a test'
            com=Comunication(phone,message)
            print('com=',com)
            com.send_sms()
            month_list = -1
            year_list = -1
            timestamp = date.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            thismonth = dt.month
            thisday = dt.day
            print('thismonth=',thismonth)
            print('thisyear=',thisyear)
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            full_months = {'1': "Janurary", '2': "Februay",  '3': "March", '4': 'April', '5': "May", '6': "June", '7': "July", '8': "August", '9': "September", '10': "October", '11': "November", '12': "December"}
            month = months[str(thismonth)]
            month_full = full_months[str(thismonth)]
            print('month =',month)
            operator = str(self.request.user)
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            veh_id = self.request.GET.get('vehicle', -1)
            build_id = self.request.GET.get('building', -1)
            person_id = self.request.GET.get('personnel', -1)
            product_id = self.request.GET.get('product', -1)
            vehicles = Vehical.objects.all()
            print('vehicles=',vehicles)
            personnel = Personnel.objects.all()
            spaces = Business_Space.objects.all()
            print('spaces=',spaces)
            product = Product.objects.all()
            # Building expences 
            expense_year_building = Expenses.objects.filter(sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Building').all()
            expense_month_building = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets', expense_description__icontains='Building').all()
            # Travel expenses
            expense_year_travel = Expenses.objects.filter(sale_date__year=thisyear, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            expense_month_travel = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            print('expense_year_travel=',expense_year_travel)
            office = Business_Space.objects.filter(last_update__year=thisyear, type__icontains='OFFICE').last()
            shop = Business_Space.objects.filter(last_update__year=thisyear, type__icontains='SHOP').last()
            lab = Business_Space.objects.filter(last_update__year=thisyear, type__icontains='LAB').last()
            
            print('expense_year_building',expense_year_building)
            print('expense_month_building',expense_month_building)
            print('expense_year_travel',expense_year_travel)
            print('expense_month_travel',expense_month_travel)
            building_month=0
            space_month=0
            utilities_month=0
            fuel_month=0
            internet_month=0
            tax_month=0
            insurance_month=0
            interest_month=0
            payments_month=0
            
            building_space_month=0
            utilities_space_month=0
            fuel_space_month=0
            internet_space_month=0
            tax_space_month=0
            insurance_space_month=0
            interest_space_month=0
            payments_space_month=0
            for item in expense_month_building:
                print('item-',item)
                if search('MAIN', item.item_desc.upper()) and search('PAYMENT', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    payments_space_month = payments_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    payments_space_month = payments_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    payments_space_month = payments_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    payments_month = payments_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('building_month=',building_month)
                elif search('MAIN', item.item_desc.upper()) and search('UTILITIES', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.power_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    utilities_space_month = utilities_space_month + (float(item.total_cost) * (float(office.power_percentage)/100))
                    utilities_space_month = utilities_space_month + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    utilities_space_month = utilities_space_month + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.power_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    utilities_month = utilities_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
                elif search('MAIN', item.item_desc.upper()) and search('FUEL', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_space_month = fuel_space_month + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    print('fuel_space_month=',fuel_space_month)
                    fuel_space_month = fuel_space_month + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    print('fuel_space_month=',fuel_space_month)
                    fuel_space_month = fuel_space_month + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    print('fuel_space_month=',fuel_space_month)
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_month = fuel_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
                elif search('MAIN', item.item_desc.upper()) and search('INTERNET', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    internet_space_month = internet_space_month + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    internet_space_month = internet_space_month + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    internet_space_month = internet_space_month + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    internet_month = internet_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
                elif search('MAIN', item.item_desc.upper()) and search('TAX', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    tax_space_month = tax_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    tax_space_month = tax_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    tax_space_month = tax_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    tax_month = tax_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('tax_month=',tax_month)
                elif search('MAIN', item.item_desc.upper()) and search('INSURANCE', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_space_month = insurance_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    insurance_space_month = insurance_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    insurance_space_month = insurance_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_month = insurance_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('insurance_month=',insurance_month)
                elif search('MAIN', item.item_desc.upper()) and search('INTEREST', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    interest_space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    interest_space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_month = utilities_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
            
            building_year=0
            space_year=0
            utilities_year=0
            fuel_year=0
            internet_year=0
            tax_year=0
            insurance_year=0
            interest_year=0
            payments_year=0
            
            building_space_year=0
            utilities_space_year=0
            fuel_space_year=0
            internet_space_year=0
            tax_space_year=0
            insurance_space_year=0
            interest_space_year=0
            payments_space_year=0
            monthly_mile=0
            print('payments_space_year=',payments_space_year)
            for item in expense_year_building:
                #print('item-',item)
                if search('MAIN', item.item_desc.upper()) and search('PAYMENT', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    payments_space_year = payments_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    payments_space_year = payments_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    payments_space_year = payments_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    payments_year = payments_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    print('payments_space_year=',payments_space_year)
                elif search('MAIN', item.item_desc.upper()) and search('UTILITIES', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.power_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    utilities_space_year = utilities_space_year + (float(item.total_cost) * (float(office.power_percentage)/100))
                    utilities_space_year = utilities_space_year + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    utilities_space_year = utilities_space_year + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.power_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    utilities_year = utilities_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('space_year=',space_year)
                elif search('MAIN', item.item_desc.upper()) and search('FUEL', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_space_year = fuel_space_year + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    print('fuel_space_year=',fuel_space_year)
                    print('(float(item.total_cost)=',float(item.total_cost))
                    fuel_space_year = fuel_space_year + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    print('fuel_space_year=',fuel_space_year)
                    fuel_space_year = fuel_space_year + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    print('fuel_space_year=',fuel_space_year)
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_year = fuel_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('space_year=',space_year)
                elif search('MAIN', item.item_desc.upper()) and search('INTERNET', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    internet_space_year = internet_space_year + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    internet_space_year = internet_space_year + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    internet_space_year = internet_space_year + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    internet_year = internet_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('space_year=',space_year)
                elif search('MAIN', item.item_desc.upper()) and search('TAX', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    tax_space_year = tax_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    tax_space_year = tax_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    tax_space_year = tax_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    tax_year = tax_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('tax_year=',tax_year)
                elif search('MAIN', item.item_desc.upper()) and search('INSURANCE', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_space_year = insurance_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    insurance_space_year = insurance_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    insurance_space_year = insurance_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_year = insurance_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('insurance_year=',insurance_year)
                elif search('MAIN', item.item_desc.upper()) and search('INTEREST', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_space_year = interest_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    interest_space_year = interest_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    interest_space_year = interest_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_year = utilities_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    print('space_year=',space_year)
                    print('interest_space_year=',interest_space_year)
           
            total_taxed  =  [building_year,space_year]
            cost_list_year  =  [payments_space_year, interest_space_year, insurance_space_year, tax_space_year, utilities_space_year, fuel_space_year, internet_space_year]
            cost_list_month  =  [payments_space_month, interest_space_month, insurance_space_month, tax_space_month, utilities_space_month, fuel_space_month, internet_space_month]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vehicle Expenses~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print('thisyear at list2',thisyear)
            print('thismonth at list2',thismonth)
            expense_year_travel = Expenses.objects.filter(sale_date__year=thisyear, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            expense_month_travel = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            print('expense_year_travel=',expense_year_travel)
            
            expense_year_vehicle = Expenses.objects.filter(sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Vehicle')
            expense_year_gas = Expenses.objects.filter(sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Gas')
            expense_month_vehicle = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Vehicle')
            expense_month_gas = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Gas')
            print('expense_year_vehicle',expense_year_vehicle)
            print('expense_month_vehicle',expense_month_vehicle)
            print('expense_month_gas',expense_month_gas)
            print('expense_year_gas',expense_year_gas)
                             
            
            vehicle_year=0
            vehicle_month=0
            vehicle_month_taxable=0
            payments_vehicle_month=0
            payments_vehicle_month=0
            insurance_vehicle_month=0
            interest_vehicle_month=0
            tax_vehicle_month=0
            repair_vehicle_month=0
            fuel_vehicle_month=0
            mantenance_vehicle_month=0
            payments_vehicle_month_taxable=0
            payments_vehicle_month_taxable=0
            insurance_vehicle_month_taxable=0
            interest_vehicle_month_taxable=0
            tax_vehicle_month_taxable=0
            repair_vehicle_month_taxable=0
            fuel_vehicle_month_taxable=0
            mantenance_vehicle_month_taxable=0
            
            travel_cost_month = 0
            travel_miles_month = 0
            for item in expense_month_travel:
                print('in expense_month_travel item')
                travel_cost_month = travel_cost_month + (float(item.total_cost))
                get_travel_miles = Equations(0,0)
                travel_miles = get_travel_miles.get_num(item.item_desc)
                travel_miles_month = travel_miles_month + travel_miles
            
            print('travel_cost_month=',travel_cost_month)
            mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
            print('mile=',mile)
            for miles in mile:
                print('miles=',miles.monthy_miles)
                monthly_mile = monthly_mile + (float(miles.monthy_miles))
                print('monthly_mile=',monthly_mile)
            
            if monthly_mile == 0:
                taxable_percent_month = 0
            else:
                taxable_percent_month = travel_miles_month/monthly_mile
            print('taxable_percent_month=',taxable_percent_month)
            
            for item in expense_month_gas:
                fuel_vehicle_month = fuel_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                fuel_vehicle_month_taxable = (fuel_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                vehicle_month = vehicle_month + float(item.total_cost)
                vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_month)))
                print('in month gas',fuel_vehicle_month )
                    
            for item in expense_month_vehicle:
                print('item-',item)
                if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                    payments_vehicle_month = (payments_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                    payments_vehicle_month_taxable = (payments_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    print('payments_vehicle_month=',payments_vehicle_month)
                    print('vehicle_month_taxable=',vehicle_month_taxable)
                    print('vehicle_month=',vehicle_month)
                elif search('VEHICLE', item.expense_description.upper()) and search('INTEREST', item.expense_description.upper()):
                    interest_vehicle_month = interest_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    interest_vehicle_month_taxable = interest_vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = vehicle_month + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_month)))
                elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                    insurance_vehicle_month = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    insurance_vehicle_month_taxable = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost))  * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                    tax_vehicle_month = (tax_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                    tax_vehicle_month_taxable = (tax_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                    repair_vehicle_month = repair_vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                    repair_vehicle_month_taxable = (repair_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and (search('OIL', item.expense_description.upper()) or search('TIRES', item.expense_description.upper())):
                    mantenance_vehicle_month = mantenance_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    mantenance_vehicle_month_taxable = (mantenance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    vehicle_month = vehicle_month + float(item.total_cost)
            
             
            payments_vehicle_year_taxable=0
            payments_vehicle_year_taxable=0
            insurance_vehicle_year_taxable=0
            interest_vehicle_year_taxable=0
            tax_vehicle_year_taxable=0
            repair_vehicle_year_taxable=0
            fuel_vehicle_year_taxable=0
            mantenance_vehicle_year_taxable=0
            payments_vehicle_year=0
            payments_vehicle_year=0
            insurance_vehicle_year=0
            interest_vehicle_year=0
            tax_vehicle_year=0
            repair_vehicle_year=0
            fuel_vehicle_year=0
            mantenance_vehicle_year=0
           
            travel_cost_year = 0
            travel_miles_year = 0
            year_miles = 0
            for item in expense_year_travel:
                print('in expense_month_travel item')
                travel_cost_year = travel_cost_year + (float(item.total_cost))
                get_travel_miles = Equations(0,0)
                travel_miles = get_travel_miles.get_num(item.item_desc)
                travel_miles_year = travel_miles_year + travel_miles
            print('travel_cost_year=',travel_cost_year)
            mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
            print('mile=',mile)
            for miles in mile:
                print('year_miles=',miles.monthy_miles * int(thismonth))
                year_miles = year_miles + (float(miles.monthy_miles *  int(thismonth)))
                print('year_miles=',year_miles)
            
            if year_miles==0:
                taxable_percent_year = 0
            else:
                taxable_percent_year = travel_miles_year/year_miles 
            print('yeary taxable_percent=',taxable_percent_year)
           
            vehicle_year_taxable=0
            for item in expense_year_gas:
                fuel_vehicle_year = fuel_vehicle_year + (float(item.total_cost) * (float(taxable_percent_month)))
                fuel_vehicle_year_taxable = (fuel_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                vehicle_year = vehicle_month + float(item.total_cost)
                vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_month)))
                print('in year gas',fuel_vehicle_year )
            
            for item in expense_year_vehicle:
                print('item-',item)
                if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                    payments_vehicle_year = (payments_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                    payments_vehicle_year_taxable = (payments_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                    print('payments_vehicle_year=',payments_vehicle_year)
                    print('vehicle_year_taxable=',vehicle_year_taxable)
                    print('vehicle_year=',vehicle_year)
                elif search('VEHICLE', item.expense_description.upper()) and search('INTEREST', item.expense_description.upper()):
                    interest_vehicle_year = interest_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                    interest_vehicle_year_taxable = interest_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = vehicle_year + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_year)))
                elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                    insurance_vehicle_year = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    insurance_vehicle_year_taxable = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                    tax_vehicle_year = (tax_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                    tax_vehicle_year_taxable = (tax_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                    repair_vehicle_year = repair_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    repair_vehicle_year_taxable = (repair_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and (search('OIL', item.expense_description.upper()) or search('TIRES', item.expense_description.upper())):
                    mantenance_vehicle_year = mantenance_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                    mantenance_vehicle_year_taxable = (mantenance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
            
            
            print('vehicle_month',vehicle_month)
            print('vehicle_month_taxable',vehicle_month_taxable)
            print('vehicle_year_taxable',vehicle_year_taxable)
            print ('payments_vehicle_year_taxable',payments_vehicle_year_taxable)
            total_taxed_v  =  [vehicle_year,vehicle_year_taxable]
            
            cost_list_month_v  =  [payments_vehicle_month_taxable, insurance_vehicle_month_taxable, interest_vehicle_month_taxable, tax_vehicle_month_taxable, travel_cost_month, repair_vehicle_month_taxable, fuel_vehicle_month_taxable]
            cost_list_year_v  =  [payments_vehicle_year_taxable, insurance_vehicle_year_taxable, interest_vehicle_year_taxable, tax_vehicle_year_taxable, travel_cost_year, repair_vehicle_year_taxable, fuel_vehicle_year_taxable]
            print('cost_list_month_v=',cost_list_month_v)
            print(vehicles)
        except IOError as e:
            print ("Lists load Failure ", e) 
            
            print('error = ',e) 
        return render (self.request,"assets/index.html",{"personnel": personnel, "spaces": spaces, "vehicles": vehicles, "veh":veh, "index_type":"assests", 'avatar':avatar, 'year_list':year_list, 'month_list':month_list,'utilities_month':utilities_month,
                                     'total_taxed':total_taxed, 'cost_list_year':cost_list_year, 'fuel_month':fuel_month,'internet_month':internet_month, 'tax_month':tax_month, 'insurance_month':insurance_month,'interest_month':interest_month,'cost_list_month':cost_list_month,
                                     'total_taxed_v':total_taxed_v, 'cost_list_year_v':cost_list_year_v, 'cost_list_month_v':cost_list_month_v, 'utilities_year':utilities_year,'fuel_year':fuel_year,'internet_year':internet_year, 'tax_year':tax_year, 'insurance_year':insurance_year, 'interest_year':interest_year,
                                     'building_month':building_month, 'building_year':building_year, 'space_month':space_month, 'space_year':space_year, 'month_full':month_full,'month':month,'year':thisyear,
                                     'vehicle_month':vehicle_month, 'vehicle_year':vehicle_year, 'vehicle_month_taxable':vehicle_month_taxable, 'vehicle_year_taxable':vehicle_year_taxable})


    def post(self, *args, **kwargs):
        try:
            tmonth_list = -1
            year_list = -1
            veh= []
            assets= []
            vehicles=[]
            spaces=[]
            personnel=[]
            operator = str(self.request.user)
            phone = self.request.user.userprofileinfo.phone
            message = 'message'
            month_list = -1
            year_list = -1
            timestamp = date.today()
            dt = datetime.datetime.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            
            thisday = dt.day
            thisyear = self.request.POST.get('_year', -1)
            month = self.request.POST.get('_month', -1)
            mon = self.request.POST.get('_month', -1)
            print('month=',month)
            printnow = self.request.POST.get('_print', -1)
            year=thisyear
            print('year',year)
            timestamp = date.today()
            print('timestamp',timestamp)
            months_num = {'Jan': "1", 'Feb': "2",  'Mar': "3", 'Apr': '4', 'May': "5", 'Jun': "6", 'Jul': "7", 'Aug': "8", 'Sept': "9", '10': "Oct", 'Nov': "11", 'Dec': "12"}
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            full_months = {'1': "Janurary", '2': "Februay",  '3': "March", '4': 'April', '5': "May", '6': "June", '7': "July", '8': "August", '9': "September", '10': "October", '11': "November", '12': "December"}
            
            thismonth = months_num[str(month)]
            month_full = full_months[str(thismonth)]
            print('thismonth =',thismonth)
            operator = str(self.request.user)
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            vehicles = Vehical.objects.all()
            print('vehicles=',vehicles)
            personnel = Personnel.objects.all()
            spaces = Business_Space.objects.all()
            print('spaces=',spaces)
            product = Product.objects.all()
            print('thisyear at list1',thisyear)
            print('thismonth at list1',thismonth)
            # Building expences 
            expense_year_building = Expenses.objects.filter(sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Building').all()
            expense_month_building = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets', expense_description__icontains='Building').all()
            # Travel expenses
            expense_year_travel = Expenses.objects.filter(sale_date__year=thisyear, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            expense_month_travel = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            print('expense_year_travel=',expense_year_travel)
            office = Business_Space.objects.filter(last_update__year=thisyear, type__icontains='OFFICE').last()
            shop = Business_Space.objects.filter(last_update__year=thisyear, type__icontains='SHOP').last()
            lab = Business_Space.objects.filter(last_update__year=thisyear, type__icontains='LAB').last()
            
            print('expense_year_building',expense_year_building)
            print('expense_month_building',expense_month_building)
            print('expense_year_travel',expense_year_travel)
            print('expense_month_travel',expense_month_travel)
            building_month=0
            space_month=0
            utilities_month=0
            fuel_month=0
            internet_month=0
            tax_month=0
            insurance_month=0
            interest_month=0
            payments_month=0
            
            building_space_month=0
            utilities_space_month=0
            fuel_space_month=0
            internet_space_month=0
            tax_space_month=0
            insurance_space_month=0
            interest_space_month=0
            payments_space_month=0
            for item in expense_month_building:
                print('item-',item)
                if search('MAIN', item.item_desc.upper()) and search('PAYMENT', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    payments_space_month = payments_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    payments_space_month = payments_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    payments_space_month = payments_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    payments_month = payments_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('building_month=',building_month)
                elif search('MAIN', item.item_desc.upper()) and search('UTILITIES', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.power_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    utilities_space_month = utilities_space_month + (float(item.total_cost) * (float(office.power_percentage)/100))
                    utilities_space_month = utilities_space_month + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    utilities_space_month = utilities_space_month + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.power_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    utilities_month = utilities_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
                elif search('MAIN', item.item_desc.upper()) and search('FUEL', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_space_month = fuel_space_month + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    fuel_space_month = fuel_space_month + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    fuel_space_month = fuel_space_month + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_month = fuel_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
                elif search('MAIN', item.item_desc.upper()) and search('INTERNET', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    internet_space_month = internet_space_month + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    internet_space_month = internet_space_month + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    internet_space_month = internet_space_month + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    internet_month = internet_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
                elif search('MAIN', item.item_desc.upper()) and search('TAX', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    tax_space_month = tax_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    tax_space_month = tax_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    tax_space_month = tax_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    tax_month = tax_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('tax_month=',tax_month)
                elif search('MAIN', item.item_desc.upper()) and search('INSURANCE', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_space_month = insurance_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    insurance_space_month = insurance_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    insurance_space_month = insurance_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_month = building_space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = building_space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_month = insurance_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('insurance_month=',insurance_month)
                elif search('MAIN', item.item_desc.upper()) and search('INTEREST', item.expense_description.upper()):
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    interest_space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    interest_space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    space_month = space_month + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_month = space_month + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_month = space_month + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_month = utilities_month + float(item.total_cost)
                    building_month = building_month + float(item.total_cost)
                    print('space_month=',space_month)
            
            building_year=0
            space_year=0
            utilities_year=0
            fuel_year=0
            internet_year=0
            tax_year=0
            insurance_year=0
            interest_year=0
            payments_year=0
            
            building_space_year=0
            utilities_space_year=0
            fuel_space_year=0
            internet_space_year=0
            tax_space_year=0
            insurance_space_year=0
            interest_space_year=0
            payments_space_year=0
            monthly_mile=0
            print('payments_space_year=',payments_space_year)
            for item in expense_year_building:
                #print('item-',item)
                if search('MAIN', item.item_desc.upper()) and search('PAYMENT', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    payments_space_year = payments_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    payments_space_year = payments_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    payments_space_year = payments_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    payments_year = payments_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    print('payments_space_year=',payments_space_year)
                elif search('MAIN', item.item_desc.upper()) and search('UTILITIES', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.power_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    utilities_space_year = utilities_space_year + (float(item.total_cost) * (float(office.power_percentage)/100))
                    utilities_space_year = utilities_space_year + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    utilities_space_year = utilities_space_year + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.power_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.power_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.power_percentage)/100))
                    
                    utilities_year = utilities_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('space_year=',space_year)
                elif search('MAIN', item.item_desc.upper()) and search('FUEL', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_space_year = fuel_space_year + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    fuel_space_year = fuel_space_year + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    fuel_space_year = fuel_space_year + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.fuel_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.fuel_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.fuel_percentage)/100))
                    
                    fuel_year = fuel_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('space_year=',space_year)
                elif search('MAIN', item.item_desc.upper()) and search('INTERNET', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    internet_space_year = internet_space_year + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    internet_space_year = internet_space_year + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    internet_space_year = internet_space_year + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.internet_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.internet_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.internet_percentage)/100))
                    
                    internet_year = internet_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('space_year=',space_year)
                elif search('MAIN', item.item_desc.upper()) and search('TAX', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    tax_space_year = tax_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    tax_space_year = tax_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    tax_space_year = tax_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    tax_year = tax_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('tax_year=',tax_year)
                elif search('MAIN', item.item_desc.upper()) and search('INSURANCE', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_space_year = insurance_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    insurance_space_year = insurance_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    insurance_space_year = insurance_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    insurance_year = insurance_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    #print('insurance_year=',insurance_year)
                elif search('MAIN', item.item_desc.upper()) and search('INTEREST', item.expense_description.upper()):
                    space_year = space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    space_year = space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    building_space_year = building_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    building_space_year = building_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_space_year = interest_space_year + (float(item.total_cost) * (float(office.space_percentage)/100))
                    interest_space_year = interest_space_year + (float(item.total_cost) * (float(shop.space_percentage)/100))
                    interest_space_year = interest_space_year + (float(item.total_cost) * (float(lab.space_percentage)/100))
                    
                    interest_year = utilities_year + float(item.total_cost)
                    building_year = building_year + float(item.total_cost)
                    print('space_year=',space_year)
                    print('interest_space_year=',interest_space_year)
           
            total_taxed  =  [building_year,space_year]
            cost_list_year  =  [payments_space_year, interest_space_year, insurance_space_year, tax_space_year, utilities_space_year, fuel_space_year, internet_space_year]
            cost_list_month  =  [payments_space_month, interest_space_month, insurance_space_month, tax_space_month, utilities_space_month, fuel_space_month, internet_space_month]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vehicle Expenses~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print('thisyear at list2',thisyear)
            print('thismonth at list2',thismonth)
            
            expense_year_vehicle = Expenses.objects.filter(sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Vehicle')
            expense_year_gas = Expenses.objects.filter(sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Gas')
            expense_month_vehicle = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Vehicle')
            expense_month_gas = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Gas')
            print('expense_year_vehicle',expense_year_vehicle)
            print('expense_month_vehicle',expense_month_vehicle)
            print('expense_month_gas',expense_month_gas)
            print('expense_year_gas',expense_year_gas)
                             
            
            vehicle_year=0
            vehicle_month=0
            vehicle_month_taxable=0
            payments_vehicle_month=0
            payments_vehicle_month=0
            insurance_vehicle_month=0
            interest_vehicle_month=0
            tax_vehicle_month=0
            repair_vehicle_month=0
            fuel_vehicle_month=0
            mantenance_vehicle_month=0
            payments_vehicle_month_taxable=0
            payments_vehicle_month_taxable=0
            insurance_vehicle_month_taxable=0
            interest_vehicle_month_taxable=0
            tax_vehicle_month_taxable=0
            repair_vehicle_month_taxable=0
            fuel_vehicle_month_taxable=0
            mantenance_vehicle_month_taxable=0
            
            travel_cost_month = 0
            travel_miles_month = 0
            for item in expense_month_travel:
                print('in expense_month_travel item')
                travel_cost_month = travel_cost_month + (float(item.total_cost))
                get_travel_miles = Equations(0,0)
                travel_miles = get_travel_miles.get_num(item.item_desc)
                travel_miles_month = travel_miles_month + travel_miles
            
            print('travel_cost_month=',travel_cost_month)
            mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
            print('mile=',mile)
            for miles in mile:
                print('miles=',miles.monthy_miles)
                monthly_mile = monthly_mile + (float(miles.monthy_miles))
                print('monthly_mile=',monthly_mile)
            
            if monthly_mile == 0:
                taxable_percent_month = 0
            else:
                taxable_percent_month = travel_miles_month/monthly_mile
            print('taxable_percent_month=',taxable_percent_month)
            
            for item in expense_month_gas:
                fuel_vehicle_month = fuel_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                fuel_vehicle_month_taxable = (fuel_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                vehicle_month = vehicle_month + float(item.total_cost)
                vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_month)))
                print('in month gas',fuel_vehicle_month )
                    
            for item in expense_month_vehicle:
                print('item-',item)
                if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                    payments_vehicle_month = (payments_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                    payments_vehicle_month_taxable = (payments_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    print('payments_vehicle_month=',payments_vehicle_month)
                    print('vehicle_month_taxable=',vehicle_month_taxable)
                    print('vehicle_month=',vehicle_month)
                elif search('VEHICLE', item.expense_description.upper()) and search('INTEREST', item.expense_description.upper()):
                    interest_vehicle_month = interest_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    interest_vehicle_month_taxable = interest_vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = vehicle_month + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_month)))
                elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                    insurance_vehicle_month = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    insurance_vehicle_month_taxable = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost))  * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                    tax_vehicle_month = (tax_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                    tax_vehicle_month_taxable = (tax_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                    repair_vehicle_month = repair_vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                    repair_vehicle_month_taxable = (repair_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and (search('OIL', item.expense_description.upper()) or search('TIRES', item.expense_description.upper())):
                    mantenance_vehicle_month = mantenance_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    mantenance_vehicle_month_taxable = (mantenance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    vehicle_month = vehicle_month + float(item.total_cost)
            
             
            payments_vehicle_year_taxable=0
            payments_vehicle_year_taxable=0
            insurance_vehicle_year_taxable=0
            interest_vehicle_year_taxable=0
            tax_vehicle_year_taxable=0
            repair_vehicle_year_taxable=0
            fuel_vehicle_year_taxable=0
            mantenance_vehicle_year_taxable=0
            payments_vehicle_year=0
            payments_vehicle_year=0
            insurance_vehicle_year=0
            interest_vehicle_year=0
            tax_vehicle_year=0
            repair_vehicle_year=0
            fuel_vehicle_year=0
            mantenance_vehicle_year=0
           
            travel_cost_year = 0
            travel_miles_year = 0
            year_miles = 0
            for item in expense_year_travel:
                print('in expense_month_travel item')
                travel_cost_year = travel_cost_year + (float(item.total_cost))
                get_travel_miles = Equations(0,0)
                travel_miles = get_travel_miles.get_num(item.item_desc)
                travel_miles_year = travel_miles_year + travel_miles
            print('travel_cost_year=',travel_cost_year)
            mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
            print('mile=',mile)
            for miles in mile:
                print('year_miles=',miles.monthy_miles * int(thismonth))
                year_miles = year_miles + (float(miles.monthy_miles *  int(thismonth)))
                print('year_miles=',year_miles)
            
            if year_miles==0:
                taxable_percent_year = 0
            else:
                taxable_percent_year = travel_miles_year/year_miles 
            print('yeary taxable_percent=',taxable_percent_year)
           
            vehicle_year_taxable=0
            for item in expense_year_gas:
                fuel_vehicle_year = fuel_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                fuel_vehicle_year_taxable = (fuel_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                vehicle_year = vehicle_year + float(item.total_cost)
                vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_year)))
                print('in year gas',fuel_vehicle_year )
            
            for item in expense_year_vehicle:
                print('item-',item)
                if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                    payments_vehicle_year = (payments_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                    payments_vehicle_year_taxable = (payments_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                    print('payments_vehicle_year=',payments_vehicle_year)
                    print('vehicle_year_taxable=',vehicle_year_taxable)
                    print('vehicle_year=',vehicle_year)
                elif search('VEHICLE', item.expense_description.upper()) and search('INTEREST', item.expense_description.upper()):
                    interest_vehicle_year = interest_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                    interest_vehicle_year_taxable = interest_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = vehicle_year + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_year)))
                elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                    insurance_vehicle_year = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    insurance_vehicle_year_taxable = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                    tax_vehicle_year = (tax_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                    tax_vehicle_year_taxable = (tax_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                    repair_vehicle_year = repair_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    repair_vehicle_year_taxable = (repair_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and (search('OIL', item.expense_description.upper()) or search('TIRES', item.expense_description.upper())):
                    mantenance_vehicle_year = mantenance_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                    mantenance_vehicle_year_taxable = (mantenance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
            
            
            print('vehicle_month',vehicle_month)
            print('vehicle_month_taxable',vehicle_month_taxable)
            print('vehicle_year_taxable',vehicle_year_taxable)
            print ('payments_vehicle_year_taxable',payments_vehicle_year_taxable)
            total_taxed_v  =  [vehicle_year,vehicle_year_taxable]
            
            cost_list_month_v  =  [payments_vehicle_month_taxable, insurance_vehicle_month_taxable, interest_vehicle_month_taxable, tax_vehicle_month_taxable, travel_cost_month, repair_vehicle_month_taxable, fuel_vehicle_month_taxable]
            cost_list_year_v  =  [payments_vehicle_year_taxable, insurance_vehicle_year_taxable, interest_vehicle_year_taxable, tax_vehicle_year_taxable, travel_cost_year, repair_vehicle_year_taxable, fuel_vehicle_year_taxable]
            print('cost_list_month_v=',cost_list_month_v)
            print(vehicles)
        except IOError as e:
            print ("Lists load Failure ", e) 
            
            print('error = ',e) 
        return render (self.request,"assets/index.html",{"personnel": personnel, "spaces": spaces, "vehicles": vehicles, "veh":veh, "index_type":"assests", 'avatar':avatar, 'year_list':year_list, 'month_list':month_list,'utilities_month':utilities_month,
                                     'total_taxed':total_taxed, 'cost_list_year':cost_list_year, 'fuel_month':fuel_month,'internet_month':internet_month, 'tax_month':tax_month, 'insurance_month':insurance_month,'interest_month':interest_month,'cost_list_month':cost_list_month,
                                     'total_taxed_v':total_taxed_v, 'cost_list_year_v':cost_list_year_v, 'cost_list_month_v':cost_list_month_v, 'utilities_year':utilities_year,'fuel_year':fuel_year,'internet_year':internet_year, 'tax_year':tax_year, 'insurance_year':insurance_year, 'interest_year':interest_year,
                                     'building_month':building_month, 'building_year':building_year, 'space_month':space_month, 'space_year':space_year, 'month_full':month_full,'month':month,'year':thisyear,
                                     'vehicle_month':vehicle_month, 'vehicle_year':vehicle_year, 'vehicle_month_taxable':vehicle_month_taxable, 'vehicle_year_taxable':vehicle_year_taxable})


class VehicleView(View):
    template_name = "vehicle.html"
    success_url = reverse_lazy('assets:vehicle')
    context = dict( backend_form = VehicleForm())
    def get(self, *args, **kwargs):
            vehicles = []
            veh = []
            uploaded_file_url=None
            print('we are here')
            # cast the request inventory_id from string to integer type.
            success = True 
            try:	
                timestamp = date.today()
                operator = str(self.request.user)
                dt = datetime.datetime.today()
                thisyear = dt.year
                thismonth = dt.month
                thisday = dt.day
                print('thismonth=',thismonth)
                print('thisyear=',thisyear)
                months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
                month = months[str(thismonth)]
                print('month =',month) 
                insurance=0
                payment_month=0
                payment_year=0
                fuel_month=0
                fuel_year=0
                maintenance=0
                repair=0;
                tires=0
                inspection=0
                veh=-1
                duplicate=-1
                business_use=-1
                vehicle_year=0
                vehicle_month=0
                vehicle_month_taxable=0
                payments_vehicle_month=0
                payments_vehicle_month=0
                insurance_vehicle_month=0
                interest_vehicle_month=0
                tax_vehicle_month=0
                repair_vehicle_month=0
                fuel_vehicle_month=0
                mantenance_vehicle_month=0
                tire_vehicle_month=0
                payments_vehicle_month_taxable=0
                payments_vehicle_month_taxable=0
                insurance_vehicle_month_taxable=0
                interest_vehicle_month_taxable=0
                tax_vehicle_month_taxable=0
                repair_vehicle_month_taxable=0
                fuel_vehicle_month_taxable=0
                mantenance_vehicle_month_taxable=0
                tire_vehicle_month_taxable=0
                monthly_mile=0
                payments_vehicle_year_taxable=0
                payments_vehicle_year_taxable=0
                insurance_vehicle_year_taxable=0
                inspection_vehicle_year_taxable=0
                tax_vehicle_year_taxable=0
                repair_vehicle_year_taxable=0
                fuel_vehicle_year_taxable=0
                mantenance_vehicle_year_taxable=0
                tire_vehicle_year_taxable=0
                payments_vehicle_year=0
                insurance_vehicle_year=0
                inspection_vehicle_year=0
                tax_vehicle_year=0
                repair_vehicle_year=0
                fuel_vehicle_year=0
                mantenance_vehicle_year=0
                tire_vehicle_year=0
                image = -1
                image_file =-1
                form = VehicleForm()
                       
                years = []
                year = datetime.date.today().year
                for i in range(-40,0):
                    years.append(year+i)
                vehicles=Vehical.objects.all()
                veh_id = self.request.GET.get('veh_id', -1)
                print('vehicles=',vehicles)
                print('veh_id=',veh_id)
                if veh_id!=-1:
                    veh = Vehical.objects.filter(id=veh_id).all()
                    print('veh=',veh)
                    veh=veh[0]
                    print('veh=',veh)
                    print('veh.image=',veh.image)
                    print('veh.business_use',veh.business_use)
                    if veh.business_use:
                        business_use = 'on'
                    else:
                        business_use = 'off'
                    if veh.image != -1:
                        print('veh.image=',veh.image)
                        uploaded_file_url= str(veh.image)
                        print('uploaded_file_url',uploaded_file_url)
                        file_name = str(veh.image)
                        print('file_name',file_name)
                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vehicle Expenses~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        expense_year_travel = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
                        expense_month_travel = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, sale_date__month=thismonth, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
                        print('expense_year_travel=',expense_year_travel)
                        print('thisyear at list2',thisyear)
                        print('thismonth at list2',thismonth)
                        
                        expense_year_vehicle = Expenses.objects.filter(item=veh.name, sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Vehicle')
                        expense_year_gas = Expenses.objects.filter(item=veh.name, sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Gas')
                        expense_month_vehicle = Expenses.objects.filter(item=veh.name, sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Vehicle')
                        expense_month_gas = Expenses.objects.filter(item=veh.name, sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Gas')
                        print('expense_year_vehicle',expense_year_vehicle)
                        print('expense_month_vehicle',expense_month_vehicle)
                        print('expense_month_gas',expense_month_gas)
                        print('expense_year_gas',expense_year_gas)
                                         
                        travel_cost_month = 0
                        travel_miles_month = 0
                        for item in expense_month_travel:
                            print('in expense_month_travel item')
                            travel_cost_month = travel_cost_month + (float(item.total_cost))
                            get_travel_miles = Equations(0,0)
                            travel_miles = get_travel_miles.get_num(item.item_desc)
                            travel_miles_month = travel_miles_month + travel_miles
                        
                        print('travel_cost_month=',travel_cost_month)
                        mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
                        print('mile=',mile)
                        for miles in mile:
                            print('miles=',miles.monthy_miles)
                            monthly_mile = monthly_mile + (float(miles.monthy_miles))
                            print('monthly_mile=',monthly_mile)
                        
                        if monthly_mile == 0:
                            taxable_percent_month = 0
                        else:
                            taxable_percent_month = travel_miles_month/monthly_mile
                        print('taxable_percent_month=',taxable_percent_month)
                        for item in expense_month_gas:
                            fuel_vehicle_month = payments_vehicle_month + float(item.total_cost) 
                            fuel_vehicle_month_taxable = (fuel_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                            vehicle_month = vehicle_month + float(item.total_cost)
                            vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_month)))
                            print('in month gas',fuel_vehicle_month )
                                
                        for item in expense_month_vehicle:
                            print('item-',item)
                            if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                                payments_vehicle_month = (payments_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                                payments_vehicle_month_taxable = (payments_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                                print('payments_vehicle_month=',payments_vehicle_month)
                                print('vehicle_month_taxable=',vehicle_month_taxable)
                                print('vehicle_month=',vehicle_month)
                            elif search('VEHICLE', item.expense_description.upper()) and search('INTEREST', item.expense_description.upper()):
                                interest_vehicle_month = interest_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                                interest_vehicle_month_taxable = vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = vehicle_month + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_month)))
                            elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                                insurance_vehicle_month = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                insurance_vehicle_month_taxable = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost))  * (float(taxable_percent_month))
                            elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                                tax_vehicle_month = (tax_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                                tax_vehicle_month_taxable = (tax_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) * (float(taxable_percent_month))
                            elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                                repair_vehicle_month = repair_vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                                repair_vehicle_month_taxable = (repair_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                            elif search('VEHICLE', item.expense_description.upper()) and search('OIL', item.expense_description.upper()):
                                mantenance_vehicle_month = mantenance_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                                mantenance_vehicle_month_taxable = (mantenance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                                vehicle_month = vehicle_month + float(item.total_cost)
                            elif search('VEHICLE', item.expense_description.upper()) and search('TIRES', item.expense_description.upper()):
                                tire_vehicle_month = tire_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                                tire_vehicle_month_taxable = (tire_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                                vehicle_month = vehicle_month + float(item.total_cost)
                                vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                                vehicle_month = vehicle_month + float(item.total_cost)
                            
                         
                        
                        travel_cost_year = 0
                        travel_miles_year = 0
                        year_miles = 0
                        for item in expense_year_travel:
                            print('in expense_month_travel item')
                            travel_cost_year = travel_cost_year + (float(item.total_cost))
                            get_travel_miles = Equations(0,0)
                            travel_miles = get_travel_miles.get_num(item.item_desc)
                            travel_miles_year = travel_miles_year + travel_miles
                        print('travel_cost_year=',travel_cost_year)
                        mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
                        print('mile=',mile)
                        for miles in mile:
                            print('year_miles=',miles.monthy_miles * int(thismonth))
                            year_miles = year_miles + (float(miles.monthy_miles *  int(thismonth)))
                            print('year_miles=',year_miles)
                        
                        if year_miles==0:
                            taxable_percent_year = 0
                        else:
                            taxable_percent_year = travel_miles_year/year_miles 
                        print('yearly taxable_percent=',taxable_percent_year)
                       
                        vehicle_year_taxable=0
                        for item in expense_year_gas:
                            fuel_vehicle_year = fuel_vehicle_year + float(item.total_cost)
                            fuel_vehicle_year_taxable = (fuel_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                            vehicle_year = vehicle_year + float(item.total_cost)
                            vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_year)))
                            print('in year gas',fuel_vehicle_year )
                        
                        payments_vehicle_year=0
                        for item in expense_year_vehicle:
                            print('item-',item)
                            if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                                payments_vehicle_year = (payments_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                                payments_vehicle_year_taxable = (payments_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                                print('payments_vehicle_year=',payments_vehicle_year)
                                print('vehicle_year_taxable=',vehicle_year_taxable)
                                print('vehicle_year=',vehicle_year)
                            elif search('VEHICLE', item.expense_description.upper()) and search('INSPECTION', item.expense_description.upper()):
                                inspection_vehicle_year = inspection_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                                inspection_vehicle_year_taxable = inspection_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = vehicle_year + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_year)))
                            elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                                insurance_vehicle_year = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                insurance_vehicle_year_taxable = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost))  * (float(taxable_percent_year))
                            elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                                tax_vehicle_year = (tax_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                                tax_vehicle_year_taxable = (tax_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) * (float(taxable_percent_year))
                            elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                                repair_vehicle_year = repair_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                                repair_vehicle_year_taxable = (repair_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                            elif search('GAS', item.expense_description.upper()):
                                fuel_vehicle_year = fuel_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                                fuel_vehicle_year_taxable = (fuel_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_year)))
                            elif search('VEHICLE', item.expense_description.upper()) and (search('OIL', item.expense_description.upper()) or search('TIRES', item.expense_description.upper())):
                                mantenance_vehicle_year = mantenance_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                                mantenance_vehicle_year_taxable = (mantenance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                            elif search('VEHICLE', item.expense_description.upper()) and search('TIRES', item.expense_description.upper()):
                                tire_vehicle_year = tire_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                                tire_vehicle_year_taxable = (tire_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                                vehicle_year = vehicle_year + float(item.total_cost)
                                vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                        
                        
                        print('vehicle_month',vehicle_month)
                        print('vehicle_month_taxable',vehicle_month_taxable)
                        print('vehicle_year_taxable',vehicle_year_taxable)
                        print ('payments_vehicle_year_taxable',payments_vehicle_year_taxable)
                        total_taxed_v  =  [vehicle_year,vehicle_year_taxable]
                
                if uploaded_file_url==None or uploaded_file_url =="":
                    uploaded_file_url = '/media/images/vehicle.png'
                print('uploaded_file_url =',uploaded_file_url)
            except IOError as e:
                print ("load vehicle Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/vehicle.html",{'form': form, 'image':image, "vehicles": vehicles, "veh":veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle", 'month':month, 'year':year,'payment_month':vehicle_month, 
                                                            'payment_year':vehicle_year, 'insurance':insurance_vehicle_year, 'fuel_month':fuel_vehicle_month, 'fuel_year':fuel_vehicle_year, 'maintenance':mantenance_vehicle_year, 'repair':repair_vehicle_year, 'tires':tire_vehicle_year,
                                                            'inspection':inspection, 'operator':operator,'years':years,'duplicate':duplicate, 'business_use':business_use})
    
    def post(self, *args, **kwargs):
        timestamp = date.today()
        operator = str(self.request.user)
        dt = datetime.datetime.today()
        thisyear = dt.year
        thismonth = dt.month
        thisday = dt.day
        print('thismonth=',thismonth)
        print('thisyear=',thisyear)
        months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
        month = months[str(thismonth)]
        print('month =',month) 
        insurance=0
        payment_month=0
        payment_year=0
        fuel_month=0
        fuel_year=0
        maintenance=0
        repair=0;
        tires=0
        inspection=0
        veh=-1
        duplicate=-1
        vehicle_year=0
        vehicle_month=0
        payment_vehicle_year=0
        insurance_vehicle_year=0
        fuel_vehicle_year=0
        mantenance_vehicle_year=0
        repair_vehicle_year=0
        tires_vehicle_year=0
        vehicle_month_taxable=0
        payments_vehicle_month=0
        payments_vehicle_month=0
        insurance_vehicle_month=0
        interest_vehicle_month=0
        tax_vehicle_month=0
        repair_vehicle_month=0
        fuel_vehicle_month=0
        mantenance_vehicle_month=0
        tire_vehicle_month=0
        payments_vehicle_month_taxable=0
        payments_vehicle_month_taxable=0
        insurance_vehicle_month_taxable=0
        interest_vehicle_month_taxable=0
        tax_vehicle_month_taxable=0
        repair_vehicle_month_taxable=0
        fuel_vehicle_month_taxable=0
        mantenance_vehicle_month_taxable=0
        tires_vehicle_month_taxable=0
        image = -1
        image_file =-1
                    
        business_use = self.request.POST.get('_use',-1)
        if business_use =='on':
            business_use_s = True
        else:
            business_use_s = False
        print('business_use=',business_use)
        name = self.request.POST.get('_name',-1)
        print('name=',name)
        make = self.request.POST.get('_make',-1)
        print('make=',make)
        load = self.request.POST.get('_load',-1)
        print('load=',load)
        type = self.request.POST.get('_type',-1) #Make
        print('type=',type)
        model = self.request.POST.get('_model',-1)
        print('model=',model)
        year= self.request.POST.get('_year',-1)
        print('year=',year)
        owner= self.request.POST.get('_owner',-1)
        print('owner=',owner)
        
        load= self.request.POST.get('_load',-1)
        if load==-1:
            load = 0
        print('load=',load)
        orig_miles= self.request.POST.get('_orig_miles',-1)
        if orig_miles==-1:
            orig_miles = 0
        print('orig_miles=',orig_miles)
        orig_val= self.request.POST.get('_orig_val',-1)
        if orig_val==-1:
            orig_val = 0
        print('orig_val=',orig_val)
        active_miles= self.request.POST.get('_active_miles',-1)
        if active_miles==-1:
            active_miles = 0
        print('active_miles=',active_miles)
        miles= self.request.POST.get('_miles',-1)
        if miles==-1:
            miles = 0
        print('miles=',miles)
        miles_save=miles
        years = []
        #year = datetime.date.today().year
        year = self.request.POST.get('_year',-1)
        year = 2018
        print('year=',year)
        for i in range(-40,0):
            years.append(year+i)
        veh_id = self.request.POST.get('veh_id', -1)
        vehicles=Vehical.objects.all()
        print('vehicles=',vehicles)
        print('veh_id=',veh_id)
        uploaded_file_url=-1
        form = VehicleForm()
        payment_vehicle_month = 0
        if veh_id !=-1 and veh_id !='':
            veh = Vehical.objects.filter(id=veh_id).all()
            print('veh=',veh)
            veh=veh[0]
            print('veh=',veh)
            print('veh.image',veh.image)
            print('veh.business_use',veh.business_use)
            uploaded_file_url=veh.image
            print('uploaded_file_url',uploaded_file_url)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vehicle Expenses~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print('thisyear at list2',thisyear)
            print('thismonth at list2',thismonth)
            expense_year_travel = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
            expense_month_travel = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, sale_date__month=thismonth, expense_type__icontains='Travel', expense_description__icontains='Travel').all()
                        
            expense_year_vehicle = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Vehicle')
            expense_year_gas = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, expense_type ='Assets',expense_description__icontains='Gas')
            expense_month_vehicle = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Vehicle')
            expense_month_gas = Expenses.objects.filter(item=veh.name,sale_date__year=thisyear, sale_date__month=thismonth, expense_type ='Assets',expense_description__icontains='Gas')
            print('expense_year_vehicle',expense_year_vehicle)
            print('expense_month_vehicle',expense_month_vehicle)
            print('expense_month_gas',expense_month_gas)
            print('expense_year_gas',expense_year_gas)
                             
            
            travel_cost_month = 0
            travel_miles_month = 0
            for item in expense_month_travel:
                print('in expense_month_travel item')
                travel_cost_month = travel_cost_month + (float(item.total_cost))
                get_travel_miles = Equations(0,0)
                travel_miles = get_travel_miles.get_num(item.item_desc)
                travel_miles_month = travel_miles_month + travel_miles
            
            print('travel_cost_month=',travel_cost_month)
            mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
            print('mile=',mile)
            monthly_mile=0
            for miles in mile:
                print('miles=',miles.monthy_miles)
                monthly_mile = monthly_mile + (float(miles.monthy_miles))
                print('monthly_mile=',monthly_mile)
            
            if monthly_mile == 0:
                taxable_percent_month = 0
            else:
                taxable_percent_month = travel_miles_month/monthly_mile
            print('taxable_percent_month=',taxable_percent_month)
            
            for item in expense_month_gas:
                fuel_vehicle_month = fuel_vehicle_month + float(item.total_cost) 
                fuel_vehicle_month_taxable = (fuel_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                vehicle_month = vehicle_month + float(item.total_cost)
                vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_month)))
                print('in month gas',fuel_vehicle_month )
                    
            for item in expense_month_vehicle:
                print('item-',item)
                if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                    payments_vehicle_month = (payments_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                    payments_vehicle_month_taxable = (payments_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    print('payments_vehicle_month=',payments_vehicle_month)
                    print('vehicle_month_taxable=',vehicle_month_taxable)
                    print('vehicle_month=',vehicle_month)
                elif search('VEHICLE', item.expense_description.upper()) and search('INTEREST', item.expense_description.upper()):
                    interest_vehicle_month = interest_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    interest_vehicle_month_taxable = vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = vehicle_month + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_month)))
                elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                    insurance_vehicle_month = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    insurance_vehicle_month_taxable = (insurance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost))  * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                    tax_vehicle_month = (tax_vehicle_month + (float(item.total_cost)) * (float(taxable_percent_month)))
                    tax_vehicle_month_taxable = (tax_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month_taxable + float(item.total_cost)) * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                    repair_vehicle_month = repair_vehicle_month_taxable + (float(item.total_cost) * (float(taxable_percent_month)))
                    repair_vehicle_month_taxable = (repair_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                elif search('VEHICLE', item.expense_description.upper()) and search('OIL', item.expense_description.upper()):
                    mantenance_vehicle_month = mantenance_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    mantenance_vehicle_month_taxable = (mantenance_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    vehicle_month = vehicle_month + float(item.total_cost)
                elif search('VEHICLE', item.expense_description.upper()) and search('TIRES', item.expense_description.upper()):
                    tire_vehicle_month = tire_vehicle_month + (float(item.total_cost) * (float(taxable_percent_month)))
                    tire_vehicle_month_taxable = (tire_vehicle_month_taxable + (float(item.total_cost)) * (float(taxable_percent_month)))
                    vehicle_month = vehicle_month + float(item.total_cost)
                    vehicle_month_taxable = (vehicle_month + float(item.total_cost))  * (float(taxable_percent_month))
                    vehicle_month = vehicle_month + float(item.total_cost)
            
            payments_vehicle_year_taxable=0
            payments_vehicle_year_taxable=0
            insurance_vehicle_year_taxable=0
            inspection_vehicle_year_taxable=0
            tax_vehicle_year_taxable=0
            repair_vehicle_year_taxable=0
            fuel_vehicle_year_taxable=0
            mantenance_vehicle_year_taxable=0
            tire_vehicle_year_taxable=0
            payments_vehicle_year=0
            payments_vehicle_year=0
            insurance_vehicle_year=0
            inspection_vehicle_year=0
            tax_vehicle_year=0
            repair_vehicle_year=0
            fuel_vehicle_year=0
            mantenance_vehicle_year=0
            tires_vehicle_year=0
            
            travel_cost_year = 0
            travel_miles_year = 0
            year_miles = 0
            for item in expense_year_travel:
                print('in expense_month_travel item')
                travel_cost_year = travel_cost_year + (float(item.total_cost))
                get_travel_miles = Equations(0,0)
                travel_miles = get_travel_miles.get_num(item.item_desc)
                travel_miles_year = travel_miles_year + travel_miles
            print('travel_cost_year=',travel_cost_year)
            mile = Vehical.objects.filter(last_update__year=thisyear,business_use=True).all()
            print('mile=',mile)
            for miles in mile:
                print('year_miles=',miles.monthy_miles * int(thismonth))
                year_miles = year_miles + (float(miles.monthy_miles *  int(thismonth)))
                print('year_miles=',year_miles)
            
            if year_miles==0:
                taxable_percent_year = 0
            else:
                taxable_percent_year = travel_miles_year/year_miles 
            print('yeary taxable_percent=',taxable_percent_year)
           
            vehicle_year_taxable=0
            for item in expense_year_gas:
                fuel_vehicle_year = fuel_vehicle_year + float(item.total_cost) 
                fuel_vehicle_year_taxable = (fuel_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                vehicle_year = vehicle_year + float(item.total_cost)
                vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) + (float(item.total_cost) * (float(taxable_percent_year)))
                print('in year gas',fuel_vehicle_year )
            
            for item in expense_year_vehicle:
                print('item-',item)
                if search('VEHICLE', item.expense_description.upper()) and search('PAYMENT', item.expense_description.upper()):
                    payments_vehicle_year = (payments_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                    payments_vehicle_year_taxable = (payments_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                    print('payments_vehicle_year=',payments_vehicle_year)
                    print('vehicle_year_taxable=',vehicle_year_taxable)
                    print('vehicle_year=',vehicle_year)
                elif search('VEHICLE', item.expense_description.upper()) and search('INSPECTION', item.expense_description.upper()):
                    inspection_vehicle_year = inspection_vehicle_year + (float(item.total_cost) * (float(taxable_percent_year)))
                    inspection_vehicle_year_taxable = inspection_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = vehicle_year + float(item.total_cost) + (float(item.total_cost) * (float(taxable_percent_year)))
                elif search('VEHICLE', item.expense_description.upper()) and search('INSURANCE', item.expense_description.upper()):
                    insurance_vehicle_year = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    insurance_vehicle_year_taxable = (insurance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('TAX', item.expense_description.upper()):
                    tax_vehicle_year = (tax_vehicle_year + (float(item.total_cost)) * (float(taxable_percent_year)))
                    tax_vehicle_year_taxable = (tax_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year_taxable + float(item.total_cost)) * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('REPAIR', item.expense_description.upper()):
                    repair_vehicle_year = repair_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    repair_vehicle_year_taxable = (repair_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and (search('OIL', item.expense_description.upper()) or search('TIRES', item.expense_description.upper())):
                    mantenance_vehicle_year = mantenance_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    mantenance_vehicle_year_taxable = (mantenance_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
                elif search('VEHICLE', item.expense_description.upper()) and search('TIRES', item.expense_description.upper()):
                    tire_vehicle_year = tire_vehicle_year_taxable + (float(item.total_cost) * (float(taxable_percent_year)))
                    tire_vehicle_year_taxable = (tire_vehicle_year_taxable + (float(item.total_cost)) * (float(taxable_percent_year)))
                    vehicle_year = vehicle_year + float(item.total_cost)
                    vehicle_year_taxable = (vehicle_year + float(item.total_cost))  * (float(taxable_percent_year))
            
            print('vehicle_month',vehicle_month)
            print('vehicle_month_taxable',vehicle_month_taxable)
            print('vehicle_year_taxable',vehicle_year_taxable)
            print ('payments_vehicle_year_taxable',payments_vehicle_year_taxable)
            total_taxed_v  =  [vehicle_year,vehicle_year_taxable]
        image_file_name = self.request.FILES.get('uploaded_file')
        print('image_file_name',image_file_name)
        if image_file_name !=None:
            image_file_content = self.request.FILES['uploaded_file'].read()
            #print('image_file_content=',image_file_content)
            
        image_file=image_file_name
        print('image_file',image_file)
        
        save = self.request.POST.get('_save',-1)
        print('save',save)
        update = self.request.POST.get('_update',-1)
        print('update',update)
        delete = self.request.POST.get('_delete',-1)
        print('delete',delete)
        if not save==None and save !=-1:	
            print('in save')
            try:		
                if Vehical.objects.filter(name=name).exists() or name =='***Name must be unique!!***':
                    duplicate=1
                    return render(self.request,"assets/vehicle.html",{'form': form, 'image':image, 'image_file':image_file, "vehicles": vehicles, "veh":veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle", 'month':month, 'year':year,'payment_month':payment_vehicle_month, 
                                                            'payment_year':payment_vehicle_year, 'insurance':insurance_vehicle_year, 'fuel_month':fuel_vehicle_month, 'fuel_year':fuel_vehicle_year, 'maintenance':mantenance_vehicle_year, 'repair':repair_vehicle_year, 'tires':tires_vehicle_year,
                                                            'inspection':inspection, 'operator':operator,'years':years,'duplicate':duplicate, 'business_use':business_use})
                else:
                    Vehical.objects.create(name=name, make=make, model=model,type=type,year=year,original_miles=orig_miles, active_miles=active_miles, original_value=orig_val,
                                          load_limit=load, ownership=owner, cost=orig_val, monthy_miles=miles_save, last_update=timestamp,business_use=business_use_s)
            
                    veh =Vehical.objects.filter(name=name)
                    print('veh=',veh[0])
                    form = VehicleForm(self.request.POST, self.request.FILES, instance = veh[0], use_required_attribute=False)
                    print('form',form)       
                    if form.is_valid():
                        print('form is valid')
                        form.save()
                        veh =Vehical.objects.filter(id=veh[0].id)
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==None and update !=-1: 
            try:
                print('in update_mkik')
                print('year=',year)
                #update existing vehicle
                
                Vehical.objects.filter(id=veh_id).update(name=name, make=make, model=model, type=type, year=year,original_miles=orig_miles, active_miles=active_miles, original_value=orig_val, 
                                                load_limit=load, ownership=owner, cost=orig_val, monthy_miles=miles_save, last_update=timestamp,business_use=business_use_s)
                
                veh =Vehical.objects.filter(id=veh_id)
                print('veh=',veh[0])
                form = VehicleForm(self.request.POST, self.request.FILES, instance = veh[0],use_required_attribute=False)
                print('form',form)       
                if form.is_valid():
                    print('form is valid')
                    form.save()
                    veh =Vehical.objects.filter(id=veh_id)
               
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None and delete !=-1: 
            print('in update')
            try:
                Vehical.objects.filter(id=veh_id).delete()
            except IOError as e:
                print ("load vehicle Failure ", e)
                print('error = ',e) 
        return render(self.request,"assets/vehicle.html",{'form': form, 'image':image, 'image_file':image_file, "vehicles": vehicles, "veh":veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle", 'month':month, 'year':year,'payment_month':payments_vehicle_month, 
                                                            'payment_year':payments_vehicle_year, 'insurance':insurance_vehicle_year, 'fuel_month':fuel_vehicle_month, 'fuel_year':fuel_vehicle_year, 'maintenance':mantenance_vehicle_year, 'repair':repair_vehicle_year, 'tires':tires_vehicle_year,
                                                             'inspection':inspection, 'operator':operator,'years':years,'duplicate':duplicate, 'business_use':business_use})
                                                            
class BuildingView(View):
    template_name = "building.html"
    success_url = reverse_lazy('assets:building')
    def get(self, *args, **kwargs):
            buildings_list = []
            veh = []
            uploaded_file_url=None
            print('we are here in building get')
            # cast the request inventory_id from string to integer type.
            success = True 
            try:	
                main_building = 'MAIN'
                sqr_feet = -1
                payment_cost = -1
                power_cost = -1
                internet_cost = -1
                fuel_cost = -1
                maintenance_cost = -1
                build_space = -1
                building = -1
                space_percentage = -1
                power_percentage = -1
                internet_percentage = -1
                insurance_percentage = -1
                fuel_percentage = -1
                duplicate=-1
                form = Business_SpaceForm()
                space_id = self.request.GET.get('space_id', -1)
                print('space_id = ',space_id)
                buildings_list=Location.objects.order_by('name').values_list('name', flat=True).distinct()
                space_type = self.request.GET.get('space_type', -1)
                spaces = Business_Space.objects.all()
                print('space_type=',space_type)
                if space_type==-1:
                    main_building = 'MAIN'
                elif space_type.find('MAIN')!=-1:
                    main_building = 'MAIN'
                else:
                    main_building = 'SPACE'
                    
                media_folder = settings.MEDIA_URL 
                print('media_folder = ',media_folder)
                if space_id!=-1:
                    build_space = Business_Space.objects.filter(id=space_id).all()
                    print('build_space = ',build_space)
                    build_space=build_space[0]
                    building = build_space.building
                    print('building',building)
                    print('build_space.image_file',build_space.image)
                    uploaded_file_url=str(build_space.image)
                
                if uploaded_file_url==None or uploaded_file_url =="":
                    uploaded_file_url = '/media/images/building_space.png'
                print('uploaded_file_url =',uploaded_file_url)
            except IOError as e:
                print ("load building Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/building.html",{'form': form, 'main_building':main_building, 'space_id':space_id, 'spaces':spaces, "buildings_list": buildings_list, "build_space": build_space, "uploaded_file_url":uploaded_file_url,  "index_type":"building", 
                                                            'space_percentage':space_percentage,'power_percentage':power_percentage, 'internet_percentage':internet_percentage, 'insurance_percentage':insurance_percentage, 'fuel_percentage':fuel_percentage,'duplicate':duplicate,
                                                            'space_type':space_type, 'building':building, 'sqr_feet':sqr_feet, 'payment_cost':payment_cost, 'power_cost':power_cost, 'internet_cost':internet_cost, 'fuel_cost':fuel_cost, 'maintenance_cost':maintenance_cost })
    
    def post(self, *args, **kwargs):
        timestamp = date.today()
        building = self.request.POST.get('_building',-1)
        print('building=',building)
        space_id = int(self.request.POST.get('_space_id', -1))
        print('space_id=',space_id)
        space = self.request.POST.get('_space', -1)
        print('space=',space)
        space_type = self.request.POST.get('_type',-1)
        print('space_type=',space_type)
        spaces = []
        buildings_list = []
        build_space = -1
       
        if space_type.find('MAIN') !=-1:
            print('in main')
            main_building = 'MAIN'
            space_percentage = 0
            power_percentage = 0
            internet_percentage = 0
            insurance_percentage = 0
            fuel_percentage = 0
            sqr_feet = self.request.POST.get('_sqr_feet',-1)
            payment_cost = self.request.POST.get('_payment_cost',-1)
            power_cost = self.request.POST.get('_power_cost',-1)
            internet_cost = self.request.POST.get('_internet_cost',-1)
            fuel_cost = self.request.POST.get('_fuel_cost',-1)
            maintenance_cost = self.request.POST.get('_maintenance_cost',-1)
        else:     
            print('in not main')
            main_building = 'SPACE'
            space_percentage = self.request.POST.get('_space',-1)
            power_percentage = self.request.POST.get('_power',-1)
            internet_percentage = self.request.POST.get('_internet',-1)
            insurance_percentage = self.request.POST.get('_insurance',-1)
            fuel_percentage = self.request.POST.get('_fuel',-1)
            sqr_feet = 100
            payment_cost = 100
            power_cost = 100
            internet_cost = 100
            fuel_cost = 100
            maintenance_cost = 100
       
        active = True
        image_file = self.request.POST.get('_image',-1)
        save = self.request.POST.get('_save',-1)
        print('save=',save)
        update = self.request.POST.get('_update',-1)
        print('update =',update )
        delete = self.request.POST.get('_delete',-1)
        print('delete=',delete)
        duplicate=-1
        print('space_id=',space_id)
        
        uploaded_file_url=-1
        buildings_list=Location.objects.order_by('name').values_list('name', flat=True).distinct()
        spaces = Business_Space.objects.all()
        form = Business_SpaceForm(self.request.POST, self.request.FILES)
        if save!=-1:	
            try:		
                if Business_Space.objects.filter(building=building,type=space_type).exists():
                    duplicate=1
                    build_space = Business_Space.objects.filter(building=building,type=space_type)
                    return render(self.request,"assets/building.html",{'main_building':main_building, 'space_id':space_id, 'spaces':spaces, "buildings_list": buildings_list, "build_space": build_space, "uploaded_file_url":uploaded_file_url,  "index_type":"building", 
                                                            'space_percentage':space_percentage,'power_percentage':power_percentage, 'internet_percentage':internet_percentage, 'insurance_percentage':insurance_percentage, 'fuel_percentage':fuel_percentage,'duplicate':duplicate,
                                                            'space_type':space_type, 'building':building, 'sqr_feet':sqr_feet, 'payment_cost':payment_cost, 'power_cost':power_cost, 'internet_cost':internet_cost, 'fuel_cost':fuel_cost, 'maintenance_cost':maintenance_cost })
                else:
                    Business_Space.objects.create(building=building, type=space_type, space_percentage=space_percentage, power_percentage=power_percentage, internet_percentage=internet_percentage, 
                                                    sqr_feet=sqr_feet,payment_cost=payment_cost,power_cost=power_cost,internet_cost=internet_cost,fuel_cost=fuel_cost,maintenance_cost=maintenance_cost,
                                                    insurance_percentage=insurance_percentage, fuel_percentage=fuel_percentage, last_update=timestamp)
                    b=Business_Space.objects.filter(building=building,type=space_type)
                    Location.objects.filter(name=building).update(Business_Space=b[0])
                    form = Business_SpaceForm(self.request.POST, self.request.FILES, instance = b[0], use_required_attribute=False)
                    print('form',form)       
                    if form.is_valid():
                        print('form is valid')
                        form.save()
                    build_space=Business_Space.objects.filter(building=building,type=space_type)
                    uploaded_file_url=str(build_space[0].image)    
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif update!=-1: 
            try:
                #update existing event
                print('in update')
                print('space_id',space_id)
                Business_Space.objects.filter(id=space_id).update(building=building, type=space_type, space_percentage=space_percentage, power_percentage=power_percentage, internet_percentage=internet_percentage, 
                                                    sqr_feet=sqr_feet,payment_cost=payment_cost,power_cost=power_cost,internet_cost=internet_cost,fuel_cost=fuel_cost,maintenance_cost=maintenance_cost,
                                                    insurance_percentage=insurance_percentage, fuel_percentage=fuel_percentage, last_update=timestamp)
                
                print('space_type=',space_type)
                print('building=',building)
                b=Business_Space.objects.filter(building=building,type=space_type)
                Location.objects.filter(name=building).update(Business_Space=b[0])
                form = Business_SpaceForm(self.request.POST, self.request.FILES, instance = b[0], use_required_attribute=False)
                      
                if form.is_valid():
                    print('form is valid')
                    form.save()
                else:
                    print('form is invalid')
                print('updated location')
                print('building',building) 
                print('space_type',space_type) 
                build_space=Business_Space.objects.get(building=building,type=space_type)
                print('build_space',build_space) 
                uploaded_file_url=str(build_space.image)
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif delete!=-1: 
            try:
               print('in delete')
               print('space_id',space_id)
               Business_Space.objects.filter(id=space_id).delete()
            except IOError as e:
                print ("load vehicle Failure ", e)
                print('error = ',e) 
        return render(self.request,"assets/building.html",{'form': form, 'main_building':main_building, 'space_id':space_id, 'spaces':spaces, "buildings_list": buildings_list, "build_space": build_space, "uploaded_file_url":uploaded_file_url,  "index_type":"building", 
                                                            'space_percentage':space_percentage,'power_percentage':power_percentage, 'internet_percentage':internet_percentage, 'insurance_percentage':insurance_percentage, 'fuel_percentage':fuel_percentage,'duplicate':duplicate,
                                                            'space_type':space_type, 'building':building, 'sqr_feet':sqr_feet, 'payment_cost':payment_cost, 'power_cost':power_cost, 'internet_cost':internet_cost, 'fuel_cost':fuel_cost, 'maintenance_cost':maintenance_cost   })

def loadmodel(request, model_id):
        models = []
        mod = []
        print('we are here')
        # cast the request inventory_id from string to integer type.
        model_id = int(model_id)
        success = True 
        try:	
            models=Model.objects.all()
            mod=Model.objects.filter(id=model_id)
            mod=mod[0]
            print('mod.image_file',mod.image_file)
            uploaded_file_url=mod.photo
            if uploaded_file_url==None or uploaded_file_url =="":
                uploaded_file_url = '/media/office1.jpg'
            print('uploaded_file_url =',uploaded_file_url)
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url,  "index_type":"Model"})
        
def newmodel(request):
        models = []
        success = True 
        try:	
            mod = -1
            models=Model.objects.all()
            image_file = 'inv1.jpg'
            uploaded_file_url = '/tcli/media/inv1.jpg'
                       
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"assets/model.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url, "image_file":image_file,  "index_type":"Model"})

@login_required
def showimage(request):
    image_file = -1
    if request.method == 'POST': 
        form = ModelsForm(request.POST, request.FILES)
        print('form =',form)
        model_id=308
        print('model_id =',model_id)       
        instance = Model.objects.get(id=model_id)
        print('instance =',instance) 
        form = ModelsForm(request.POST or None, instance=instance)
            
        #print('imagefile =',imagefile)
        media_folder = settings.MEDIA_URL
        print('media_folder = ',media_folder)
        #file_path = media_folder+image_file
        #image_file = media_folder + imagefile
        
        #os.rename(file_path,image_file)
       
        if form.is_valid(): 
            form.save() 
    else: 
        form = ModelsForm()
        imagefile = request.POST.get('photo',-1)
        #print('imagefile =',imagefile)
    return render(request, 'assets/images.html', {'form' : form}) 
        
        
def loadpersonnel(request, model_id):
        personnel = []
        mod = []
        print('we are here')
        # cast the request inventory_id from string to integer type.
        model_id = int(model_id)
        success = True 
        try:	
            personnel=Model.objects.all()
            mod=Model.objects.filter(id=model_id)
            mod=mod[0]
            print('mod.image_file',mod.image_file)
            uploaded_file_url=mod.photo
            if uploaded_file_url==None or uploaded_file_url =="":
                uploaded_file_url = '/ats/media/inv1.jpg'
            print('uploaded_file_url =',uploaded_file_url)
        except IOError as e:
            print ("load personnel Failure ", e)
            print('error = ',e) 
        return render(request,"assets/personnel.html",{"personnel": personnel, "mod": mod, "uploaded_file_url":uploaded_file_url,  "index_type":"personnel"})
        
def newpersonnel(request):
        models = []
        success = True 
        try:	
            mod = -1
            models=Model.objects.all()
            image_file = 'inv1.jpg'
            uploaded_file_url = '/ats/media/inv1.jpg'
                       
        except IOError as e:
            print ("load personnel Failure ", e)
            print('error = ',e) 
        return render(request,"assets/personnel.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url, "image_file":image_file,  "index_type":"personnel"})


def showimage(request):
    image_file = -1
    if request.method == 'POST': 
        print('form =',form)
        model_id=308
        print('model_id =',model_id)       
        instance = Model.objects.get(id=model_id)
        print('instance =',instance) 
        form = ModelsForm(request.POST or None, instance=instance)
            
        #print('imagefile =',imagefile)
        media_folder = settings.MEDIA_URL
        print('media_folder = ',media_folder)
        #file_path = media_folder+image_file
        #image_file = media_folder + imagefile
        
        #os.rename(file_path,image_file)
       
        if form.is_valid(): 
            form.save() 
    else: 
        form = ModelsForm()
        imagefile = request.POST.get('photo',-1)
        #print('imagefile =',imagefile)
    return render(request, 'assets/images.html', {}) 
   
def loadassests():
    import csv
    contSuccess = 0
    CSV_PATH = 'models.csv'
    print('csv = ',CSV_PATH)
    
    # Remove all data from Table
    Model.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for description, category, band, vendor, model, comments, image_file, status, last_update in reader:
        print(description)
        print (band)
        print(vendor)
        print(model)
        print(comments)
        print(image_file)
        print(status)
        print(last_update)
        Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, comments=comments, image_file=image_file, status=status, last_update=datetime.datetime.strptime(last_update, '%m/%d/%Y'))
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
 


def saveasset(request):
    if request.method == 'POST':
        model_id = request.POST.get('m_id',-1)
        models = Model.objects.all()
        print('model_id=',model_id)
        mod = Model.objects.filter(id__contains=model_id)
        mod=mod[0]
        print('mod=',mod)
        try:        
            image_file = request.FILES.get('_upload',-1)
        except IOError as e:
             image_file = -1
        print('image_file=',image_file)  
        if image_file==-1 or image_file=='inv1.jpg' or image_file== None or image_file== "":
            image_file = mod.image_file
            print(image_file)
            uploaded_file_url = mod.photo
            print('uploaded_file_url =',uploaded_file_url )
        else:    
            myfile = request.FILES['_upload']
            print('MYFILE =', myfile)
            fs = FileSystemStorage()
            print('fs=',fs)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print('uploaded_file_url =',uploaded_file_url )
            print(image_file)
            
        if uploaded_file_url == None or uploaded_file_url =="":
            uploaded_file_url='/tcli/media/inv1.jpg' 
            image_file='inv1.jpg'
        
        timestamp = date.today()
        band = request.POST.get('_band',-1)
        category = request.POST.get('_category',-1)
        description = request.POST.get('_desc',-1)
        model = request.POST.get('_model',-1)
        vendor= request.POST.get('_vendor',-1)
        active = True
        comments = request.POST.get('_com',-1)
        if comments==-1:
            comments=""
        print('comments=',comments)
        save = request.POST.get('_save',-1)
        update = request.POST.get('_update',-1)
        delete = request.POST.get('_delete',-1)
        
                      
        if not save==-1:	
            try:		
                Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, comments=comments, 
                            image_file=image_file, photo=uploaded_file_url, status=active, last_update=timestamp)
                if pic_form.is_valid():
                    pic_form.save()
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==-1: 
            try:
                #update existing event
                Model.objects.filter(id=model_id).update(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, image_file=image_file, photo=uploaded_file_url, status=active, last_update=timestamp)
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==-1: 
            try:
                Model.objects.filter(id=model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render(request,"assets/model.html",{"models": models, "mod": mod, "image_file":image_file, 'uploaded_file_url':uploaded_file_url,  "index_type":"Model"})   