from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from .forms import VendorForm
from datetime import date
from django.urls import reverse,  reverse_lazy
from vendor.models import Vendor
from django.views import View
from django.contrib.auth import authenticate
site_id = 0

class UserLogin(View):
    template_name = "user_login.html"
    success_url = reverse_lazy('vendor:login')
        
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user.get_short_name())
        
        except IOError as e:
           print('error = ',e) 
        return render(request, 'vendor/user_login.html', {})
 
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
                    return render(request,'vendor/index.html')
                else:
                    return render(request, 'vendor/user_login.html', {'message':'Login Failed!!'})
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
            return render(request, 'vendor/user_login.html', {'message':'Login Failed!!'})
        else:
            return render(request, 'vendor/user_login.html', {})

class VendorView(View):
    form_class = VendorForm
    template_name = "index.html"
    success_url = reverse_lazy('vendor:vendor')
        
    def get(self, *args, **kwargs):
        form = self.form_class()
        operator = str(self.request.user.get_short_name())
        active = "off"
        try:
            vendor = Vendor.objects.all()
            print('vendor =',vendor)
                       
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"vendor/index.html",{"form": form, "vendor":vendor, "index_type":"SIGNIN", "UserN":self.request.user, "index_type":"vendor", "operator":operator, "active":active})
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            operator = str(self.request.user.get_short_name())
            timestamp = date.today()
            name = request.POST.get('_name', -1)
            address = request.POST.get('_addr', -1)
            if address ==-1:
                address='N/A'
            print('address=',address)
            city = request.POST.get('_city', -1)
            if city ==-1:
                city='N/A'
            print('city=',city)
            state = request.POST.get('_state', -1)
            if state ==-1:
                state='N/A'
            print('state=',state)
            zip_code = request.POST.get('_zip', -1)
            if zip_code ==-1:
                zip_code='N/A'
            print('zip_code=',zip_code)
            phone = request.POST.get('_phone', -1)
            if phone ==-1:
                phone='N/A'
            lat = request.POST.get('_lat', -1)
            if lat ==-1:
                lat=None
            print('lat=',lat)
            lng = request.POST.get('_lng', -1)
            if lng ==-1:
                lng=None
            print('lng=',lng)
            email = request.POST.get('_email', -1)
            if email ==-1:
                email='N/A'
            print('email=',email)
            website = request.POST.get('_web', -1)
            if website ==-1:
                website='N/A'
            print('website=',website)
            active = request.POST.get('_active', -1)
            if active ==-1:
                active=False
           
            print('active=',active)
            if active =='on':
                active_save = True
            else:
                active_save = False
            
            first_name = request.POST.get('_first', -1)
            if first_name ==-1:
                first_name='N/A'
            print('first_name=',first_name)
            last_name = request.POST.get('_last', -1)
            if last_name ==-1:
                last_namee='N/A'
            print('last_name=',last_name)
            print('active_save',active_save)            
            inventory_id = None
            vendor = Vendor.objects.all()
            sites = Vendor.objects.all()
            site = Vendor.objects.filter(name=name).all()
            print('site=',site)
           
            try: 
                if Vendor.objects.filter(name=name).exists():
                    site = Vendor.objects.filter(name=name).all()
                    print('site=',site)
                    return redirect('vendor:site',site[0].id)
                else:
                    if lat=='':
                        print('lat=',lat)
                        Vendor.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                                active=active_save, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, contact_first=first_name, contact_last=last_name)
                    else:
                        Vendor.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                                active=active_save, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, lat=lat, lng=lng, contact_first=first_name, contact_last=last_name)
            except IOError as e:
                print ("vendor Save Failure ", e)	
        return render (self.request,"vendor/index.html",{"vendor":vendor, "index_type":"SIGNIN", "UserN":self.request.user, "index_type":"vendor" , "operator":operator, "active":active})

def save_vendor_csv(delete):               
    #~~~~~~~~~~~Load vendor database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'vendor.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    Vendor.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for name, address, city, state,zip_code, phone, email, website, lat, lng, created_on ,last_entry in reader:
        if lat=="": lat=40.815320
        if lng=="": lng=-73.237710
        Vendor.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email,
                 website=website,active=True, lat=float(lat), lng=float(lng), created_on=timestamp, last_entry=timestamp)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
             
    	
def site(request,vendor_id):
    sites = []
    site = []
    lat = 0
    lng = 0
    print('we are here')
    if request.method == 'GET':
        operator = str(request.user)
        # cast the request inventory_id from string to integer type.
        vendor_id = int(vendor_id)
        print('location_id=',vendor_id)
        success = True 
        try:	
            sites = Vendor.objects.all()
            for site1 in sites:
                if site1.id ==vendor_id:
                    site = site1
                    break
            print('site.lat=',site.lat)       
            if not site.lat ==None:
                lat = float(site.lat)
                print(lat)
                lng = float(site.lng)
                print(lng)
            if site.active == True:
                active = 'on'
            else:
                active = 'off'
            print('active=',active)
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"vendor/site.html",{"sites": sites, "site": site, "lat":lat, "lng":lng, "index_type":"Model", "active":active, "operator":operator})
                
    if request.method == 'POST':
        print('in post')
       # cast the request inventory_id from string to integer type.
        vendor_id = int(vendor_id)
        print('vendor_id=',vendor_id)
        success = True 
        try:
            sites = Vendor.objects.all()
            for site1 in sites:
                if site1.id ==vendor_id:
                    site = site1
                    break
            operator = str(request.user)
            timestamp = date.today()
            name = request.POST.get('_name', -1)
            address = request.POST.get('_addr', -1)
            city = request.POST.get('_city', -1)
            state = request.POST.get('_state', -1)
            zip_code = request.POST.get('_zip', -1)
            phone = request.POST.get('_phone', -1)
            print('phone=',phone)
            lat = request.POST.get('_lat', -1)
            lng = request.POST.get('_lng', -1)
            email = request.POST.get('_email', -1)
            print('email=',email)
            website = request.POST.get('_web', -1)
            print('website=',website)
            active = request.POST.get('_active', -1)
            if active == 'on':
                active_save = True
            else:
                active_save = False
            print('active=',active_save)
            Vendor.objects.filter(id=vendor_id).update(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email,
                        website=website,active=active_save, lat=float(lat), lng=float(lng), created_on=timestamp, last_entry=timestamp)
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"vendor/site.html",{"sites": sites, "site": site, "lat":lat, "lng":lng, "index_type":"Model", "active":active, "operator":operator})
	
def searchsite(request):
    json_data = []
    row_header = []
    
    success = True  
    try:
        site_list = Vendor.objects.all()
    except IOError as e:
        success = False
        print ("Sitelist load Failure ", e)    
	 
    if site_list == None:
        success = False
    else:
        site=[e.serialize() for e in site_list]
    return jsonify({"success": success, "site_list": site})
