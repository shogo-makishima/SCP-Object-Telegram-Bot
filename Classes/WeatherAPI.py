from requests import get

class WeatherAPI:
    __weather_current_url = "https://api.openweathermap.org/data/2.5/weather"
    def __init__(self): pass
    def GetWeatherByPosition(self, lat: float, lon: float) -> str:
        data = get(self.__weather_current_url, params={"lat": f"{lat}", "lon": f"{lon}", "APPID": "23b36e2d0634d4352ea52ad2ab028ea1"}).json()

        weather_main = f"{data['weather'][0]['main']}"
        weather_description = f"{data['weather'][0]['description']}"
        weather_temp = f"{data['main']['temp']}"
        weather_pressure = f"{data['main']['pressure']}"
        weather_humidity = f"{data['main']['humidity']}"
        weather_wind_speed = f"{data['wind']['speed']}"
        # weather_wind_deg = f"{data['wind']['deg']}"
        # print(data)
        return f"{weather_main}: {weather_description} -> Temperature: {weather_temp}°F | {round(float(weather_temp) - 273, 2)}°C -> Pressure: {round(float(weather_pressure) * 100 / 133, 2)}mm Hg -> Humidity: {weather_humidity}% -> Wind: {weather_wind_speed}m/s, {weather_wind_deg}°"

"""
weather = WeatherAPI()
print(weather.GetWeatherByPosition(lat=54.55493, lon=36.329075))
"""