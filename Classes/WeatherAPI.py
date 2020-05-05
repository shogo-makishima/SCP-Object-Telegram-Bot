from requests import get
import Classes.Core.Settings as Settings

class WeatherAPI:
    __weather_current_url = "https://api.openweathermap.org/data/2.5/weather"
    __weather_forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def __init__(self): pass
    def GetWeatherByPosition(self, lat: float, lon: float) -> str:
        data = get(self.__weather_current_url, params={"lat": f"{lat}", "lon": f"{lon}", 'lang': 'ru', "APPID": Settings.APPID_OW}).json()

        weather_description = f"{data['weather'][0]['description']}".capitalize()
        weather_temp = f"{data['main']['temp']}"
        weather_pressure = f"{data['main']['pressure']}"
        weather_humidity = f"{data['main']['humidity']}"
        weather_wind_speed = f"{data['wind']['speed']}"

        return f"\n{weather_description}\n-> Температура: {weather_temp}°K | {round(float(weather_temp) - 273, 2)}°C\n-> Давление: {round(float(weather_pressure) * 100 / 133, 2)}мм. рт. ст.\n-> Влажность: {weather_humidity}%\n-> Ветер: {weather_wind_speed}м/с" #  , {weather_wind_deg}°

    def GetWeatherByCityName(self, city: str) -> str:
        data = get(self.__weather_current_url, params={"q": f"{city}", 'lang': 'ru', "APPID": Settings.APPID_OW}).json()

        weather_description = f"{data['weather'][0]['description']}".capitalize()
        weather_temp = f"{data['main']['temp']}"
        weather_pressure = f"{data['main']['pressure']}"
        weather_humidity = f"{data['main']['humidity']}"
        weather_wind_speed = f"{data['wind']['speed']}"

        return f"\n{weather_description}\n-> Температура: {weather_temp}°K | {round(float(weather_temp) - 273, 2)}°C\n-> Давление: {round(float(weather_pressure) * 100 / 133, 2)}мм. рт. ст.\n-> Влажность: {weather_humidity}%\n-> Ветер: {weather_wind_speed}м/с" #  , {weather_wind_deg}°


    def GetForecastWeatherByPosition(self, lat: float, lon: float, count: int = 1) -> list:
        data = get(self.__weather_forecast_url, params={"lat": f"{lat}", "lon": f"{lon}", 'lang': 'ru', "APPID": Settings.APPID_OW}).json()

        temp_list = list()

        if (count <= 40 and count > 0): weather_list = data["list"][:count]
        elif (count > 40): weather_list = data["list"][:40]
        elif (count < 0): weather_list = data["list"][:1]
        else: weather_list = None

        for weather in weather_list:
            temp_weather_description = weather['weather'][0]["description"].capitalize()
            temp_weather_temp = f"{weather['main']['temp']}"
            temp_weather_pressure = f"{weather['main']['pressure']}"
            temp_weather_humidity = f"{weather['main']['humidity']}"
            temp_weather_wind_speed = f"{weather['wind']['speed']}"
            temp_list.append(f"\n{weather['dt_txt']} -> {temp_weather_description}:\n-> Температура: {temp_weather_temp}°K | {round(float(temp_weather_temp) - 273, 2)}°C\n-> Давление: {round(float(temp_weather_pressure) * 100 / 133, 2)}мм. рт. ст.\n-> Влажность: {temp_weather_humidity}%\n-> Ветер: {temp_weather_wind_speed}м/с")

        return temp_list

    def GetForecastWeatherByCityName(self, city: str, count: int = 1) -> list:
        data = get(self.__weather_forecast_url, params={"q": f"{city}", 'lang': 'ru', "APPID": Settings.APPID_OW}).json()

        temp_list = list()

        if (count <= 40 and count > 0): weather_list = data["list"][:count]
        elif (count > 40): weather_list = data["list"][:40]
        elif (count < 0): weather_list = data["list"][:1]
        else: weather_list = None

        for weather in weather_list:
            temp_weather_description = weather['weather'][0]["description"].capitalize()
            temp_weather_temp = f"{weather['main']['temp']}"
            temp_weather_pressure = f"{weather['main']['pressure']}"
            temp_weather_humidity = f"{weather['main']['humidity']}"
            temp_weather_wind_speed = f"{weather['wind']['speed']}"
            temp_list.append(f"\n{weather['dt_txt']} -> {temp_weather_description}:\n-> Температура: {temp_weather_temp}°K | {round(float(temp_weather_temp) - 273, 2)}°C\n-> Давление: {round(float(temp_weather_pressure) * 100 / 133, 2)}мм. рт. ст.\n-> Влажность: {temp_weather_humidity}%\n-> Ветер: {temp_weather_wind_speed}м/с")

        return temp_list

# max_count = 40

"""
weather = WeatherAPI()

print(weather.GetWeatherByCityName("London"))
print(*weather.GetForecastWeatherByName("London", 4))

print(weather.GetWeatherByPosition(lat=54.55493, lon=36.329075))
print(*weather.GetForecastWeatherByPosition(lat=54.55493, lon=36.329075, count=40))
"""