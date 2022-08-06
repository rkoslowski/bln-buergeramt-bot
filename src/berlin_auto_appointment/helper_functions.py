import time
import bs4
import requests
from urllib import request
from requests.exceptions import HTTPError
import webbrowser as wb
import random

def check_url(url):
    #for url in ['https://api.github.com', 'https://api.github.com/invalid']:
        try:
            response = requests.get(url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

def randomize_time():
    return random.randint(90, 120)

def get_available_appointment_links_this_month(response):
    body = bs4.BeautifulSoup(response.content, features="html.parser")
    links = body.select('.calendar-month-table')[0].select('td.buchbar a')
    print('found:', len(links), 'this month')
    if links:
        for link in links[:10]:
            if 'href' in link.attrs:
                day = int(link.text.strip()) 
                found = True
                print('{}: http://service.berlin.de{} '.format(day, link.attrs['href']))
                ext_link = "http://service.berlin.de" + link.attrs['href']
                print(ext_link)
                if found:
                    open_in_browser(ext_link)
                    exit()

def get_available_appointment_links_next_month(response):
    body = bs4.BeautifulSoup(response.content, features="html.parser")
    links = body.select('.calendar-month-table')[1].select('td.buchbar a')
    print('found:', len(links), 'next month')
    if links:
        for link in links[:10]:
            day = int(link.text.strip())
            found = True
            #print('{}: http://service.berlin.de{} '.format(day, link.attrs['href']))
            ext_link = "http://service.berlin.de" + link.attrs['href']
            print(ext_link)
            if found:
                open_in_browser(ext_link)
                exit()


# opens the target link in the browser
def open_in_browser(link):
    wb.open_new_tab(link)

# defines the type of service to check for available appointments
# the booleans are to be set as the only input parameter
# i really didnt want to make an gui...
def get_servic_type():
    anmeldung_einer_wohnung     = False
    personal_id_beantragen      = True
    reisepass_beantragen        = False
    if(anmeldung_einer_wohnung):
        return 'https://service.berlin.de/dienstleistung/120686/'
    elif (personal_id_beantragen):
        return 'https://service.berlin.de/dienstleistung/120703/'
    else:
        return 'https://service.berlin.de/dienstleistung/121151/'

def get_appointment_link():
    servicelink = get_servic_type()

    try:
        response = requests.get(servicelink)
        response.raise_for_status()
    except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
    else:
            print('Connection successfull!')

    body = bs4.BeautifulSoup(response.content, 'html.parser')

    if(body.find('div', class_='zmstermin-multi inner')):

        bodyclass = body.find('a', class_='btn')
        link = bodyclass.attrs['href']
        return link
    else:
        print('required element not found')
        exit()

# wait a random time between 90 to 120 sec to prevent the webserver to refuse connection (for ddos)
def sleep_til_next_request():
    time.sleep(randomize_time())


def get_response(url):
    return requests.get(url)

def try_get_app(urlbody):
    get_available_appointment_links_this_month(urlbody)
    get_available_appointment_links_next_month(urlbody)