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
from atspublic.models import Blog, Category
from django.shortcuts import render_to_response, get_object_or_404
 
   
# Create your views here.
def index(request):
	return render(request,'atspublic/index.html')


class BlogView(View):
    template_name = "blog.html"
    success_url = reverse_lazy('blog:blog')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render_to_response('view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render_to_response('view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
       

class CategoryView(View):
    template_name = "blog.html"
    success_url = reverse_lazy('category:view_category_post')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            slug = request.POST.get('slug', -1)
            category = get_object_or_404(Category, slug=slug)
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render_to_response('view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
 

# Create your views here.
class PostView(View):
    template_name = "view_post.html"
    success_url = reverse_lazy('post:view_blog_post')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render_to_response('view_post.html', {'post': get_object_or_404(Blog, slug=slug)}) 
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render_to_response('view_post.html', {'post': get_object_or_404(Blog, slug=slug)})

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
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"robotLab.html",{"inventory": inv})
		
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
        return render (self.request,"field.html",{"inventory": inv})
        
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
