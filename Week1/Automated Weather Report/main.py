import requests, os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")
def WeatherReport(cityName, data):
    weatherReport = f"""{cityName} Weather Forecast
Temperature:  {data['main']['temp']} C
Humidity: {data['main']['humidity']}%
Weather description: {data['weather'][0]['description']}
---------------------------------------------------------
"""
    return weatherReport
# -----------------------------------------------------------------------

with open("cities.txt", "r") as cityFile, open("weather_report.txt", "w") as reportFile:
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    reportFile.write(f"Weather Report generated at {timestamp}\n\n")
    for cityName in cityFile:
        cityName = cityName.strip()
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": cityName,
                "appid": api_key ,
                "units": "metric"
            }
        )
        if response.status_code == 200:
            data = response.json()
            weather = WeatherReport(cityName, data)
            reportFile.write(weather)
        else:
            print(f"Could not fetch weather for {cityName}. Skipping...")
            continue

