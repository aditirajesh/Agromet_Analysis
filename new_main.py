from crop_times import irrigation_notification,gdd
from fertilizer import fert_recommend,chemical_fertilizer
import requests
import pandas as pd
from geopy.geocoders import Nominatim
import markupsafe
from datetime import datetime,timedelta,date

class Customer:

    def __init__(self,fname,lname,mail,phno,passwd,location,soiln,soilp,soilk,crop,dos,size):
        self.fname = fname
        self.lname = lname
        self.mail = mail
        self.phno = phno
        self.passwd = passwd
        self.location = location
        self.n = soiln
        self.p = soilp
        self.k = soilk
        self.crop = crop
        self.dos = dos
        self.size = size

'''------------------------------CROP HISTORY--------------------'''

def crop_gdd_timeline(p:Customer):
    data = gdd(p.dos,p.crop,p.location)
    data_first = data.groupby(1).first()
    data_first = data_first.sort_values(by=0)
    dict__ = data_first.to_dict()[0]
    l = []
    for i in dict__:
        n = {}
        n['phase'] = i
        n['date'] = dict__[i].to_pydatetime().date()
        print(type(dict__[i]))
        l.append(n)
    return l

'''-----------------------------FERTILIZERS---------------------------'''

def fertilizer_practice(p:Customer):
    return markupsafe.Markup(fert_recommend(p.n,p.p,p.k,p.crop))

def chemical_fertilizer_soil(p:Customer):
    return chemical_fertilizer(p.n,p.p,p.k)

'''------------------------NOTIFICATIONS------------------------------'''

def main_notification_irrigation(p:Customer):
    return irrigation_notification(p.crop,p.location,p.size)

'''---------------------------WEATHER---------------------------------'''

def main_weather(p:Customer):
    def get_latitude_longitude(location):
        geolocator = Nominatim(user_agent="try")
        location = geolocator.geocode(location)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None
    lat,long = get_latitude_longitude(p.location) 

    api_key = 'P2KDEF4ES4JTMC67572CFVF9U'
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{long}?key={api_key}'
    response = requests.get(url).json()
    response = pd.DataFrame(response['days'])
    response['temp']=round((response['temp']-32)*5/9,2)
    response['feelslike']=round((response['feelslike']-32)*5/9,2)
    response['tempmin']=round((response['tempmin']-32)*5/9,2)
    response['tempmax']=round((response['tempmax']-32)*5/9,2)
    return (list(response[['temp','feelslike','tempmin','tempmax','pressure','windspeed','conditions','humidity']].iloc[1]))

'''---------------------------------------------------------------------------------------------------------'''
def harvesting(dos,crop):
    def time_to_harvest(dos,crop):
        dictionary = {
        'rice': [113,125],
        'maize':[100,120],
        'lentil':[105,115],
        'coffee':[1000,1010],
        'jute':[125,140],
        'coconut':[360,370],
        'chickpea':[85,100],
        'cotton':[200,220]}
        tod = date.today()
        l = dos.split('-')
        dos_dat = date(int(l[-1]),int(l[1]),int(l[0]))
        comp = tod - dos_dat
        comp = int(comp.days)
        dos_date = datetime.strptime(dos,'%d-%m-%Y')
        a = dictionary[crop]
        harvest__1 = dos_date+timedelta(days = a[0] )
        harvest__2 = dos_date+timedelta(days = a[1])
        perc1,perc2 = comp/a[0],comp/a[1]
        per = round((perc1+perc2/2)*100)
        return ((harvest__1.strftime('%d-%m-%Y'),harvest__2.strftime('%d-%m-%Y')),per)
    t,p = time_to_harvest(dos,crop)
    return f'{t[0]} to {t[1]}',p

if __name__=="__main__":
    cust = Customer('Test','Test','example@123','9090909','passwd','coimbatore',50,50,30,'lentil','18-08-2023',1)
    print(harvesting(cust))