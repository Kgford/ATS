import math
from client.models import Clients
from contractors.models import Contractors

#https://www.programiz.com/python-programming/modules/math
class Equations:
    def travel_distance(self,client_id,contractor_id): 
        try:
            client = Clients.objects.filter(id=client_id).first()
            longitude1 = client.lng
            latitude1 = client.lat
                        
            contractor = Contractors.objects.filter(id=contractor_id).first()
            longitude2 = contractor.lng
            latitude2 = contractor.lat
            
            return distance(latitude1, longitude1, latitude2, longitude2, "N")
        except IOError as e:
            print('error = ',e) 
            return 0
   
    
    
    def distance(self,lat1,lon1,lat2,lon2,unit):
        try:
            if lat1==lat2 and lon1==lon2:
                return 0
            else:
                theta = lon1 - lon2
                dist = math.sin(deg2rad(lat1)) * math.sin(deg2rad(lat2)) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.cos(deg2rad(theta))
                dist = math.acos(dist)
                dist = rad2deg(dist)
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
        return deg * math.pi / 180.0
        
    def deg2rad (self,rad):
        return rad / math.pi * 180.0
    
    