import requests
import redis
from redis.cache import CacheConfig
class WeatherData:
    def __init__(self, day, country, temp, description):
        self.day = day
        self.country = country
        self.temp = temp
        self.description = description
        
    def __str__(self):
        return f"\nDay: {self.day}\nCity / Country: {self.country}\nTemperature (Celcius): {self.temp}\nDesc: {self.description}\n"

def get_api():
    place = input("Enter Address, partial address, or lat,lon: ")
    try:
        api_link = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{place}?unitGroup=metric&include=current&key=LM4GMBNWSGYADVYXVUNVNET8V&contentType=json"
    
        response = requests.get(api_link)
        data = response.json()
    
        weather_data = WeatherData(data["days"][0]["datetime"], data["days"][1]["description"], data["resolvedAddress"], data["days"][0]["temp"])
        return weather_data
    except:
        return f"Connection Error {response.status_code}"


print(get_api())