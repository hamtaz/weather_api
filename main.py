import requests
import redis
import sys

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class WeatherData:
    def __init__(self, day, country, temp, description):
        self.day = day
        self.country = country
        self.temp = temp
        self.description = description
        
    def to_dict(self):
        return {
            "Day": self.day,
            "Country": self.country,
            "Temp": self.temp,
            "Description": self.description
        }

def get_weather():
    place = input("Enter Address, partial address, or lat,lon / quit to exit: ")
    
    if place.lower() == "quit":
        sys.exit()
    
    cached_data = redis_client.get(f"weather:{place}")
    if cached_data:
        print("Data loaded from cache")
        return cached_data
    
    try:
        api_link = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{place}?unitGroup=metric&include=current&key=LM4GMBNWSGYADVYXVUNVNET8V&contentType=json"
    
        response = requests.get(api_link)
        data = response.json()
        weather_data = WeatherData(
            data["days"][0]["datetime"], 
            data["resolvedAddress"], 
            data["days"][0]["temp"], 
            data["days"][0]["description"]
        )
        
        weather_dict = weather_data.to_dict()
        redis_client.setex(f"weather:{place}", 900, str(weather_dict))
        return weather_dict
    except:
        return f"Error code: {response.status_code}"
while True:
    print(get_weather())