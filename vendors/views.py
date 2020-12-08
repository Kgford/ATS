from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from .forms import VendorForm
from datetime import date
from django.urls import reverse,  reverse_lazy
from vendors.models import Vendors
from django.views import View
site_id = 0

class VendorView(View):
    form_class = VendorForm
    template_name = "index.html"
    success_url = reverse_lazy('vendors:vendor')
    
    def get(self, *args, **kwargs):
        form = self.form_class()
        operator = str(self.request.user)
        try:
            vendors = Vendors.objects.all()
            print('vendors =',vendors)
                       
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"vendors/index.html",{"form": form, "vendors":vendors, "index_type":"SIGNIN", "UserN":self.request.user, "index_type":"Vendor", "operator":operator})
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            operator = str(self.request.user)
            timestamp = date.today()
            name = request.POST.get('_name', -1)
            address = request.POST.get('_addr', -1)
            city = request.POST.get('_city', -1)
            state = request.POST.get('_state', -1)
            zip_code = request.POST.get('_zip', -1)
            phone = request.POST.get('_phone', -1)
            lat = request.POST.get('_lat', -1)
            lng = request.POST.get('_lng', -1)
            email = request.POST.get('_email', -1)
            website = request.POST.get('_web', -1)
            inventory_id = None
            active=True
            vendors = Vendors.objects.all()
           
            try: 
               
               Vendors.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                        active=active, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, lat=lat, lng=lng)
            except IOError as e:
                print ("vendor Save Failure ", e)	
        return render (self.request,"vendors/index.html",{"vendors":vendors, "index_type":"SIGNIN", "UserN":self.request.user, "index_type":"Vendor" , "operator":operator})

def save_csv(delete):               
    #~~~~~~~~~~~Load vendor database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'vendors.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    Vendors.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for name, address, city, state,zip_code, phone, email, website, lat, lng, created_on ,last_entry in reader:
        if lat=="": lat=40.815320
        if lng=="": lng=-73.237710
        Vendors.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email,
                 website=website,active=True, lat=float(lat), lng=float(lng), created_on=timestamp, last_entry=timestamp)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
             
    	
def site(request,vendor_id):
    sites = []
    site = []
    print('we are here')
    # cast the request inventory_id from string to integer type.
    vendor_id = int(vendor_id)
    print('location_id=',vendor_id)
    success = True 
    try:	
        sites = Vendors.objects.all()
        for site1 in sites:
            if site1.id ==vendor_id:
                site = site1
                break
        lat = float(site.lat)
        print(lat)
        lng = float(site.lng)
        print(lng)
    except IOError as e:
        print ("load model Failure ", e)
        print('error = ',e) 
    return render(request,"vendors/site.html",{"sites": sites, "site": site, "lat":lat, "lng":lng, "index_type":"Model"})
	
def searchsite(request):
    json_data = []
    row_header = []
    
    success = True  
    try:
        site_list = Vendors.objects.all()
    except IOError as e:
        success = False
        print ("Sitelist load Failure ", e)    
	 
    if site_list == None:
        success = False
    else:
        site=[e.serialize() for e in site_list]
    return jsonify({"success": success, "site_list": site})
