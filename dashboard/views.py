from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.views import View
from django.contrib.auth import authenticate
from accounts.models import Expenses, Invoice_Item, Charge_Code, Income, Invoice
from dashboard.models import Income_report
import datetime
import time


class DashboardView(View):
    template_name = "index.html"
    success_url = reverse_lazy('dashboard:dashboard')
    def get(self, *args, **kwargs):
        try:
            
            
            
            '''
            timestamp = date.today()
            dt = datetime.datetime.today()
            thisyear = dt.year
            thismonth = dt.month
            thisday = dt.day
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            monthstr = months[str(thismonth)]
            invoices = Invoice.objects.all()
            print('invoices=',invoices)
            for y in range(2017, int(dt.year) + 1):
                for m in range(1, int(dt.month) + 1):
                    temp_date = str(y) + "-" + str(m)  + "-" + str(1)
                    invoices = Invoice_Item.objects.filter(item_date__month=m, item_date__year=y).all()
                    print(invoices)
                    total=0
                    if invoices:
                        for inv in invoices:
                            total = inv.total
                            invoice_date = inv.item_date
                            print('invoice_date =',invoice_date)
                            client_id = inv.client_id
                            print('client_id =',client_id)
                            if inv.total:
                                total = total + float(inv.total)
                            print('total =',total)
                            paid = True
                            print('paid =',paid)
                            income = total
                            if paid:
                                income_paid = total
                                income_unpaid = 0
                            else:
                                income_paid = 0
                                income_unpaid = total
                            
                            print('invoice_date =',invoice_date)
                            invoice_date=str(invoice_date)
                            split_date = invoice_date.split("-")
                            year = int(split_date[0])
                            print('year =',year)
                            month = int(split_date[1])
                            print('month =',month)
                            day = int(split_date[2])
                            print('day =',day)
                            temp_year = year
                            temp_month = month
                            monthstr = months[str(temp_month)]
                            temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                                              
                        monthstr = months[str(m)]
                        temp_date = str(y) + "-" + str(m)  + "-" + str(day)
                        if not Income_report.objects.filter(month=m, year=y).exists():
                            Income_report.objects.create(client_id=client_id, month_str=monthstr, month=m, year=y,
                                                  income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                        else:
                            Income_report.objects.filter(month=temp_month, year=y).update(income_total=income, income_paid=income_paid, income_unpaid=income_unpaid)
                            
                        if not Income.objects.filter(month=m, year=y).exists():
                            Income_report.objects.create(client_id=client_id, month_str=monthstr, month=m, year=y,
                                                  income_total=income, income_paid=income_paid, income_unpaid=income_unpaid, last_update=timestamp)
                        else:
                            Income_report.objects.filter(month=temp_month, year=y).update(income_total=income, income_paid=income_paid, income_unpaid=income_unpaid)
                        
                        print('income_total =',income)                          
                        print('updated income report for date: ',temp_date)
                        #time.sleep(5)
                
            
            for y in range(2017, int(dt.year) + 1):
                for m in range(1, int(dt.month) + 1):
                    expenses = Expenses.objects.filter(sale_date__month=m, sale_date__year=y).all()
                    temp_date = str(y) + "-" + str(m)  + "-" + str(1)
                    print('expenses=',expenses)
                    if expenses:
                        total = 0
                        for exp in expenses:
                            sale_date = exp.sale_date
                            print('sale_date =',sale_date)
                            if exp.total_cost:
                                total = total + float(exp.total_cost)
                            print('expense_total =',total)
                            sale_date=str(sale_date)
                            split_date = sale_date.split("-")
                            year = int(split_date[0])
                            print('year =',year)
                            month = int(split_date[1])
                            print('month =',month)
                            day = 1
                            print('day =',day)
                            temp_year = year
                            temp_month = month
                            temp_date = str(temp_year) + "-" + str(temp_month)  + "-" + str(day)
                            print('temp_date =',temp_date)
                            print('total =',total)
                            
                        
                        Income_report.objects.filter(month=m, year=y).update(expense=total)
                        print('updated income report expenses for date: ',temp_date)
                        print('total =',total)
                        #time.sleep(5)
                        '''          
            
            
            
            
            
            
            
            
            
            
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
                months.append(montharray[str(report.month)])
                expen.append(float(report.income_paid))
                incom.append(float(report.expense))
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
            
            new_date = request.POST.get('_date', -1)
            print('new_date',new_date)
            timestamp = date.today()
            print('timestamp',timestamp)
            if new_date ==-1:
                dt = datetime.datetime.today()
                thisyear = dt.year
                thismonth = dt.month
                thisday = dt.day
            else:
                split_date = new_date.split("-")
                print('split_date =',split_date)
                thisyear = int(split_date[0])
                thismonth = int(split_date[1])
                thisday = int(split_date[2])
                
            send_month = str(thismonth)
            if len(send_month)==1:
                send_month = '0' + send_month
            send_day = str(thisday)
            if len(send_day )==1:
                send_day  = '0' + send_day     
            send_date = str(thisyear) + '-' + send_day + '-' + send_month
            print('send_date=',send_date)
            months = {'1': "Jan", '2': "Feb",  '3': "Mar", '4': 'Apr', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            full_months = {'1': "Janurary", '2': "Februay",  '3': "March", '4': 'April', '5': "May", '6': "June", '7': "July", '8': "August", '9': "September", '10': "October", '11': "November", '12': "December"}
            month = months[str(thismonth)]
            month_full = full_months[str(thismonth)]
            #print('month =',month)
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
                months.append(montharray[str(report.month)])
                expen.append(float(report.income_paid))
                incom.append(float(report.expense))
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
                               
                                                            
                                                            
                                                            
                                                            