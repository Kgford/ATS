from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.views import View
from django.contrib.auth import authenticate
from accounts.models import Expenses, Invoice_Item, Charge_Code, Income, Invoice
from dashboard.models import Income_report
from django.contrib.auth.decorators import login_required
import datetime
import time


class DashboardView(View):
    template_name = "index.html"
    success_url = reverse_lazy('dashboard:dashboard')
    def get(self, *args, **kwargs):
        try:
            send_date = -1
            timestamp = date.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            thismonth = dt.month
            thisday = dt.day
            send_month = str(thismonth)
            print('send_date=',send_date)
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            full_months = {'1': "Janurary", '2': "Februay",  '3': "March", '4': 'April', '5': "May", '6': "June", '7': "July", '8': "August", '9': "September", '10': "October", '11': "November", '12': "December"}
            month = months[str(thismonth)]
            month_full = full_months[str(thismonth)]
            print('month =',month)
            operator = str(self.request.user)
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            #search for monthly invoices
            invoice_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            
            #search for yealy income
            items_year = Invoice_Item.objects.filter(item_date__year=thisyear)
            rev_year=0
            for item in items_year:
                rev_year = rev_year + item.total
                #print('rev_year =',rev_year)
            
            #search for monthly income
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear, item_date__month=thismonth)
            rev_month=0
            for item in items_month:
                rev_month = rev_month + item.total
                            
            #search for monthly expenses
            expense_month = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth)
            exp_month=0
            for item in expense_month:
               exp_month = exp_month + float(item.total_cost)
                           
            #search for yearly expenses
            expense_year = Expenses.objects.filter(sale_date__year=thisyear)
            exp_year=0
            for item in expense_year:
                exp_year= exp_year + float(item.total_cost)
               
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
        return render(self.request, 'dashboard/index.html', {'operator':operator,'month_full':month_full,'month':month,'year':thisyear, 'invoice_month':invoice_month, 'invoice_unpaid':invoice_unpaid,
                                                            'rev_year':rev_year, 'profit':profit,  'rev_month':rev_month, 'exp_month':exp_month, 'months':months, 'expen':expen, 'incom':incom,
                                                             'avatar':avatar, 'send_date':send_date, 'ate':ate, 'win':win, 'web':web, 'auto':auto, 'man':man,'robot':robot })
 
    def post(self, request, *args, **kwargs):
        try:
            refresh = request.POST.get('_select', -1)
            new_date = request.POST.get('_date', -1)
            print('new_date',new_date)
            print('refresh',refresh)
            timestamp = date.today()
            print('timestamp',timestamp)
            
            if new_date !=-1:
                split_date = new_date.split("-")
                print('split_date =',split_date)
                thisyear = int(split_date[0])
                thismonth = int(split_date[1])
                thisday = int(split_date[2])
            else:
                thisyear = dt.year
                thismonth = dt.month
                thisday = dt.day
                
            send_month = str(thismonth)
            if len(send_month)==1:
                send_month = '0' + send_month
            send_day = str(thisday)
            if len(send_day )==1:
                send_day  = '0' + send_day     
            send_date = str(thisyear) + '-' + str(thismonth) + '-' + str(thisday)
            print('send_date=',send_date)
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            full_months = {'1': "Janurary", '2': "Februay",  '3': "March", '4': 'April', '5': "May", '6': "June", '7': "July", '8': "August", '9': "September", '10': "October", '11': "November", '12': "December"}
            month = months[str(thismonth)]
            month_full = full_months[str(thismonth)]
            print('month =',month)
            operator = str(self.request.user)
            avatar = 'dashboard/images/avatars/' + operator + '.jpeg'
            #search for monthly invoices
            invoice_month = Invoice.objects.filter(invoice_date__year=thisyear, invoice_date__month=thismonth)
            
            #search for yealy income
            items_year = Invoice_Item.objects.filter(item_date__year=thisyear)
            rev_year=0
            for item in items_year:
                rev_year = rev_year + item.total
                #print('rev_year =',rev_year)
            
            #search for monthly income
            items_month = Invoice_Item.objects.filter(item_date__year=thisyear, item_date__month=thismonth)
            rev_month=0
            for item in items_month:
                rev_month = rev_month + item.total
                            
            #search for monthly expenses
            expense_month = Expenses.objects.filter(sale_date__year=thisyear, sale_date__month=thismonth)
            exp_month=0
            for item in expense_month:
               exp_month = exp_month + float(item.total_cost)
                           
            #search for yearly expenses
            expense_year = Expenses.objects.filter(sale_date__year=thisyear)
            exp_year=0
            for item in expense_year:
                exp_year= exp_year + float(item.total_cost)
               
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
                    print('report.month=',report.month)
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
        return render(self.request, 'dashboard/index.html', {'operator':operator,'month_full':month_full,'month':month,'year':thisyear, 'invoice_month':invoice_month, 'invoice_unpaid':invoice_unpaid,
                                                            'rev_year':rev_year, 'profit':profit,  'rev_month':rev_month, 'exp_month':exp_month, 'months':months, 'expen':expen, 'incom':incom,
                                                             'avatar':avatar, 'send_date':send_date, 'ate':ate, 'win':win, 'web':web, 'auto':auto, 'man':man,'robot':robot })
                               
                                                            
                                                            
                                                            
                                                            