# Weather app

### 1.Summary
Simple application to cheek weather forecast for today and next 5 days using coordinates or your current location.
App uses following APIs:
1. https://api.ipify.org and https://geo.ipify.org to determine location.
2. https://api.openweathermap.org to get forecast
## 2.Instalation
#### Requierments:
-Python version 3.11 or higher
#### Manual instalation:

1. Create directory for the application
2. Copy all files from the repository to directory You created
#### Instalation with Git:
In command line execute :
>git clone https://github.com/Michzlor/WeatherApp.git

It will create a directory named WeatherApp in your active directory(default: C/Users/username)

## 3.Start-up

1. Creating virtual environment
In command line execute
>  python -m venv env
2. Activating virtual environment
>  env/Scripts/activate
3. Instalation of packets and libraries used by app
> pip install -r requirements.txt
4. Run the main.py file
> Python main.py
or
> Python3 main.py