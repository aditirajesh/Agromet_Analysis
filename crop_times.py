from datetime import datetime,date
from datetime import timedelta
import pandas as pd
import requests
from geopy.geocoders import Nominatim
from ml import get_water_per_day
from meteostat import Point, Daily

def time_to_harvest(dos,crop):
    dictionary = {
    'rice': [113,125],
    'maize':[100,120],
    'lentil':[105,115],
    'coffee':[1000,1010],
    'jute':[125,140],
    'coconut':[360,370],
    'chickpea':[85,100],
    'cotton':[200-220]}
    dos_date = datetime.strptime(dos,'%d-%m-%Y')
    a = dictionary[crop]
    harvest__1 = dos_date+timedelta(days = a[0] )
    harvest__2 = dos_date+timedelta(days = a[1])
    return harvest__1.strftime('%d-%m-%Y'),harvest__2.strftime('%d-%m-%Y')


def gdd(dos,crop,loc):
    crop_phases = pd.read_csv('crop_details.csv')
    crop_phases = crop_phases[crop_phases['crop']==crop]
    dos_date = datetime.strptime(dos,'%d-%m-%Y')
    #print(crop_phases)
    gdd_data = get(dos,loc)[::-1]
    result=[]
    for idx, value in gdd_data.items():
    # Iterate over the DataFrame rows to compare with the value
        for row in crop_phases.itertuples():
            if value < row.GDD:
                result.append((idx, row.phase))
                break
            elif value>crop_phases['GDD'].iloc[-1] and idx<datetime.strptime(time_to_harvest(dos,crop)[0],'%d-%m-%Y'):
                result.append((idx,'ripening'))    
    return pd.DataFrame(result[::-1])

def get_latitude_longitude(location):
    geolocator = Nominatim(user_agent="try")
    location = geolocator.geocode(location)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None

def function(crop,location):
    lat,long = get_latitude_longitude(location)
    api_key = 'P2KDEF4ES4JTMC67572CFVF9U'
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{long}?key={api_key}'
    response = requests.get(url).json()
    df = pd.DataFrame(response['days'])
    rain = df['precip'][0]*25.4
    reqd = get_water_per_day(location,crop)
    return reqd-rain,((reqd-rain)/reqd)*100
#print(function('lentil','cherrapunjee'))
def function2(location):
    lat,long = get_latitude_longitude(location)
    api_key = 'P2KDEF4ES4JTMC67572CFVF9U'
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{long}?key={api_key}'
    response = requests.get(url).json()
    df = pd.DataFrame(response['days'])
    raindf = df['precip']*25.4
    return list(raindf)[:3]

def get(dos,loc):

    lat,lon = get_latitude_longitude(loc)
    start = datetime.strptime(dos,'%d-%m-%Y')
    end = datetime.now()

# Create Point for Vancouver, BC
    vancouver = Point(lat, lon)

# Get daily data for 2018
    data = Daily(vancouver, start, end)
    data = data.fetch()['tavg']
    data = (9/5)*data+32
    data = data-50
    data = data.astype(int)
    data = data.cumsum()
    return data
    #data_first = data.groupby(1).first()
    #data_first = data_first.sort_values(by=0)
    #return data_first
#print(get('16-07-2023','delhi'))

if __name__ =='__main__':
    print(function2('chennai'))


    print(time_to_harvest('15-04-2023','maize'))
    data = gdd('15-07-2023','maize','shimla')


    data_first = data.groupby(1).first()
    data_first = data_first.sort_values(by=0)
    print(data)
    print(data_first)
def crops_density(crop,size):
    crop_dict = {'rice':392000,'lentil':43500,'maize':77400,'coconut':70,'chickpea':392000,'cotton':14500,'jute':77500,'coffee':174000}
    return crop_dict[crop]*size

def irrigation_notification(crop,location,size):
    irrigate,percentage = function(crop,location)
    if -30<percentage<10:
        return f"{date.today()}:","IRRIGATION NOT REQUIRED DUE TO SUFFICIENT RAIN "
    elif 10<percentage:
        return f"{date.today()}:",f"WATER {irrigate} mm per crop",f" TOTAL WATER FOR FIELD REQUIRED : {int(crops_density(crop,size)*irrigate/1000)} litres"
    elif percentage<-30:
        return f'EXCESSIVE RAIN EXPECTED WHICH MAY CAUSE FLOODING','Kindly be ready with runoff stream.'
