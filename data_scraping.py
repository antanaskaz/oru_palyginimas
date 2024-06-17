from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
from datetime import date, timedelta


def get_cities():
    url = "https://lt.wikipedia.org/wiki/Sąrašas:Lietuvos_miestai"
    response = requests.get(url)
    city_table = pd.read_html(StringIO(response.text))[1]
    city_names = city_table.loc[:, "Miestas"]
    return list(city_names)


def get_weather_info(city_name: str, today_only: bool = False):
    if type(city_name) is str:
        link = f"{city_to_link(city_name)}"
        source = requests.get(f"https://www.tv3.lt/orai/{link}").text
        soup = BeautifulSoup(source, "html.parser")
        block = soup.find("div", class_="first-item")
        blocks = block.find_all("div", class_="infoRow")
        if not blocks:
            return None
        city_weather_info = [{}] * 6
        date_today = date.today().strftime("%Y-%m-%d")
        city_weather_info[0] = {}
        city_weather_info[0]["city"] = city_name
        city_weather_info[0]["date_current"] = str(date_today)
        city_weather_info[0]["date_for"] = str(date_today)
        # Todays weather information
        for index, info in enumerate(blocks):
            if index == 0:
                temperature = info.find("div", class_="infoCol right").text.strip()
                temperature = temperature.replace("°", "")
                temperature = temperature.replace("+", "")
                temperature = temperature.replace(" ", "")
                temperature = temperature.split("...")
                temperature = max(temperature[0], temperature[1])
                city_weather_info[0]["temperature"] = temperature
            elif index == 1:
                wind = info.find("div", class_="infoCol right").text.strip()
                wind = wind.replace(" ", "")
                wind = wind.replace("\n", "")
                wind = wind.replace("m/s", "")
                wind = wind.split("...")
                wind = max(wind[0], wind[1])
                city_weather_info[0]["wind"] = wind
            elif index == 2:
                precipitation = info.find("div", class_="infoCol right").text.strip()
                precipitation = precipitation.replace(" ", "")
                precipitation = precipitation.replace("\n", "")
                precipitation = precipitation.replace("mm", "")
                precipitation = precipitation.split("...")
                precipitation = max(precipitation[0], precipitation[1])
                city_weather_info[0]["precipitation"] = precipitation
        if today_only is False:
            # Next '5' days weather information (without today)
            block = soup.find("div", class_="weatherByDays-segment")
            block = block.find("div", class_="group-a")
            blocks = block.find_all("div", class_="cell")
            for index, info in enumerate(blocks):
                if index == 0:
                    temperature = info.find("span", class_="maxTemp").text.strip()
                    temperature = temperature.replace("°", "")
                    temperature = temperature.replace("+", "")
                    temperature = temperature.replace(" ", "")
                    wind = info.find("div", class_="wind").text.strip()
                    wind = wind.replace("m/s", "")
                    wind = wind.replace(" ", "")
                    precipitation = info.find("div", class_="precipitation").text.strip()
                    precipitation = precipitation.replace(" ", "")
                    precipitation = precipitation.replace("mm", "")
                    date_for = date.today() + timedelta(days=+1)
                    date_for = date_for.strftime("%Y-%m-%d")
                    city_weather_info[1] = {}
                    city_weather_info[1]["city"] = city_name
                    city_weather_info[1]["date_current"] = date_today
                    city_weather_info[1]["date_for"] = date_for
                    city_weather_info[1]["temperature"] = temperature
                    city_weather_info[1]["wind"] = wind
                    city_weather_info[1]["precipitation"] = precipitation
                if index == 1:
                    temperature = info.find("span", class_="maxTemp").text.strip()
                    temperature = temperature.replace("°", "")
                    temperature = temperature.replace("+", "")
                    temperature = temperature.replace(" ", "")
                    wind = info.find("div", class_="wind").text.strip()
                    wind = wind.replace("m/s", "")
                    wind = wind.replace(" ", "")
                    precipitation = info.find("div", class_="precipitation").text.strip()
                    precipitation = precipitation.replace(" ", "")
                    precipitation = precipitation.replace("mm", "")
                    date_for = date.today() + timedelta(days=+2)
                    date_for = date_for.strftime("%Y-%m-%d")
                    city_weather_info[2] = {}
                    city_weather_info[2]["city"] = city_name
                    city_weather_info[2]["date_current"] = date_today
                    city_weather_info[2]["date_for"] = date_for
                    city_weather_info[2]["temperature"] = temperature
                    city_weather_info[2]["wind"] = wind
                    city_weather_info[2]["precipitation"] = precipitation
                if index == 2:
                    temperature = info.find("span", class_="maxTemp").text.strip()
                    temperature = temperature.replace("°", "")
                    temperature = temperature.replace("+", "")
                    temperature = temperature.replace(" ", "")
                    wind = info.find("div", class_="wind").text.strip()
                    wind = wind.replace("m/s", "")
                    wind = wind.replace(" ", "")
                    precipitation = info.find("div", class_="precipitation").text.strip()
                    precipitation = precipitation.replace(" ", "")
                    precipitation = precipitation.replace("mm", "")
                    date_for = date.today() + timedelta(days=+3)
                    date_for = date_for.strftime("%Y-%m-%d")
                    city_weather_info[3] = {}
                    city_weather_info[3]["city"] = city_name
                    city_weather_info[3]["date_current"] = date_today
                    city_weather_info[3]["date_for"] = date_for
                    city_weather_info[3]["temperature"] = temperature
                    city_weather_info[3]["wind"] = wind
                    city_weather_info[3]["precipitation"] = precipitation
                if index == 3:
                    temperature = info.find("span", class_="maxTemp").text.strip()
                    temperature = temperature.replace("°", "")
                    temperature = temperature.replace("+", "")
                    temperature = temperature.replace(" ", "")
                    wind = info.find("div", class_="wind").text.strip()
                    wind = wind.replace("m/s", "")
                    wind = wind.replace(" ", "")
                    precipitation = info.find("div", class_="precipitation").text.strip()
                    precipitation = precipitation.replace(" ", "")
                    precipitation = precipitation.replace("mm", "")
                    date_for = date.today() + timedelta(days=+4)
                    date_for = date_for.strftime("%Y-%m-%d")
                    city_weather_info[4] = {}
                    city_weather_info[4]["city"] = city_name
                    city_weather_info[4]["date_current"] = date_today
                    city_weather_info[4]["date_for"] = date_for
                    city_weather_info[4]["temperature"] = temperature
                    city_weather_info[4]["wind"] = wind
                    city_weather_info[4]["precipitation"] = precipitation
                if index == 4:
                    temperature = info.find("span", class_="maxTemp").text.strip()
                    temperature = temperature.replace("°", "")
                    temperature = temperature.replace("+", "")
                    temperature = temperature.replace(" ", "")
                    wind = info.find("div", class_="wind").text.strip()
                    wind = wind.replace("m/s", "")
                    wind = wind.replace(" ", "")
                    precipitation = info.find("div", class_="precipitation").text.strip()
                    precipitation = precipitation.replace(" ", "")
                    precipitation = precipitation.replace("mm", "")
                    date_for = date.today() + timedelta(days=+5)
                    date_for = date_for.strftime("%Y-%m-%d")
                    city_weather_info[5] = {}
                    city_weather_info[5]["city"] = city_name
                    city_weather_info[5]["date_current"] = date_today
                    city_weather_info[5]["date_for"] = date_for
                    city_weather_info[5]["temperature"] = temperature
                    city_weather_info[5]["wind"] = wind
                    city_weather_info[5]["precipitation"] = precipitation
        return city_weather_info


def city_to_link(city_name: str):
    if type(city_name) is str:
        lith_to_eng = {"ą": "a", "č": "c", "ę": "e", "ė": "e", "š": "s", "ū": "u", "ų": "u", "ž": "z"}
        changed = city_name.lower()
        for old_letter, new_letter in lith_to_eng.items():
            changed = changed.replace(old_letter, new_letter)
        return changed
