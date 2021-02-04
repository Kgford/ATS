import math
import os, requests
from client.models import Clients
from contractors.models import Contractors
from googlevoice import Voice
#from googlevoice.util import input
from six.moves import input
import sys
from ATS import settings
from django.core.mail import send_mail


#https://data-flair.training/blogs/django-send-email/
class Email:
    def __init__ (self, recepient_list,subject,message):
        self.subject = subject
        self.message = message
        self.recepient = recepient_list
        print('recepient=',self.recepient)
        if not isinstance(self.recepient, list):
            self.recepient = [self.recepient]
            print('recepient=',self.recepient)
    
    def send_email(self):
        print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        res = send_mail(self.subject, self.message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False)
        print('response=',res)
        return res



#https://sphinxdoc.github.io/pygooglevoice/examples.html#send-sms-messages
class Comunication:
    def __init__ (self, number,message):
        print('number=',number)
        numeric_filter = filter(str.isdigit, str(number))
        number = "".join(numeric_filter)
        print('numeric_string=',number)
        self.number = '+1' + number
        self.message = message
        print('message=',self.message)
        print('number=',self.number)
    

    def send_sms(self):
        till_username = settings.TILL_USERNAME
        till_api_key = settings.TILL_API_KEY
                        
        requests.post(
            "https://platform.tillmobile.com/api/send?username=%s&api_key=%s" % (
                till_username,
                till_api_key
            ), 
            json={
                "phone": [self.number],
                "text" : self.message,
                "tag": "New User Alert"
            }
        )
    def send_sms_question(self):
        till_username = settings.TILL_USERNAME
        till_api_key = settings.TILL_API_KEY

        requests.post(
            "https://platform.tillmobile.com/api/send?username=%s&api_key=%s" % (
                till_username,
                till_api_key
            ), 
            json={
                "phone": [self.number],
                "introduction": "Hello from Till.",
                "questions" : [{
                    "text": "Do you have a few moments to answer a question or two?",
                    "tag": "have_a_few_moments",
                    "responses": ["Yes", "No"],
                    "conclude_on": "No",
                    "webhook": "https://yourapp.com/have_a_few_moments_results/"
                },
                {
                    "text": "What is your favorite color?",
                    "tag": "favorite_color",
                    "responses": ["Red", "Green", "Yellow"],
                    "webhook": "https://yourapp.com/favorite_color_results/"
                },
                {
                    "text": "Who is you favorite Star Wars character?",
                    "tag": "favorite_star_wars_character",
                    "webhook": "https://yourapp.com/favorite_star_wars_character_results/"
                }],
                "conclusion": "Thank you for your time"
            }
        )
        
    
    
    def call(self):
        user = 'atetestalerts@gmail.com'
        password = 'Gadget2021'
        print('self.number=',self.number)
        voice = Voice()
        print('voice=',voice)
        print(voice.login(user, password))
        print('in communication')
        outgoingNumber = input('Number to call: ')
        forwardingNumber = input('Number to call from [optional]: ') or None

        voice.call(outgoingNumber, forwardingNumber)

        if input('Calling now... cancel?[y/N] ').lower() == 'y':
            voice.cancel(outgoingNumber, forwardingNumber)
    
    def voice_mails(self):
        user = 'atetestalerts@gmail.com'
        password = 'Gadget2021'
        print('self.number=',self.number)
        voice = Voice()
        print('voice=',voice)
        print(voice.login(user, password))
        print('in communication')
        for message in voice.voicemail().messages:
            util.print_(message)
        
    def delete_messages(self):
        user = 'atetestalerts@gmail.com'
        password = 'Gadget2021'
        print('self.number=',self.number)
        voice = Voice()
        print('voice=',voice)
        print(voice.login(user, password))
        print('in communication')
        for message in voice.sms().messages:
            if message.isRead:
                message.delete()
        
    

#https://www.programiz.com/python-programming/modules/math
class Equations:
    def __init__ (self, client_id,contractor_id):
        self.client_id = client_id
        self.contractor_id = contractor_id
    
    def travel_distance(self): 
        try:
            client = Clients.objects.filter(id=self.client_id).first()
            longitude1 = client.lng
            latitude1 = client.lat
                        
            contractor = Contractors.objects.filter(id=self.contractor_id).first()
            longitude2 = contractor.lng
            latitude2 = contractor.lat
            dist=self.distance(latitude1, longitude1, latitude2, longitude2, "N")
            
            return dist
        except IOError as e:
            print('error = ',e) 
            return 0
   
    
    
    def distance(self,lat1,lon1,lat2,lon2,unit):
        try:
            if lat1==lat2 and lon1==lon2:
                return 0
            else:
                theta = lon1 - lon2
                
                dist = math.sin(self.deg2rad(lat1)) * math.sin(self.deg2rad(lat2)) + math.cos(self.deg2rad(lat1)) * math.cos(self.deg2rad(lat2)) * math.cos(self.deg2rad(theta))
                dist = math.acos(dist)
                dist = self.rad2deg(dist)
                dist = dist * 60 * 1.1515
                if unit == "K":
                    dist = dist * 1.609344
                elif unit == "N":
                    dist = dist * 0.8684
                return dist
        except IOError as e:
            print('error = ',e) 
            return 0            
            
   
    def deg2rad (self,deg):
        ans = deg * math.pi / 180.0
        return ans
        
    def rad2deg (self,rad):
        ans = rad / math.pi * 180.0
        return ans
        
    def get_num(self,x):
        return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
    
    