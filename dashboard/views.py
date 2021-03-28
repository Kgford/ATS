from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.views import View
from django.contrib.auth import authenticate
from accounts.models import Expenses, Invoice_Item, Charge_Code, Income, Invoice
from dashboard.models import Income_report
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
import datetime
import time
from re import search
load_id = 0

class UserLogin(View):
    template_name = "user_login.html"
    success_url = reverse_lazy('client:login')
        
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user.get_short_name())
        
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
            
class DashboardView(View):
    template_name = "index.html"
    success_url = reverse_lazy('dashboard:dashboard')
    def get(self, *args, **kwargs):
        try:
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
            operator = str(self.request.user.get_short_name())
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            #search for monthly invoices
            invoice_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            
            #search for yealy income
            items_year = Invoice_Item.objects.filter(item_date__year=thisyear)
            print('items_year =',items_year)
            rev_year=0
            for item in items_year:
                rev_year = round(rev_year + item.total,2)
                print('rev_year =',rev_year)
            
            #search for monthly income
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear, item_date__month=thismonth)
            rev_month=0
            for item in items_month:
                rev_month = round(rev_month + item.total,2)
                            
            #search for monthly expenses
            expense_month = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth)
            print('expense_month=',expense_month)
            exp_month=0
            insurance = 0
            travel = 0
            vehicle = 0
            taxes = 0 
            salarys = 0
            supplies = 0
            services = 0
            hardware = 0
            robot = 0
            for item in expense_month:
                exp_month = round(exp_month + float(item.total_cost),2)
                print('item-',item)
                if search('INSURANCE', item.expense_description.upper()):
                    insurance = insurance + float(item.total_cost)
                    print('insurance=',insurance)
                elif search('DATABASE', item.expense_description.upper()) or search('CONTRACTOR', item.expense_description.upper()) :
                    services = services + float(item.total_cost)
                    print('services=',services)
                elif search('TRAVEL', item.expense_description.upper()):
                    travel = travel + float(item.total_cost)
                    print('travel =',travel)
                elif search('TRAVEL', item.expense_type.upper()):
                    travel = travel + float(item.total_cost)
                    print('travel =',travel)
                elif search('VEHICLE', item.expense_description.upper()):
                    vehicle = vehicle + float(item.total_cost) * 0.3  # estimated 30% lease. will be calibrated later for acutal contract work miles
                    print('vehicle =',vehicle)
                elif search('SALARYS', item.expense_type.upper()):
                    salarys = salarys + float(item.total_cost)
                    print('salarys =',salarys)                    
                elif search('TAXES', item.expense_description.upper()):
                    taxes = taxes + float(item.total_cost)
                    print('taxes =',taxes) 
                elif search('SUPPLIES', item.expense_description.upper()):
                    supplies = supplies + float(item.total_cost)
                elif search('FIXTURES', item.expense_description.upper()) or search('ELECTRONICS', item.expense_description.upper()) or search('COMPUTERS', item.expense_description.upper()):
                    hardware = hardware + float(item.total_cost)
                elif search('ROBOT', item.expense_description.upper()):
                    robot = robot + float(item.total_cost)
                    #print('supplies =',supplies)
            expense_list_month = [services,insurance,travel,vehicle,taxes,supplies,hardware,robot]
            print('expense_list_month=',expense_list_month)
                           
            #search for yearly expenses
            expense_year = Expenses.objects.filter(sale_date__year=thisyear)
            exp_year=0
            insurance = 0
            travel = 0
            vehicle = 0
            taxes = 0 
            salarys = 0
            supplies = 0
            services = 0
            hardware = 0
            robot = 0
            for item in expense_year:
                #print('item-',item)
                exp_year= round(exp_year + float(item.total_cost),2)
                if search('INSURANCE', item.expense_description.upper()):
                    insurance = insurance + float(item.total_cost)
                    #print('insurance=',insurance)
                elif search('DATABASE', item.expense_description.upper()) or search('CONTRACTOR', item.expense_description.upper()) :
                    services = services + float(item.total_cost)
                    #print('services=',services)
                elif search('TRAVEL', item.expense_description.upper()):
                    travel = travel + float(item.total_cost)
                    #print('travel =',travel)
                elif search('TRAVEL', item.expense_type.upper()):
                    travel = travel + float(item.total_cost)
                    #print('travel =',travel)
                elif search('VEHICLE', item.expense_description.upper()):
                    vehicle = vehicle + float(item.total_cost) * 0.3  # estimated 30% lease. will be calibrated later for acutal contract work miles
                    #print('travel =',travel)
                elif search('SALARYS', item.expense_type.upper()):
                    salarys = salarys + float(item.total_cost)
                    #print('salarys =',salarys)                    
                elif search('TAXES', item.expense_description.upper()):
                    taxes = taxes + float(item.total_cost)
                    #print('taxes =',taxes) 
                elif search('SUPPLIES', item.expense_description.upper()):
                    supplies = supplies + float(item.total_cost)
                elif search('FIXTURES', item.expense_description.upper()) or search('ELECTRONICS', item.expense_description.upper()) or search('COMPUTERS', item.expense_description.upper()):
                    hardware = hardware + float(item.total_cost)
                elif search('ROBOT', item.expense_description.upper()):
                    robot = robot + float(item.total_cost)
                    #print('supplies =',supplies) 
                   
            expense_list_year  =  [services,insurance,travel,vehicle,taxes,supplies,hardware,robot]
            print('expense_list_year=',expense_list_year)
                
            #search for all unpaid invoices
            invoice_unpaid = Invoice.objects.filter(paid=False).all()
            
            #calculate yearly profit
            profit = round(float(rev_year)-float(exp_year),2)
            
            #search for income report chart data
            income_report = Income_report.objects.filter(year=thisyear)
            print('income_report=',income_report)
            months = []
            expen = []
            incom = []
            montharray = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            for report in income_report:
                if report.month:
                    months.append(montharray[str(report.month)])
                if report.income_paid:
                    expen.append(float(report.income_paid))
                else:
                    expen.append(0.00)
                if report.expense:
                    incom.append(float(report.expense))
                else:
                    expen.append(0.00)
            print('months=',months)
            print('expen=',expen)
            print('incom=',incom)
            #time.sleep(5)
            
           
            #search for most purchased Products for the year
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear)
            ate=0
            win=0
            web=0
            man=0
            auto=0
            robot=0
            total=0
            for item in items_month:
                total=total+1
                if item.service_type=='ATE Application':
                    ate=ate+1
                if item.service_type=='Windows Application':
                    win=win+1 
                if item.service_type=='Web Application':
                    web=web+1 
                if item.service_type=='Manual Test Fixture':
                    man=man+1 
                if item.service_type=='Automated Test Fixture':
                    auto=auto+1 
                if item.service_type=='Robot Test Fixture':
                    robot=robot+1
                
            if total !=0:
                ate = round(ate/total * 100,2)
                win = round(win/total * 100,2)
                web = round(web/total * 100,2)
                auto = round(auto/total * 100,2)
                man = round(man/total * 100,2)
                robot = round(robot/total * 100,2)
           
        except IOError as e:
           print('error = ',e) 
        return render(self.request, 'dashboard/index.html', {'operator':operator,'month_full':month_full,'month':month,'year':thisyear, 'invoice_month':invoice_month, 'invoice_unpaid':invoice_unpaid,'rev_year':rev_year, 'profit':profit, 
                                                             'rev_month':rev_month, 'exp_month':exp_month, 'months':months, 'expen':expen, 'incom':incom, 'expense_list_month':expense_list_month, 'expense_list_year':expense_list_year,
                                                             'avatar':avatar, 'year_list':year_list, 'month_list':month_list, 'ate':ate, 'win':win, 'web':web, 'auto':auto, 'man':man,'robot':robot })
 
    def post(self, request, *args, **kwargs):
        try:
            
            printnow = request.POST.get('_print', -1)
            
                
            thisyear = request.POST.get('_year', -1)
            month = request.POST.get('_month', -1)
            printnow = request.POST.get('_print', -1)
            year=thisyear
            print('year',year)
            print('month',month)
            timestamp = date.today()
            print('timestamp',timestamp)
            month_list = -1
            year_list = -1
            
            
            months = {'Jan': "1", 'Feb': "2",  'Mar': "3", 'Apr': '4', 'May': "5", 'Jun': "6", 'Jul': "7", 'Aug': "8", 'Sept': "9", 'Oct': "10", 'Nov': "11", 'Dec': "12"}
            full_months = {'Jan': "January", 'Feb': "February",  'Mar': "March", 'Apr': 'April', 'May': "May", 'Jun': "June", 'Jul': "July", 'Aug': "August", 'Sept': "September", 'Oct': "October", 'Nov': "November", 'Dec': "December"}
            thismonth = months[str(month)]
            print('thismonth',thismonth)
            month_full = full_months[str(month)]
            print('month =',month)
            operator = str(self.request.user.get_short_name())
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            #search for monthly invoices
            invoice_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            
            #search for yealy income
            items_year = Invoice_Item.objects.filter(item_date__year=thisyear)
            rev_year=0
            for item in items_year:
                rev_year = round(rev_year + item.total,2)
                #print('rev_year =',rev_year)
            
            #search for monthly income
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear, item_date__month=thismonth)
            rev_month=0
            for item in items_month:
                rev_month = round(rev_month + item.total,2)
                            
            #search for monthly expenses
            expense_month = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth)
            print('expense_month=',expense_month)
            exp_month=0
            insurance = 0
            travel = 0
            vehicle = 0
            taxes = 0 
            salarys = 0
            supplies = 0
            services = 0
            hardware = 0
            robot = 0
            for item in expense_month:
                exp_month = round(exp_month + float(item.total_cost),2)
                print('item-',item)
                if search('INSURANCE', item.expense_description.upper()):
                    insurance = insurance + float(item.total_cost)
                    #print('insurance=',insurance)
                elif search('DATABASE', item.expense_description.upper()) or search('CONTRACTOR', item.expense_description.upper()) :
                    services = services + float(item.total_cost)
                    #print('services=',services)
                elif search('TRAVEL', item.expense_description.upper()):
                    travel = travel  + float(item.total_cost)
                    #print('travel =',travel)
                elif search('TRAVEL', item.expense_type.upper()):
                    travel = travel  + float(item.total_cost)
                    #print('travel =',travel)
                elif search('VEHICLE', item.expense_description.upper()):
                    vehicle = vehicle + float(item.total_cost) * 0.3  # estimated 30% lease. will be calibrated later for acutal contract work miles
                    #print('vehicle =',vehicle)
                elif search('SALARYS', item.expense_type.upper()):
                    salarys = salarys  + float(item.total_cost)
                    #print('salarys =',salarys)                    
                elif search('TAXES', item.expense_description.upper()):
                    taxes = taxes  + float(item.total_cost)
                    #print('taxes =',taxes) 
                elif search('SUPPLIES', item.expense_description.upper()):
                    supplies = supplies  + float(item.total_cost)
                elif search('FIXTURES', item.expense_description.upper()) or search('ELECTRONICS', item.expense_description.upper()) or search('COMPUTERS', item.expense_description.upper()):
                    hardware = hardware  + float(item.total_cost)
                elif search('ROBOT', item.expense_description.upper()):
                    robot = robot  + float(item.total_cost)
                    #print('supplies =',supplies)
            expense_list_month = [services,insurance,travel,vehicle,taxes,supplies,hardware,robot]
            print('expense_list_month=',expense_list_month)
                           
            #search for yearly expenses
            expense_year = Expenses.objects.filter(sale_date__year=thisyear)
            exp_year=0
            insurance = 0
            travel = 0
            vehicle = 0
            taxes = 0 
            salarys = 0
            supplies = 0
            services = 0
            hardware = 0
            robot = 0
            for item in expense_year:
                #print('item-',item)
                exp_year= exp_year + float(item.total_cost)
                if search('INSURANCE', item.expense_description.upper()):
                    insurance = insurance + float(item.total_cost)
                    #print('insurance=',insurance)
                elif search('DATABASE', item.expense_description.upper()) or search('CONTRACTOR', item.expense_description.upper()) :
                    services = services + float(item.total_cost)
                    #print('services=',services)
                elif search('TRAVEL', item.expense_description.upper()):
                    travel = travel + float(item.total_cost)
                    #print('travel =',travel)
                elif search('TRAVEL', item.expense_type.upper()):
                    travel = travel + float(item.total_cost)
                    #print('travel =',travel)
                elif search('VEHICLE', item.expense_description.upper()):
                    vehicle = vehicle + float(item.total_cost) * 0.2  # estimated 30% lease. will be calibrated later for acutal contract work miles
                    #print('travel =',travel)
                elif search('SALARYS', item.expense_type.upper()):
                    salarys = salarys + float(item.total_cost) 
                    #print('salarys =',salarys)                    
                elif search('TAXES', item.expense_description.upper()):
                    taxes = taxes + float(item.total_cost)
                    #print('taxes =',taxes) 
                elif search('SUPPLIES', item.expense_description.upper()):
                    supplies = supplies + float(item.total_cost)
                elif search('FIXTURES', item.expense_description.upper()) or search('ELECTRONICS', item.expense_description.upper()) or search('COMPUTERS', item.expense_description.upper()):
                    hardware = hardware + float(item.total_cost)
                elif search('ROBOT', item.expense_description.upper()):
                    robot = robot + float(item.total_cost)
                    #print('supplies =',supplies) 
                   
            expense_list_year  =  [services,insurance,travel,vehicle,taxes,supplies,hardware,robot]
            print('expense_list_year=',expense_list_year)
            
            #search for all unpaid invoices
            invoice_unpaid = Invoice.objects.filter(paid=False).all()
           
           #calculate yearly profit
            profit = round(float(rev_year)-float(exp_year),2)
            
            #search for income report chart data
            income_report = Income_report.objects.filter(year=thisyear)
            months = []
            expen = []
            incom = []
            montharray = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            for report in income_report:
                if report.month:
                    months.append(montharray[str(report.month)])
                    #print('report.month=',report.month)
                if report.income_paid:
                    expen.append(float(report.income_paid))
                else:
                    expen.append(0.00)
                if report.expense:
                    incom.append(float(report.expense))
                else:
                    expen.append(0.00)
            print('months=',months)
            print('expen=',expen)
            print('incom=',incom)
            #time.sleep(5)
            
           
            #search for most purchased Products for the year
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear)
            ate=0
            win=0
            web=0
            man=0
            auto=0
            robot=0
            total=0
            for item in items_month:
                total=total+1
                if item.service_type=='ATE Application':
                    ate=ate+1
                if item.service_type=='Windows Application':
                    win=win+1 
                if item.service_type=='Web Application':
                    web=web+1 
                if item.service_type=='Manual Test Fixture':
                    man=man+1 
                if item.service_type=='Automated Test Fixture':
                    auto=auto+1 
                if item.service_type=='Robot Test Fixture':
                    robot=robot+1
                
            if total !=0:
                ate = round(ate/total * 100,2)
                win = round(win/total * 100,2)
                web = round(web/total * 100,2)
                auto = round(auto/total * 100,2)
                man = round(man/total * 100,2)
                robot = round(robot/total * 100,2)
            print(thisyear)
            print(month)
            print(thisyear)
                                        
        except IOError as e:
           print('error = ',e) 
        return render(self.request, 'dashboard/index.html', {'operator':operator,'month_full':month_full,'month':month,'year':thisyear, 'invoice_month':invoice_month, 'invoice_unpaid':invoice_unpaid,'rev_year':rev_year, 'profit':profit, 
                                                     'rev_month':rev_month, 'exp_month':exp_month, 'months':months, 'expen':expen, 'incom':incom, 'expense_list_month':expense_list_month, 'expense_list_year':expense_list_year,
                                                     'avatar':avatar, 'year_list':year_list, 'month_list':month_list, 'ate':ate, 'win':win, 'web':web, 'auto':auto, 'man':man,'robot':robot })

                               
                                                            
                                                            
class ReportView(View):
    template_name = "report.html"
    success_url = reverse_lazy('dashboard:report')
    def get(self, *args, **kwargs):
        try:
            thisyear = self.request.GET.get('year', -1)
            thismonth  = self.request.GET.get('month', -1)
            year = thisyear
            month = thismonth
            print('year',year)
            print('month',month)
            timestamp = date.today()
            print('timestamp',timestamp)
            month_list = -1
            year_list = -1
            months = {'Jan': "1", 'Feb': "2",  'Mar': "3", 'Apr': '4', 'May': "5", 'Jun': "6", 'Jul': "7", 'Aug': "8", 'Sept': "9", 'Oct': "10", 'Nov': "11", 'Dec': "12"}
            full_months = {'Jan': "January", 'Feb': "February",  'Mar': "March", 'Apr': 'April', 'May': "May", 'Jun': "June", 'Jul': "July", 'Aug': "August", 'Sept': "September", 'Oct': "October", 'Nov': "November", 'Dec': "December"}
            thismonth = months[str(month)]
            print('thismonth',thismonth)
            month_full = full_months[str(month)]
            print('month =',month)
            operator = str(self.request.user.get_short_name())
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            year_list =  Income_report.objects.order_by('year').values_list('year', flat=True).distinct()
            month_list =  Income_report.objects.order_by('month_str').values_list('month_str', flat=True).distinct()
            #search for monthly invoices
            invoice_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            
            #search for yealy income
            items_year = Invoice_Item.objects.filter(item_date__year=thisyear)
            rev_year=0
            for item in items_year:
                rev_year = round(rev_year + item.total,2)
                #print('rev_year =',rev_year)
            
            #search for monthly income
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear, item_date__month=thismonth)
            rev_month=0
            for item in items_month:
                rev_month = round(rev_month + item.total,2)
                            
            #search for monthly expenses
            expense_month = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth)
            print('expense_month=',expense_month)
            exp_month=0
            insurance = 0
            travel = 0
            vehicle = 0
            taxes = 0 
            salarys = 0
            supplies = 0
            services = 0
            hardware = 0
            robot = 0
            for item in expense_month:
                exp_month = round(exp_month + float(item.total_cost),2)
                print('item-',item)
                if search('INSURANCE', item.expense_description.upper()):
                    insurance = insurance + float(item.total_cost)
                    print('insurance=',insurance)
                elif search('DATABASE', item.expense_description.upper()) or search('CONTRACTOR', item.expense_description.upper()) :
                    services = services + float(item.total_cost)
                    print('services=',services)
                elif search('TRAVEL', item.expense_description.upper()):
                    travel = travel + float(item.total_cost)
                    print('travel =',travel)
                elif search('TRAVEL', item.expense_type.upper()):
                    travel = travel + float(item.total_cost)
                    print('travel =',travel)
                elif search('VEHICLE', item.expense_description.upper()):
                    vehicle = vehicle + float(item.total_cost) * 0.3  # estimated 30% lease. will be calibrated later for acutal contract work miles
                    print('vehicle =',vehicle)
                elif search('SALARYS', item.expense_type.upper()):
                    salarys = salarys + float(item.total_cost)
                    print('salarys =',salarys)                    
                elif search('TAXES', item.expense_description.upper()):
                    taxes = taxes + float(item.total_cost)
                    print('taxes =',taxes) 
                elif search('SUPPLIES', item.expense_description.upper()):
                    supplies = supplies + float(item.total_cost)
                elif search('FIXTURES', item.expense_description.upper()) or search('ELECTRONICS', item.expense_description.upper()) or search('COMPUTERS', item.expense_description.upper()):
                    hardware = hardware + float(item.total_cost)
                elif search('ROBOT', item.expense_description.upper()):
                    robot = robot + float(item.total_cost)
                    #print('supplies =',supplies)
            expense_list_month = [services,insurance,travel,vehicle,taxes,supplies,hardware,robot]
            print('expense_list_month=',expense_list_month)
                           
            #search for yearly expenses
            expense_year = Expenses.objects.filter(sale_date__year=thisyear)
            exp_year=0
            insurance = 0
            travel = 0
            vehicle = 0
            taxes = 0 
            salarys = 0
            supplies = 0
            services = 0
            hardware = 0
            robot = 0
            for item in expense_year:
                #print('item-',item)
                exp_year= round(exp_year + float(item.total_cost),2)
                if search('INSURANCE', item.expense_description.upper()):
                    insurance = insurance + float(item.total_cost)
                    #print('insurance=',insurance)
                elif search('DATABASE', item.expense_description.upper()) or search('CONTRACTOR', item.expense_description.upper()) :
                    services = services + float(item.total_cost)
                    #print('services=',services)
                elif search('TRAVEL', item.expense_description.upper()):
                    travel = travel + float(item.total_cost)
                    #print('travel =',travel)
                elif search('TRAVEL', item.expense_type.upper()):
                    travel = travel + float(item.total_cost)
                    #print('travel =',travel)
                elif search('VEHICLE', item.expense_description.upper()):
                    vehicle = vehicle + float(item.total_cost) * 0.3  # estimated 30% lease. will be calibrated later for acutal contract work miles
                    #print('travel =',travel)
                elif search('SALARYS', item.expense_type.upper()):
                    salarys = salarys + float(item.total_cost)
                    #print('salarys =',salarys)                    
                elif search('TAXES', item.expense_description.upper()):
                    taxes = taxes + float(item.total_cost)
                    #print('taxes =',taxes) 
                elif search('SUPPLIES', item.expense_description.upper()):
                    supplies = supplies + float(item.total_cost)
                elif search('FIXTURES', item.expense_description.upper()) or search('ELECTRONICS', item.expense_description.upper()) or search('COMPUTERS', item.expense_description.upper()):
                    hardware = hardware + float(item.total_cost)
                elif search('ROBOT', item.expense_description.upper()):
                    robot = robot + float(item.total_cost)
                    #print('supplies =',supplies) 
                   
            expense_list_year  =  [services,insurance,travel,vehicle,taxes,supplies,hardware,robot]
            print('expense_list_year=',expense_list_year)
                
            #search for all unpaid invoices
            invoice_unpaid = Invoice.objects.filter(paid=False).all()
            
            #calculate yearly profit
            profit = round(float(rev_year)-float(exp_year),2)
            
            #search for income report chart data
            income_report = Income_report.objects.filter(year=thisyear)
            months = []
            expen = []
            incom = []
            montharray = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            for report in income_report:
                if report.month:
                    months.append(montharray[str(report.month)])
                if report.income_paid:
                    expen.append(float(report.income_paid))
                else:
                    expen.append(0.00)
                if report.expense:
                    incom.append(float(report.expense))
                else:
                    expen.append(0.00)
            print('months=',months)
            print('expen=',expen)
            print('incom=',incom)
            #time.sleep(5)
            
           
            #search for most purchased Products for the year
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear)
            ate=0
            win=0
            web=0
            man=0
            auto=0
            robot=0
            total=0
            for item in items_month:
                total=total+1
                if item.service_type=='ATE Application':
                    ate=ate+1
                if item.service_type=='Windows Application':
                    win=win+1 
                if item.service_type=='Web Application':
                    web=web+1 
                if item.service_type=='Manual Test Fixture':
                    man=man+1 
                if item.service_type=='Automated Test Fixture':
                    auto=auto+1 
                if item.service_type=='Robot Test Fixture':
                    robot=robot+1
                
            if total !=0:
                ate = round(ate/total * 100,2)
                win = round(win/total * 100,2)
                web = round(web/total * 100,2)
                auto = round(auto/total * 100,2)
                man = round(man/total * 100,2)
                robot = round(robot/total * 100,2)
           
        except IOError as e:
           print('error = ',e) 
        return render(self.request, 'dashboard/report.html', {'operator':operator,'month_full':month_full,'month':month,'year':thisyear, 'invoice_month':invoice_month, 'invoice_unpaid':invoice_unpaid,'rev_year':rev_year, 'profit':profit, 
                                                             'rev_month':rev_month, 'exp_month':exp_month, 'months':months, 'expen':expen, 'incom':incom, 'expense_list_month':expense_list_month, 'expense_list_year':expense_list_year,
                                                             'avatar':avatar, 'year_list':year_list, 'month_list':month_list, 'ate':ate, 'win':win, 'web':web, 'auto':auto, 'man':man,'robot':robot })                                                  
                                                