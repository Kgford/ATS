from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from datetime import date
from django.urls import reverse, reverse_lazy
from django.views import View
import datetime
from django.contrib.auth.decorators import login_required
from atspublic.models import Blog, Category, Visitor
from ATS.overhead import Comunication,Email
from django.contrib.auth.models import User
from users.models import UserProfileInfo
from django.db.models import Q
#from django.shortcuts import render_to_response, get_object_or_404
 
   
# Create your views here.
def index(request):
	return render(request,'atspublic/index.html')

class SignupView(View):
    template_name = "signup.html"
    success_url = reverse_lazy('atspublic:signup')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~
            error_message = 'this is a test'
            cookie_array =[]
            inner_array =[]
            email=-1
            cookie = str(self.request.headers.get('Cookie'))
            cookie_array= cookie.split( ';',-1)
            print('Cookie=',cookie)
            inner_array=cookie_array[0].split( '=',-1) 
            client_id=inner_array[1]
            print('client_id=',client_id)
            visitor_ip = str(self.request.headers.get('visitor_ip'))
            print('visitor_ip=',visitor_ip)
            user_agent = str(self.request.headers.get('User-Agent'))
            print('user_agent=',user_agent)
            visitor = str(self.request.user)
            session_id ='N/A'
            if visitor!='AnonymousUser':
                inner_array=cookie_array[2].split( '=',-1) 
                session_id=inner_array[1]
                print('session_id=',session_id)
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True)).all()
            print('profiles=',profiles)
            email_list=[]
            phone_list=[]
            print('profiles[0]=',profiles[0].address)
            for staff in profiles:
                if staff.alerts_web_monitor:
                    email_list.append(staff.email)
                    phone_list.append(staff.phone)
            print('email_list=',email_list)
            print('phone_list=',phone_list)
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            print(self.request.user)        
            message = 'ATS ' + visitor +' is Signing up for updates and news letters.\n' + 'Client_Id:  ' + client_id 
            print(message)
            com=Comunication(phone_list,message)
            print('com=',com)
            com.send_sms()
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'signup.html',{"error_message": error_message,'email':email})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            timestamp = date.today()
            print("in POST")
            username = self.request.POST.get('_user_name', -1)
            print('username=',username)
            email = self.request.POST.get('_email', -1)
            email_list = [email]
            print('email=',email_list)
            error_message = -1
                                   
           #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~
            cookie_array =[]
            inner_array =[]
            cookie = str(self.request.headers.get('Cookie'))
            cookie_array= cookie.split( ';',-1)
            print('Cookie=',cookie)
            inner_array=cookie_array[0].split( '=',-1) 
            client_id=inner_array[1]
            print('client_id=',client_id)
            visitor_ip = str(self.request.headers.get('visitor_ip'))
            print('visitor_ip=',visitor_ip)
            user_agent = str(self.request.headers.get('User-Agent'))
            print('user_agent=',user_agent)
            visitor = str(self.request.user)
            session_id ='N/A'
            if visitor!='AnonymousUser':
                inner_array=cookie_array[2].split( '=',-1) 
                session_id=inner_array[1]
                print('session_id=',session_id)
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True)).all()
            print('profiles=',profiles)
            phone_list=[]
            print('profiles[0]=',profiles[0].address)
            for staff in profiles:
                if staff.alerts_web_monitor:
                    phone_list.append(staff.phone)
            print('phone_list=',phone_list)
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if Visitor.objects.filter(visitor=username).exists():
                error_message = 'Username: ' + username + ' already exists please choose another'
                return render(self.request,'signup.html',{"error_message": error_message,'email':email})
            else:
                Visitor.objects.create(visitor=visitor,email=email,session_id=session_id,client_id=client_id,
                                    user_agent=user_agent,visitor_ip=visitor_ip,created_on=timestamp,last_entry=timestamp)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
           
           #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            subject = 'Welcome to Automated Test Solutions'
            email_body = 'Hello ' + username + ' Nice to meet you!\n\nYou are now on the ATS list to recieve our News Letter, price updates, and any new technology advances.\n\nThanks,\nATS Staff\nhttps://automatedtestsolutions.herokuapp.com/.'
            print(email_body)
            email=Email(email_list,subject, email_body)
            print('email=',email)
            email.send_email()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'signup.html',{"error_message": error_message})
        
class SigninView(View):
    template_name = "signin.html"
    success_url = reverse_lazy('atspublic:signin')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~
            error_message = 'this is a test'
            cookie_array =[]
            inner_array =[]
            email=-1
            cookie = str(self.request.headers.get('Cookie'))
            cookie_array= cookie.split( ';',-1)
            print('Cookie=',cookie)
            inner_array=cookie_array[0].split( '=',-1) 
            client_id=inner_array[1]
            print('client_id=',client_id)
            visitor_ip = str(self.request.headers.get('visitor_ip'))
            print('visitor_ip=',visitor_ip)
            user_agent = str(self.request.headers.get('User-Agent'))
            print('user_agent=',user_agent)
            visitor = str(self.request.user)
            session_id ='N/A'
            if visitor!='AnonymousUser':
                inner_array=cookie_array[2].split( '=',-1) 
                session_id=inner_array[1]
                print('session_id=',session_id)
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True)).all()
            print('profiles=',profiles)
            email_list=[]
            phone_list=[]
            print('profiles[0]=',profiles[0].address)
            for staff in profiles:
                if staff.alerts_web_monitor:
                    email_list.append(staff.email)
                    phone_list.append(staff.phone)
            print('email_list=',email_list)
            print('phone_list=',phone_list)
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            print(self.request.user)        
            message = 'ATS ' + visitor +' is Signing up for updates and news letters.\n' + 'Client_Id:  ' + client_id 
            print(message)
            com=Comunication(phone_list,message)
            print('com=',com)
            com.send_sms()
            success = True
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'signin.html',{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'signin.html',{"inventory": inv})

class TestimonialView(View):
    template_name = "testimonial.html"
    success_url = reverse_lazy('atspublic:testimonial')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'testimonial.html',{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'testimonial.html',{"inventory": inv})
        
class ContactView(View):
    template_name = "contact_us.html"
    success_url = reverse_lazy('atspublic:contacts')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~
            error_message = 'this is a test'
            cookie_array =[]
            inner_array =[]
            email=-1
            cookie = str(self.request.headers.get('Cookie'))
            cookie_array= cookie.split( ';',-1)
            print('Cookie=',cookie)
            inner_array=cookie_array[0].split( '=',-1) 
            client_id=inner_array[1]
            print('client_id=',client_id)
            visitor_ip = str(self.request.headers.get('visitor_ip'))
            print('visitor_ip=',visitor_ip)
            user_agent = str(self.request.headers.get('User-Agent'))
            print('user_agent=',user_agent)
            visitor = str(self.request.user)
            session_id ='N/A'
            if visitor!='AnonymousUser':
                inner_array=cookie_array[2].split( '=',-1) 
                session_id=inner_array[1]
                print('session_id=',session_id)
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_help_desk=True) | Q(alerts_security=True) | Q(alerts_sales=True) | Q(alerts_marketing=True)).all()
            print('profiles=',profiles)
            email_list=[]
            phone_list=[]
            print('profiles[0]=',profiles[0].address)
            for staff in profiles:
                if staff.alerts_web_monitor:
                    email_list.append(staff.email)
                    phone_list.append(staff.phone)
            print('email_list=',email_list)
            print('phone_list=',phone_list)
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            print(self.request.user)        
            message = 'ATS ' + visitor +' is Signing up for updates and news letters.\n' + 'Client_Id:  ' + client_id 
            print(message)
            com=Comunication(phone_list,message)
            print('com=',com)
            com.send_sms()
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'contact_us.html',{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            timestamp = date.today()
            print("in POST")
            username = self.request.POST.get('_user_name', -1)
            print('username=',username)
            email = self.request.POST.get('_email', -1)
            user_email = [email]
            message = self.request.POST.get('_message', -1)
            print('email=',user_email)
            print('message=',message)
            error_message = -1
                                   
           #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~
            cookie_array =[]
            inner_array =[]
            cookie = str(self.request.headers.get('Cookie'))
            cookie_array= cookie.split( ';',-1)
            print('Cookie=',cookie)
            inner_array=cookie_array[0].split( '=',-1) 
            client_id=inner_array[1]
            print('client_id=',client_id)
            visitor_ip = str(self.request.headers.get('visitor_ip'))
            print('visitor_ip=',visitor_ip)
            user_agent = str(self.request.headers.get('User-Agent'))
            print('user_agent=',user_agent)
            visitor = str(self.request.user)
            session_id ='N/A'
            if visitor!='AnonymousUser':
                inner_array=cookie_array[2].split( '=',-1) 
                session_id=inner_array[1]
                print('session_id=',session_id)
            
                
            #~~~~~~~~~~~~~~~~~~~~Get visitor information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_help_desk=True) | Q(alerts_security=True) | Q(alerts_sales=True) | Q(alerts_marketing=True)).all()
            print('profiles=',profiles)
            phone_list=[]
            email_list=[]
            print('profiles[0]=',profiles[0].address)
            for staff in profiles:
                if staff.alerts_web_monitor:
                    email_list.append(staff.email)
                    phone_list.append(staff.phone)
            print('email_list=',email_list)
            print('phone_list=',phone_list)
            #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list ~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if not Visitor.objects.filter(Q(visitor=username) | Q(session_id=session_id)).exists():
                Visitor.objects.create(visitor=visitor,email=email,session_id=session_id,client_id=client_id,
                                    user_agent=user_agent,visitor_ip=visitor_ip,created_on=timestamp,last_entry=timestamp)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
           
           #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to user ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            subject = 'Automated Test Solutions'
            email_body = 'Hello ' + username + ' We have recieved your request and we will contact you soon.\n\nThanks,\nATS Staff\nhttps://automatedtestsolutions.herokuapp.com/.'
            print(email_body)
            email=Email(user_email,subject, email_body)
            email.send_email()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to staff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            subject = 'Customer Contact Request'
            email_body = message
            email=Email(email_list,subject, email_body)
            print('email=',email)
            email.send_email()
            mes= 'Customer Contact Request. Check your email' 
            com=Comunication(phone_list,mes)
            print('com=',com)
            com.send_sms()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to staff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'contact_us.html',{"inventory": inv})

class NewsView(View):
    template_name = "newsletter.html"
    success_url = reverse_lazy('atspublic:news')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'newsletter.html',{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'newsletter.html',{"inventory": inv})
        
class BlogView(View):
    template_name = "blog.html"
    success_url = reverse_lazy('atspublic:blog')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
       

class CategoryView(View):
    template_name = "blog.html"
    success_url = reverse_lazy('atspublic:view_category_post')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            #slug = request.POST.get('slug', -1)
            #category = get_object_or_404(Category, slug=slug)
            category = -1
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
 

# Create your views here.
class PostView(View):
    template_name = "view_post.html"
    success_url = reverse_lazy('atspublic:view_blog_post')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            category = -1
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        #return render(self.request,'view_post.html', {'post': get_object_or_404(Blog, slug=slug)}) 
        return render(self.request,'view_post.html') 
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        #return render(self.request,'view_post.html', {'post': get_object_or_404(Blog, slug=slug)})
        return render(self.request,'view_post.html') 

# Create your views here.
class PublicView(View):
    template_name = "index.html"
    success_url = reverse_lazy('atspublic:public')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"index.html",{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"index.html",{"inventory": inv})

		   
class WorkstationView(View):
    template_name = "racks.html"
    success_url = reverse_lazy('atspublic:racks')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"racks.html",{"inventory": inv})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"racks.html",{"inventory": inv})
        
class RobotView(View):
    template_name = "robotLab.html"
    success_url = reverse_lazy('atspublic:robot')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            video = self.request.GET.get('video', -1)
            print('video=',video)
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"robotLab.html",{"inventory": inv, 'video':video})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"robotLab.html",{"inventory": inv})
        
class FieldView(View):
    template_name = "field.html"
    success_url = reverse_lazy('atspublic:site')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            video=-1
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"field.html",{"inventory": inv})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"field.html",{"inventory": inv, 'video':video})
        
class SoftwareView(View):
    template_name = "software.html"
    success_url = reverse_lazy('atspublic:software')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"software.html",{"inventory": inv})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"software.html",{"inventory": inv})
