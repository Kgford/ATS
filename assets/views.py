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
from assets.models import Personnel,Vehical,Building, Business_Space, Product
from vendor.models import Vendor
from contractors.models import Contractors
from .models import Vehical
from django.views import View
import datetime
from collections import OrderedDict
from ATS.overhead import Equations
from re import search
from ATS.overhead import Comunication
from django.contrib.auth.decorators import login_required

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
            vehicle=-1
            operator = str(self.request.user)
            phone = self.request.user.userprofileinfo.phone
            message = 'message'
            com=Comunication(phone,message)
            print('com=',com)
            com.send_sms()
            veh_id = self.request.GET.get('vehicle', -1)
            build_id = self.request.GET.get('building', -1)
            person_id = self.request.GET.get('personnel', -1)
            product_id = self.request.GET.get('product', -1)
            vehicle = Vehical.objects.all()
            personnel = Personnel.objects.all()
            space = Business_Space.objects.all()
            product = Product.objects.all()
            if veh_id!=-1:
                veh = Model.objects.filter(id=veh_id).all()
                veh=veh[0]
                print(veh)
                
            print(vehicle)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"assets/index.html",{ "vehicle": vehicle, "veh":veh,  "index_type":"assests"})
        
    def post(self, *args, **kwargs):
        timestamp = date.today()
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
                years = []
                year = datetime.date.today().year
                for i in range(-40,0):
                    years.append(year+i)
                veh_id = self.request.GET.get('vehicle', -1)
                vehicles=Vehical.objects.all()
                if veh_id!=-1:
                    veh = Model.objects.filter(id=veh_id).all()
                    veh=veh[0]
                    print('veh.image_file',veh.image_file)
                    uploaded_file_url=veh.photo
                
                if uploaded_file_url==None or uploaded_file_url =="":
                    uploaded_file_url = '/ATS/media/inv1.png'
                print('uploaded_file_url =',uploaded_file_url)
            except IOError as e:
                print ("load vehicle Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/vehicle.html",{'year':year, 'years':years, "vehicles": vehicles, "veh": veh, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle"})
    def post(self, *args, **kwargs):
        timestamp = date.today()
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
                print ("load vehicle Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/vehicle.html",{"vehicles": vehicles, "mod": mod, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle"})

class BuildingView(View):
    template_name = "building.html"
    success_url = reverse_lazy('assets:building')
    def get(self, *args, **kwargs):
            buildings_list = []
            veh = []
            uploaded_file_url=None
            print('we are here')
            # cast the request inventory_id from string to integer type.
            success = True 
            try:	
                build_space = -1
                space_id = self.request.GET.get('building', -1)
                buildings_list=Location.objects.order_by('name').values_list('name', flat=True).distinct()
               
                
                if space_id!=-1:
                    build_space = Building.objects.filter(id=space_id).all()
                    build_space=build_space[0]
                    print('build_space.image_file',build_space.image_file)
                    uploaded_file_url=veh.photo
                
                if uploaded_file_url==None or uploaded_file_url =="":
                    uploaded_file_url = '/ATS/media/inv1.png'
                print('uploaded_file_url =',uploaded_file_url)
            except IOError as e:
                print ("load building Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/building.html",{'build_space':build_space,  "buildings_list": buildings_list,  "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle"})
    
    def post(self, *args, **kwargs):
        timestamp = date.today()
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
                print ("load vehicle Failure ", e)
                print('error = ',e) 
            return render(self.request,"assets/building.html",{"buildings": buildings, "mod": mod, "uploaded_file_url":uploaded_file_url,  "index_type":"vehicle"})

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
                uploaded_file_url = '/tcli/media/inv1.jpg'
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