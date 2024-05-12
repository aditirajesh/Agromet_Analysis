import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from geopy.geocoders import Nominatim
import requests

def gen_data_model(plant):
    df = pd.read_csv(r'Crop_recommendation.csv')
    df = df[df.label==plant]
    y = df['rainfall']
    x = df.drop(['rainfall','label','N','P','K','ph'], axis=1)
    return ml_model(x,y)


def ml_model(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)


    lr = LinearRegression()
    lr.fit(X, y)

    return lr


def get_latitude_longitude(location):
    geolocator = Nominatim(user_agent="try")
    location = geolocator.geocode(location)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None
    
def get_weather(location):
    lat , lon = get_latitude_longitude(location)
    api_key = "b136d8eadf0b12d2552205a829726b32"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
   
    
    response = requests.get(url).json()

    dates = []
    temperatures = []
    feels_like = []
    temp_min = []
    temp_max = []
    pressure = []
    humidity = []
    weather_conditions = []
    cloud_coverage = []
    wind_speed = []
    wind_direction = []
    visibility = []

# Extract relevant data from the response and store it in the lists
    for data_point in response['list']:
        dates.append(pd.to_datetime(data_point['dt'], unit='s'))
        temperatures.append(data_point['main']['temp']-273)
        feels_like.append(data_point['main']['feels_like']-273)
        temp_min.append(data_point['main']['temp_min']-273)
        temp_max.append(data_point['main']['temp_max']-273)
        pressure.append(data_point['main']['pressure'])
        humidity.append(data_point['main']['humidity'])
        weather_conditions.append(data_point['weather'][0]['main'])
        cloud_coverage.append(data_point['clouds']['all'])
        wind_speed.append(data_point['wind']['speed'])
        wind_direction.append(data_point['wind']['deg'])
        visibility.append(data_point['visibility'])

# Create a pandas DataFrame using the lists
    weather_df = pd.DataFrame({
        'Date': dates,
        'temperature': temperatures,
        'Feels Like (C)': feels_like,
        'Min Temperature (C)': temp_min,
        'Max Temperature (C)': temp_max,
        'Pressure (hPa)': pressure,
        'humidity': humidity,
        'Weather Conditions': weather_conditions,
        'Cloud Coverage (%)': cloud_coverage,
        'Wind Speed (m/s)': wind_speed,
        'Wind Direction (degrees)': wind_direction,
        'Visibility (meters)': visibility})
    weather_df.set_index('Date', inplace=True)
    return weather_df.iloc[:,[True,False,False,False,False,True,False,False,False,False,False]]
def get_water_per_day(loc,crop):
    l = get_weather(loc)
    dm = gen_data_model(crop)
    return (sum(dm.predict(l))/len(l))/14

def function(crop,location):
    lat,long = get_latitude_longitude(location)
    api_key = 'P2KDEF4ES4JTMC67572CFVF9U'
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{long}?key={api_key}'
    #dic = {'rice':30}
    response = requests.get(url).json()
    df = pd.DataFrame(response['days'])
    rain = df['precip'][0]*25.4
    reqd = get_water_per_day(location,crop)
    return (reqd-rain)




