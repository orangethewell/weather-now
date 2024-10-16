from flask import Flask, render_template, request

app = Flask(__name__)

OWM_API_KEY = "9f4c4d69db3a59cdaef140a4bb8d400d"

import requests

class Weather:
    def __init__(self, city_string, weather_desc, icon_url, temp):
        self.city_string = city_string
        self.desc = weather_desc
        self.icon_url = icon_url
        self.temp = temp
        

def get_location(city_name, limit=5):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={OWM_API_KEY}&lang=pt_br"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            # Retorna as informações de localização
            return data
        else:
            return None
    else:
        return None

def get_current_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&lang=pt_br&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            # Retorna as informações de localização
            return data
        else:
            return None
    else:
        return None
    
def get_weather_information(query):
    location_data = get_location(query)[0]
    if not location_data:
        return None
    
    weather_data = get_current_weather(location_data["lat"], location_data["lon"])
    if not weather_data:
        return None
    
    return Weather(
        f"{location_data["name"]} - {location_data["state"]}",
        weather_data["weather"][0]["description"],
        f" https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}@2x.png",
        round(weather_data["main"]["temp"])
    )

@app.route("/")
def index():
    query = request.args.get("q")
    temp = 0

    if query:
        weather = get_weather_information(query)

        if weather:
            print(weather)
            return render_template("base.html", weather=weather)

    return render_template("base.html", weather=None)

if __name__ == "__main__":
    app.run(debug=True)