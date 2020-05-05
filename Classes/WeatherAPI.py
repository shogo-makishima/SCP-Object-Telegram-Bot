from requests import get
import Classes.Core.Settings as Settings

class WeatherAPI:
    __weather_current_url = "https://api.openweathermap.org/data/2.5/weather"
    def __init__(self): pass
    def GetWeatherByPosition(self, lat: float, lon: float) -> str:
        data = get(self.__weather_current_url, params={"lat": f"{lat}", "lon": f"{lon}", 'lang': 'ru', "APPID": Settings.APPID_OW}).json()

        weather_description = f"{data['weather'][0]['description']}".capitalize()
        weather_temp = f"{data['main']['temp']}"
        weather_pressure = f"{data['main']['pressure']}"
        weather_humidity = f"{data['main']['humidity']}"
        weather_wind_speed = f"{data['wind']['speed']}"

        return f"{weather_description} -> Температура: {weather_temp}°F | {round(float(weather_temp) - 273, 2)}°C -> Давление: {round(float(weather_pressure) * 100 / 133, 2)}мм. рт. ст. -> Влажность: {weather_humidity}% -> Ветер: {weather_wind_speed}м/с" #  , {weather_wind_deg}°


weather = WeatherAPI()
print(weather.GetWeatherByPosition(lat=54.55493, lon=36.329075))
