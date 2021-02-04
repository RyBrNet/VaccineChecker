import time

from bs4 import BeautifulSoup
import requests
import ezgmail
from playsound import playsound

import secrets  # from secrets.py in this folder
def get_page_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content


def check_appt_available(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    appt_available = 0
    locations_checked = 0
    while True:
        locations_checked = locations_checked + 1
        try:
            appt_location = int(soup.select("body > div.main-container > div.mt-24.pt-4.border-t.border-gray-200 > div:nth-child(" + str(locations_checked) + ") > div > div > h4")[0].contents[0][0:4])
            print("Appt_Location is 1500: " + str(appt_location == 1500))
            if (appt_location == 1500): 
                appt_available = int(soup.select("body > div.main-container > div.mt-24.pt-4.border-t.border-gray-200 > div:nth-child(" + str(locations_checked) + ") > div > div > p:nth-child(8)")[0].contents[1])
                print("Appt Available: " + str(appt_available != 0))
                if appt_available != 0:
                    return True
        except:
            print("Locations Checked: " + str(locations_checked))
            break
    
    return False
# TODO Need to check all appointment sites - div:nth-child(#)


# body > div.main-container > div.mt-24.pt-4.border-t.border-gray-200 > div:nth-child(1) > div > div > h4

def send_notification():
    ezgmail.send('rybrnet@gmail.com', 'Appointment Available!', 'Put info here')
    while True:
        playsound('alarm.wav')

def check_inventory():
    url = "https://prepmod.doh.wa.gov/clinic/search"
    page_html = get_page_html(url)
    
    if check_appt_available(page_html):
        send_notification()
    else:
        print("No appointments")

while True:
    check_inventory()
    time.sleep(1800)  # Wait an half hour and try again