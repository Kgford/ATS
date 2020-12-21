from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.views import View
from django.contrib.auth import authenticate


class DashboardView(View):
    template_name = "index.html"
    success_url = reverse_lazy('dashboard:dashboard')
        
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user)
        
        except IOError as e:
           print('error = ',e) 
        return render(self.request, 'dashboard/index.html', {'operator':operator})
 
    def post(self, request, *args, **kwargs):
        try:
            operator = str(self.request.user)
    
        except IOError as e:
            print('error = ',e) 
        return render(self.request, 'dashboard/index.html', {'operator':operator})