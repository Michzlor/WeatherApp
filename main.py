import tkinter as tk
import json
import requests
import urllib.request
from datetime import datetime
from PIL import Image, ImageTk


def click_location():
    ip_address = requests.get('https://api.ipify.org').content.decode('utf8')

    response = requests.get(URL_geo.format(ip=ip_address))
    result = json.loads(response.text)
    lat = result['location']['lat']
    lon = result['location']['lng']
    print(f"lat: {lat}, lon: {lon}")
    get_weather(lat=lat, lon=lon)
    get_forecast(lat=lat, lon=lon)


def click_coordinates():
    get_weather(lat=entry_lat.get(), lon=entry_lon.get())
    get_forecast(lat=entry_lat.get(), lon=entry_lon.get())


def get_weather(lat, lon):
    req = requests.get(url=URL_today.format(lat=lat, lon=lon, api=api_key))
    content = json.loads(req.text)
    output = (
        f"Weather summary for today: {content['weather'][0]['description']}\n"
        f"Temperature: {content['main']['temp']}°C\n"
        f"Atmospheric pressure: {content['main']['pressure']}hPa\n"
        f"Humidity: {content['main']['humidity']}%\n"
        f"Wind speed: {content['wind']['speed']}m/s up to {content['wind']['gust']}m/s\n")

    urllib.request.urlretrieve(icon_url.format(code=content['weather'][0]['icon']), 'img.png')
    ico = ImageTk.PhotoImage(Image.open('img.png'))
    label_txt = tk.Label(master=frm_result, text=output, borderwidth=3, bg='#fffafa')
    label_ico = tk.Label(master=frm_result, image=ico, borderwidth=3, bg='#fffafa')
    label_ico.image = ico
    label_txt.grid(row=0, column=0)
    label_ico.grid(row=0, column=1)


def get_forecast(lat, lon):
    dates = []
    icons = []
    req = requests.get(url=URL_forecast.format(lat=lat, lon=lon, api=api_key))
    content = json.loads(req.text)
    for forecast in content['list']:
        if datetime.strptime(forecast['dt_txt'].split(sep=" ")[0], date_format) not in dates \
                and forecast['dt_txt'].split(sep=" ")[1] == '12:00:00':
            urllib.request.urlretrieve(icon_url.format(code=forecast['weather'][0]['icon']), 'img.png')
            icons.append(Image.open('img.png'))

            output.append(
                f"Weather summary for {forecast['dt_txt'].split(sep=' ')[0]}: {forecast['weather'][0]['description']}\n"
                f"Temperature: {forecast['main']['temp']}°C\n"
                f"Atmospheric pressure: {forecast['main']['pressure']}hPa\n"
                f"Humidity: {forecast['main']['humidity']}%\n"
                f"Wind speed: {forecast['wind']['speed']}m/s up to {forecast['wind']['gust']}m/s\n")

            dates.append(datetime.strptime(forecast['dt_txt'].split(sep=" ")[0], date_format))
        else:
            continue
    for idx, day in enumerate(output):
        print(day)

        label_txt = tk.Label(master=frm_result, text=day, borderwidth=3, bg='#fffafa')
        ico = ImageTk.PhotoImage(icons[idx])
        label_ico = tk.Label(master=frm_result, image=ico, borderwidth=3, bg='#fffafa')
        label_ico.image = ico
        label_txt.grid(row=idx + 1, column=0)
        label_ico.grid(row=idx + 1, column=1)


URL_today = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric'
URL_forecast = 'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api}&units=metric'

# https://geo.ipify.org/api/v2/country,city?apiKey=at_IZGI1P62xIOc5TfTlVcG1oVD16dDB&ipAddress=8.8.8.8

URL_geo = "https://geo.ipify.org/api/v2/country,city?apiKey=at_IZGI1P62xIOc5TfTlVcG1oVD16dDB&ipAddress={ip}"
api_key = '9b7c27108e50e497c9187a08e55d8333'
date_format = '%Y-%m-%d'
urllib.request.urlretrieve('https://openweathermap.org/img/wn/10d@2x.png', '123.png')
img = Image.open('123.png')
icon_url = "https://openweathermap.org/img/wn/{code}@2x.png"
output = []

window = tk.Tk()
window['background'] = '#fffafa'
window.columnconfigure('all', minsize=15)
window.rowconfigure("all", minsize=50)

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3, bg='#fffafa')
frm_form.pack(fill=tk.X)

button_location = tk.Button(master=frm_form, text="Use your location", width=30, height=2, command=click_location,
                            bg='#fffafa')
button_submit = tk.Button(master=frm_form, text="Submit coordinates", width=30, height=2, command=click_coordinates,
                          bg='#fffafa')
label_lat = tk.Label(master=frm_form, text="Latitude:", bg='#fffafa', borderwidth=3)
entry_lat = tk.Entry(master=frm_form, borderwidth=1)
label_lon = tk.Label(master=frm_form, text="Longitude:", bg='#fffafa', borderwidth=3)
entry_lon = tk.Entry(master=frm_form, borderwidth=1)
button_location.grid(row=0, column=0)
button_submit.grid(row=0, column=1)
label_lat.grid(row=1, column=0, sticky="e")
entry_lat.grid(row=1, column=1, sticky='w')
label_lon.grid(row=2, column=0, sticky="e")
entry_lon.grid(row=2, column=1, sticky='w')

frm_result = tk.Frame(borderwidth=3, bg='#fffafa')
frm_result.pack()

window.mainloop()
