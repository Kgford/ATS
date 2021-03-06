from django import forms
from ATS import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from datetime import date
from django.urls import reverse, reverse_lazy
from django.views import View
import datetime
from django.contrib.auth.decorators import login_required
from barcode_app.models import Barcodes
from barcode_app.barcode_lib import Barcode
from base64 import *
from io import BytesIO
from django.core.files import File
from .forms import BarcodeForm

# Create your views here.

class BarcodeView(View):
    template_name = "index.html"
    success_url = reverse_lazy('barcode_app:barcode')
    def get(self, *args, **kwargs):
        try:
            print('in Get')
            part_num = self.request.POST.get('_part_num', -1)
            standard = self.request.POST.get('_standard', -1)
            bc = -1
            encoded = -1
            message=-1
            description=-1
            staticfile = 'sample'
            if part_num !=-1 and standard !=-1:
                bc = Barcodes.objects.filter(part_number=part_num,standard=standard).all()
                bc=bc[0]
                #
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)
        return render(self.request,'index.html',{'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})
    
    def post(self, request, *args, **kwargs):
        try: 
            print("in POST")
            bc = -1
            success = True
            staticfile = 'sample'
            media_save_folder = settings.MEDIA_ROOT + '\\barcodes\\'
            media_folder =settings.MEDIA_URL
            message = -1
            timestamp = date.today()
            
            part_num = self.request.POST.get('_part_num',-1)
            print('part_num=',part_num)
            description = self.request.POST.get('_desc',-1)
            print('description=',description)
            if description ==-1:
                desc = 'N/A'
            else: 
                desc = description
            standard = self.request.POST.get('_standard',-1)
            if standard == 'Code 39':
                standard = 'code39'
            print('standard=',standard)
            #uploaded_file_url=media_folder + 'barcodes/' + part_num + '.jpg'     
            
            print('bc',bc)
            word = 'EAN'
            if word in standard.upper():
                print(len(part_num))
                if not part_num.isnumeric():
                    message = standard + ' must only contain numbers'
                    bc=-1
                    staticfile = 'barcode1'
                    return render(self.request,'index.html',{'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})
                if len(part_num) < 12: 
                    message = standard + ' needsatleast12digits'
                    bc=-1
                    staticfile = 'barcode2'
                    return render(self.request,'index.html',{'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})
            word = 'GTIN'
            if word in standard.upper():
                print(len(part_num))
                if not part_num.isnumeric():
                    message = standard + ' must only contain numbers'
                    bc=-1
                    staticfile = 'barcode1'
                    return render(self.request,'index.html',{'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})
                
            word = 'UPC'
            if word in standard.upper():
                print(len(part_num))
                if not part_num.isnumeric():
                    message = standard + ' must only contain numbers'
                    bc=-1
                    staticfile = 'barcode1'
                    return render(self.request,'index.html',{'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})
            
            word = 'ISBN'
            startwith = part_num[0:3]
            print('startwith=',startwith)
            if word in standard.upper():
                if not startwith =='978' and not  startwith =='979' in part_num:
                    message = standard + ' must start with 978 or 979'
                    bc=-1
                    staticfile = 'barcode3'
                    return render(self.request,'index.html',{'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})
            
            if Barcodes.objects.filter(part_number=part_num, standard=standard).count()>0:
                bc = Barcodes.objects.filter(part_number=part_num, standard=standard)
                bc=bc[0]              
                print('bc=',bc)
                print('bc.image=',bc.image)
            
            save = self.request.POST.get('_save',-1)
            print('save',save)
            if save !=-1:
                print('in save')
                bc = Barcodes.objects.create(part_number=part_num, standard=standard)
                print('bc',bc)
                bc.save()
                print('bc',bc)
                print('image=',bc.image)
                print('part_number=',bc.part_number)
                
            update = self.request.POST.get('_update',-1)
            print('update',update)   
            if update !=-1:
                print('in update')
                bc = Barcodes.objects.filter(part_number=part_num, standard=standard)
                print('bc',bc)
                bc.update()
                bc = Barcodes.objects.latest('id')
            
            delete = self.request.POST.get('_delete',-1)
            print('delete',delete)   
            if delete !=-1:
                print('in update')
                Barcodes.objects.filter(part_number=part_num, standard=standard).delete() 
                bc=-1                
             
            image=-1
            if bc!=-1:
                print('bc=',bc.image)
                image = bc.image
                image = str(image)
                x=image.split('/')
                image = x[2]
                print('image',image)
            
                        
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'index.html',{'image':image,'staticfile':staticfile, 'message':message, "bc": bc, 'part_num':part_num, 'standard':standard})