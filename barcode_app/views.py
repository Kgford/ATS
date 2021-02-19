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

# Create your views here.

class BarcodeView(View):
    template_name = "index.html"
    success_url = reverse_lazy('barcode_app:barcode')
    def get(self, *args, **kwargs):
        try:
            print('in Get')
            part_num = self.request.POST.get('_year', -1)
            barcode = []
            encoded = -1
            part_num=-1
            standard=-1
            message=-1
            description=-1
            media_save_folder = settings.MEDIA_ROOT + '\\barcodes\\'
            media_folder =settings.MEDIA_URL
            uploaded_file_url=media_folder + 'barcodes/sample.jpg'
            print('uploaded_file_url',uploaded_file_url) 
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)
        return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num, "barcode": barcode,"uploaded_file_url":uploaded_file_url})
    
    def post(self, request, *args, **kwargs):
        try: 
            print("in POST")
            barcode = []
            success = True
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
            
            uploaded_file_url=media_folder + 'barcodes/' + part_num + '.jpg'     
            
            word = 'EAN'
            if word in standard.upper():
                print(len(part_num))
                if not part_num.isnumeric():
                    message = standard + ' must only contain numbers'
                    uploaded_file_url=media_folder + 'barcodes/mustonlycontainnumbers.jpg'
                    return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num,"barcode": barcode,"uploaded_file_url":uploaded_file_url})
                if len(part_num) < 12: 
                    message = standard + ' needsatleast12digits'
                    uploaded_file_url=media_folder + 'barcodes/needsatleast12digits.jpg'
                    return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num,"barcode": barcode,"uploaded_file_url":uploaded_file_url})
            word = 'GTIN'
            if word in standard.upper():
                print(len(part_num))
                if not part_num.isnumeric():
                    message = standard + ' must only contain numbers'
                    uploaded_file_url=media_folder + 'barcodes/mustonlycontainnumbers.jpg'
                    return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num,"barcode": barcode,"uploaded_file_url":uploaded_file_url})
                
            word = 'UPC'
            if word in standard.upper():
                print(len(part_num))
                if not part_num.isnumeric():
                    message = standard + ' must only contain numbers'
                    uploaded_file_url=media_folder + 'barcodes/mustonlycontainnumbers.jpg'
                    return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num,"barcode": barcode,"uploaded_file_url":uploaded_file_url})
            word = 'ISBN'
            startwith = part_num[0:3]
            print('startwith=',startwith)
            if word in standard.upper():
                if not startwith =='978' and not  startwith =='979' in part_num:
                    message = standard + ' must start with 978 or 979'
                    uploaded_file_url=media_folder + 'barcodes/muststartwith978or979.jpg'
                    return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num,"barcode": barcode,"uploaded_file_url":uploaded_file_url})
            '''
            b = Barcode(part_num,media_save_folder,standard,'test')
            image = b.create_barcode_jpg()
            print('image',image)
            print('uploaded_file_url',uploaded_file_url)
            
            rv = b.create_barcode_byte()
            print('byte=',File(rv))
            '''
            save = self.request.POST.get('_save',-1)
            print('save',save)
            if save !=-1:
                print('in save')
                bc = Barcodes.objects.create(part_number=part_num, standard=standard)
                bc = Barcodes.objects.latest('id')
                print('bc',bc)
                bc.save()
                barcode = Barcodes.objects.latest('id')
                
                
            
            update = self.request.POST.get('_update',-1)
            print('update',update)   
            if update !=-1:
                print('in update')
                uploaded_file_url=media_folder + 'barcodes/' + part_num +'.jpg'
                print('uploaded_file_url',uploaded_file_url)         
            
            delete = self.request.POST.get('_delete',-1)
            print('delete',delete)   
            if update !=-1:
                print('in update')
                uploaded_file_url=media_folder + 'barcodes/' + part_num +'.jpg'
                print('uploaded_file_url',uploaded_file_url)   
             
                        
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'index.html',{'description':description, 'message':message, 'standard':standard, 'part_num':part_num,"barcode": barcode,"uploaded_file_url":uploaded_file_url})