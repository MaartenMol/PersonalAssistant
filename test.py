# importing the requests library 
import requests 
  
# api-endpoint 
URL = "https://www.ns.nl/rio-reisinfo-api/service/stations?q=" + "Oss"
  
# sending get request and saving the response as response object 
r = requests.get(url = URL) 
  
# extracting data in json format 
data = r.json() 
  
  
# extracting latitude, longitude and formatted address  
# of the first matching location 
station_id = data[0]['id'] 
station_naam = data[0]['naam'] 
  
# printing the output 
print(station_id + " " + station_naam) 