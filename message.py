from twilio.rest import Client
import schedule
import requests
from crop_times import irrigation_notification
#import keys

def send_message(body,num):
    client = Client('AC005fc729911624de12078a7cfdd0ac69','63d52bc79de342d2b42a55b3acf69e10')
    message = client.messages.create(
        to="+918220431150",body=body,from_ = '+13345084262'
    )
if __name__=="__main__":
    send_message(irrigation_notification('rice','chennai',3),"74981279")
