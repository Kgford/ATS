from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .forms import ModelsForm
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.urls import reverse
from django.views import View
from equipment.models import Model
from vendor.models import Vendor
from datetime import date, datetime
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
model_id = 0


class UserLogin(View):
    template_name = "user_login.html"
    success_url = reverse_lazy('equipment:login')
        
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user.get_short_name())
        
        except IOError as e:
           print('error = ',e) 
        return render(request, 'equipments/user_login.html', {})
 
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
                    return render(request,'equipment/index.html')
                else:
                    return render(request, 'equipment/user_login.html', {'message':'Login Failed!!'})
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
            return render(request, 'equipment/user_login.html', {'message':'Login Failed!!'})
        else:
            return render(request, 'equipment/user_login.html', {})

class EquipmentView(View):
    form_class = ModelsForm
    template_name = "index.html"
    success_url = reverse_lazy('equipment:equipment')
    contSuccess = 0
    
    def get(self, *args, **kwargs):
        form = self.form_class()
        
        try:
            models = Model.objects.all()
            vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/index.html",{"form": form, "models": models, 'vendor_list':vendor_list, "index_type":"EQUIPMENT"})
	   	
    def post(self, request, *args, **kwargs):
        form = self.form_class()
        search = request.POST.get('search', -1)
        vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
        print('search =',search)
        success = True
        if not search ==-1:
            models = Model.objects.filter(description__icontains=search) | Model.objects.filter(category__icontains=search) | Model.objects.filter(band__icontains=search) | Model.objects.filter(vendor__icontains=search) | Model.objects.filter(model__icontains=search) | Model.objects.filter(status__contains=search).all()
            if not models:
                models = Model.objects.all()
        else:
            models = Model.objects.all()

        return render (self.request,"equipment/index.html",{"form": form, "models": models, 'vendor_list':vendor_list, "index_type":"EQUIPMENT"})

class ModelView(View):
    form_class = ModelsForm
    template_name = "model.html"
    success_url = reverse_lazy('equipment:newmodel')
   
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            model_id = self.request.GET.get('model_id', -1)
            print('model_id=',model_id)
            mod=-1
            form=-1
            uploaded_file_url=-1
            if model_id !=-1:
                mod = Model.objects.filter(id=model_id).all()
                mod = mod[0]
                uploaded_file_url=mod.image
                print('uploaded_file_url=',uploaded_file_url)
               
            models = Model.objects.all()
            vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
            
            print(models)
            print(mod)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/model.html",{"form": form, "models": models, "mod": mod, 'vendor_list':vendor_list, 'uploaded_file_url':uploaded_file_url,  "index_type":"EQUIPMENT"})
        
    def post(self, *args, **kwargs):
        timestamp = date.today()
        band = self.request.POST.get('_band',-1)
        category = self.request.POST.get('_category',-1)
        description = self.request.POST.get('_desc',-1)
        model = self.request.POST.get('_model',-1)
        vendor= self.request.POST.get('_vendor',-1)
        active = True
        image = self.request.POST.get('fileupload',-1)
        print('image=',image)
        comments = self.request.POST.get('_comments',-1)
        model_id = self.request.POST.get('m_id',-1)
        save = self.request.POST.get('_save',-1)
        print('save=',save)
        update = self.request.POST.get('_update',-1)
        print('update=',update)
        delete = self.request.POST.get('_delete',-1)
        print('delete=',delete)
        models = Model.objects.all()
        vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
        mod=-1
        form=-1
        
        if not save==-1:	
            try:		
                Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, status=active, last_update=timestamp)
                        
                m=Model.objects.filter(description=description,band=band, vendor=vendor, model=model)
                form = ModelsForm(self.request.POST, self.request.FILES, instance = m[0], use_required_attribute=False)
                print('form',form)       
                if form.is_valid():
                    print('form is valid')
                    form.save()
                mod = Model.objects.filter(description=description,band=band, vendor=vendor, model=model).all()
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==-1: 
            try:
                #update existing event
                Model.objects.filter(id=model_id).update(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, status=active, last_update=timestamp)
                m=Model.objects.filter(description=description, band=band, vendor=vendor, model=model)
                form = ModelsForm(self.request.POST, self.request.FILES, instance = m[0], use_required_attribute=False)
                print('form',form)       
                if form.is_valid():
                    print('form is valid')
                    form.save()
                mod = Model.objects.filter(description=description,band=band, vendor=vendor, model=model).all()
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==-1: 
            try:
                Model.objects.filter(id=model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render (self.request,"equipment/model.html",{"form": form, "models": models, 'vendor_list':vendor_list,  "mod": mod, "index_type":"EQUIPMENT"})

       


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
        file_path = media_folder+image_file
        image_file = media_folder + imagefile
        
        os.rename(file_path,image_file)
       
        if form.is_valid(): 
            form.save() 
    else: 
        form = ModelsForm()
        imagefile = request.POST.get('photo',-1)
        #print('imagefile =',imagefile)
    return render(request, 'equipment/images.html', {'form' : form}) 
   

@login_required
def savemodel(request):
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
            uploaded_file_url='/ATS/media/inv1.jpg' 
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
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "image_file":image_file, 'uploaded_file_url':uploaded_file_url,  "index_type":"Model"})