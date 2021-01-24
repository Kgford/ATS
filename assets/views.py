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
from assets.models import Personnel,Vehical,Business_Space, Product
from vendor.models import Vendor
from contractors.models import Contractors
from .models import Vehical
from .forms import *
from django.views import View
import datetime
from collections import OrderedDict
from ATS.overhead import Equations
from re import search
from ATS.overhead import Comunication
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

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
            message = 'message'
            #com=Comunication(phone,message)
            #print('com=',com)
            #com.send_sms()
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
            building_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            building_year = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            space_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            space_year = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
           
            if veh_id!=-1:
                veh = Model.objects.filter(id=veh_id).all()
                veh=veh[0]
                print(veh)
            timestamp = date.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            thismonth = dt.month
            thisday = dt.day
            print('thismonth=',thismonth)
            print('thisyear=',thisyear)
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            month = months[str(thismonth)]
            print('month =',month)    
            print(vehicles)
        except IOError as e:
            print ("Lists load Failure ", e) 
            
            print('error = ',e) 
        return render (self.request,"assets/index.html",{"personnel": personnel, "spaces": spaces, "vehicles": vehicles, "veh":veh, "index_type":"assests",'avatar':avatar, 'year_list':year_list, 'month_list':month_list,
                                         'building_month':building_month,'building_year':building_year,'space_month':space_month, 'space_year':space_year, 'month_full':month_full,'month':month,'year':thisyear,})
        
    def post(self, *args, **kwargs):
        timestamp = date.today()
        dt = datetime.datetime.today()
        thisyear = dt.year
        thismonth = dt.month
        thisday = dt.day
        print('thismonth=',thismonth)
        print('thisyear=',thisyear)
        months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
        month = months[str(thismonth)]
        print('month =',month) 
        operator = str(self.request.user)
        band = request.POST.POST('_band',-1)
        category = request.POST.get('_category',-1)
        description = request.POST.get('_desc',-1)
        model = request.POSTget('_model',-1)
        vendor= request.POST.get('_vendor',-1)
        active = True
        image_file = request.POST.get('fileupload',-1)
        comments = request.POST.get('_comments',-1)
        model_id = request.POST.get('m_id',-1)
        save = request.POST.get('_save',-1)
        update = request.POST.get('_update',-1)
        delete = request.POST.get('_delete',-1)
        
        if not save==None:	
            try:		
                Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, image_file=image_file, status=active, last_update=timestamp)
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==None: 
            try:
                #update existing event
                Model.objects.filter(id=model_id).update({'description': description,'category':category,'band=':band,
                    'model':model,'comment':comment,'locationname':locationname,'image_file':image_file,'vendor':vendor,'active':active,'last_update':last_update})
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None: 
            try:
                Model.objects.filter(id=model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render (self.request,"assets/index.html",{"form": form, "models": models, "index_type":"assests"})


class VehicleView(View):
    template_name = "vehicle.html"
    success_url = reverse_lazy('assets:vehicle')
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
                years = []
                year = datetime.date.today().year
                for i in range(-40,0):
                    years.append(year+i)
                vehicles=Vehical.objects.all()
                veh_id = self.request.GET.get('veh_id', -1)
                print('vehicles=',vehicles)
                print('veh_id=',veh_id)
                if veh_id!=-1:
                    media_folder = settings.MEDIA_URL + 'images/'
                    print('media_folder = ',media_folder)
                    veh = Vehical.objects.filter(id=veh_id).all()
                    print('veh=',veh)
                    veh=veh[0]
                    print('veh=',veh)
                    print('veh.image_file=',veh.image_file)
                    if veh.image_file != -1:
                        print('media_folder=',media_folder)
                        print('veh.image_file=',veh.image_file)
                        uploaded_file_url= media_folder + str(veh.image_file)
                
                if uploaded_file_url==None or uploaded_file_url =="":
                    uploaded_file_url = '/media/images/vehicle.png'
                print('uploaded_file_url =',uploaded_file_url)
            except IOError as e:
                print ("load vehicle Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/vehicle.html",{"vehicles": vehicles, "veh":veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle", 'month':month, 'year':year,'payment_month':payment_month, 
                                                            'payment_year':payment_year, 'insurance':insurance, 'fuel_month':fuel_month, 'fuel_year':fuel_year, 'maintenance':maintenance, 'repair':repair, 'tires':tires,
                                                            'inspection':inspection, 'operator':operator,'years':years,'duplicate':duplicate})
    
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
        
        years = []
        year = datetime.date.today().year
        for i in range(-40,0):
            years.append(year+i)
        veh_id = self.request.POST.get('veh_id', -1)
        vehicles=Vehical.objects.all()
        print('vehicles=',vehicles)
        print('veh_id=',veh_id)
        uploaded_file_url=-1
        if veh_id:
            veh = Vehical.objects.filter(id=veh_id).all()
            print('veh=',veh)
            veh=veh[0]
            print('veh=',veh)
            print('veh.image_file',veh.image_file)
            uploaded_file_url=veh.image_file
        
        image_file_content = self.request.FILES['uploaded_file'].read()
        print('image_file_content',image_file_content)
        image_file_name = self.request.FILES.get('uploaded_file')
        print('image_file_content',image_file_content)
        
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
                    return render(self.request,"assets/vehicle.html",{"vehicles": vehicles, "veh":veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle", 'month':month, 'year':year,'payment_month':payment_month, 
                                                            'payment_year':payment_year, 'insurance':insurance, 'fuel_month':fuel_month, 'fuel_year':fuel_year, 'maintenance':maintenance, 'repair':repair, 'tires':tires,
                                                            'inspection':inspection, 'operator':operator,'years':years,'duplicate':duplicate})
                else:
                    Vehical.objects.create(name=name, make=make, model=model,type=type,year=year,original_miles=orig_miles, active_miles=active_miles, original_value=orig_val,
                                        load_limit=load, ownership=owner, cost=orig_val, monthy_miles=miles, image_file=image_file, last_update=timestamp)
                
                #if pic_form.is_valid():
                    #pic_form.save()
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==None and update !=-1: 
            try:
                print('in update')
                #update existing event
                Vehical.objects.filter(id=veh_id).update(make=make, model=model, type=type,year=year,original_miles=orig_miles, active_miles=active_miles, original_value=orig_val, 
                                 load_limit=load, ownership=owner, cost=orig_val, monthy_miles=miles, image_file=image_file, last_update=timestamp)
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None and delete !=-1: 
            print('in update')
            try:
                Vehical.objects.filter(id=veh_id).delete()
            except IOError as e:
                print ("load vehicle Failure ", e)
                print('error = ',e) 
        return render(self.request,"assets/vehicle.html",{"vehicles": vehicles, "veh":veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle", 'month':month, 'year':year,'payment_month':payment_month, 
                                                        'payment_year':payment_year, 'insurance':insurance, 'fuel_month':fuel_month, 'fuel_year':fuel_year, 'maintenance':maintenance, 'repair':repair, 'tires':tires,
                                                        'inspection':inspection, 'operator':operator,'years':years,'duplicate':duplicate})

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
                space_id = self.request.GET.get('space_id', -1)
                print('space_id = ',space_id)
                buildings_list=Location.objects.order_by('name').values_list('name', flat=True).distinct()
                spaces = Business_Space.objects.all()
                space_type = self.request.GET.get('space_type', -1)
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
                    print('build_space.image_file',build_space.image_file)
                    uploaded_file_url=media_folder + '/images/' +str(build_space.image_file)
                
                if uploaded_file_url==None or uploaded_file_url =="":
                    uploaded_file_url = '/media/images/building_space.png'
                print('uploaded_file_url =',uploaded_file_url)
            except IOError as e:
                print ("load building Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/building.html",{'main_building':main_building, 'space_id':space_id, 'spaces':spaces, "buildings_list": buildings_list, "build_space": build_space, "uploaded_file_url":uploaded_file_url,  "index_type":"building", 
                                                            'space_percentage':space_percentage,'power_percentage':power_percentage, 'internet_percentage':internet_percentage, 'insurance_percentage':insurance_percentage, 'fuel_percentage':fuel_percentage,'duplicate':duplicate,
                                                            'space_type':space_type, 'building':building, 'sqr_feet':sqr_feet, 'payment_cost':payment_cost, 'power_cost':power_cost, 'internet_cost':internet_cost, 'fuel_cost':fuel_cost, 'maintenance_cost':maintenance_cost })
    
    def post(self, *args, **kwargs):
        timestamp = date.today()
        building = self.request.POST.get('_building',-1)
        print('building=',building)
        space_id = int(self.request.POST.get('_space_id', -1))
        print('space_id=',space_id)
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
        image_file = self.request.POST.get('_image',"-1")
       
        save = self.request.POST.get('_save',-1)
        print('save=',save)
        update = self.request.POST.get('_update',-1)
        print('update =',update )
        delete = self.request.POST.get('_delete',-1)
        print('delete=',delete)
        duplicate=-1
        print('space_id=',space_id)
        uploaded_file_url=-1
        image_file_content = self.request.FILES['uploaded_file'].read()
        print('image_file_content',image_file_content)
        image_file_name = self.request.FILES.get('uploaded_file')
        print('image_file_content',image_file_content)
        image_file=image_file_name
        if image_file==-1:
            uploaded_file_url=image_file
        print('image_file',image_file)
        if space_id != -1:
            spa = Business_Space.objects.filter(id=space_id).all()
            print('spa=',spa)
            spa=spa[0]
            print('spa=',spa)
            print('spa.image_file',spa.image_file)
            if image_file==-1:
                uploaded_file_url=spa.image_file
                image_file = spa.image_file
                
            print('image_file=',image_file)
        
            
        
        media_folder = settings.MEDIA_URL
        uploaded_file_url=media_folder + str(image_file)
        buildings_list=Location.objects.order_by('name').values_list('name', flat=True).distinct()
        spaces = Business_Space.objects.all()
        
        if save!=-1:	
            try:		
                if Business_Space.objects.filter(building=building,type=build_space).exists():
                    duplicate=1
                    return render(self.request,"assets/building.html",{'main_building':main_building, 'space_id':space_id, 'spaces':spaces, "buildings_list": buildings_list, "build_space": build_space, "uploaded_file_url":uploaded_file_url,  "index_type":"building", 
                                                            'space_percentage':space_percentage,'power_percentage':power_percentage, 'internet_percentage':internet_percentage, 'insurance_percentage':insurance_percentage, 'fuel_percentage':fuel_percentage,'duplicate':duplicate,
                                                            'space_type':space_type, 'building':building, 'sqr_feet':sqr_feet, 'payment_cost':payment_cost, 'power_cost':power_cost, 'internet_cost':internet_cost, 'fuel_cost':fuel_cost, 'maintenance_cost':maintenance_cost })
                else:
                    Business_Space.objects.create(building=building, type=space_type, space_percentage=space_percentage, power_percentage=power_percentage, internet_percentage=internet_percentage, 
                                                    sqr_feet=sqr_feet,payment_cost=payment_cost,power_cost=power_cost,internet_cost=internet_cost,fuel_cost=fuel_cost,maintenance_cost=maintenance_cost,
                                                    insurance_percentage=insurance_percentage, fuel_percentage=fuel_percentage, image_file=image_file, last_update=timestamp)
                    b=Business_Space.objects.get(building=building,type=build_space)
                    Location.objects.filter(name=building).update(Business_Space=b)
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
                                                    insurance_percentage=insurance_percentage, fuel_percentage=fuel_percentage, image_file=image_file, last_update=timestamp)
                b=Business_Space.objects.get(id=space_id)
                print('b=',b)
                Location.objects.filter(name=building).update(Business_Space=b)
                print('updated location')
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
        return render(self.request,"assets/building.html",{'main_building':main_building, 'space_id':space_id, 'spaces':spaces, "buildings_list": buildings_list, "build_space": build_space, "uploaded_file_url":uploaded_file_url,  "index_type":"building", 
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