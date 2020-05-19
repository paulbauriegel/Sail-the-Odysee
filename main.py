import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText
import threading
from threading import Thread
import datetime
import platform

toast_caption = "New Quest Slots available"
if platform.system() == 'Windows':
    from win10toast import ToastNotifier
elif platform.system() == 'Linux':
    from gi.repository import Notify
    Notify.init(toast_caption)

url = "https://odyssey.wildcodeschool.com/users/login?locale=en"
toaster = ToastNotifier()

password = input("Enter your Password: ")
def get_stuff():
    login_get = requests.request("GET", url)
    login_source = BeautifulSoup(login_get.text.encode('utf8'), 'html.parser')
    authenticity_token = login_source.select_one("#new_user input[name=authenticity_token]").get("value") #authenticity_token

    payload = {'utf8': 'true',
    'authenticity_token': authenticity_token,
    'commit': 'Sign in',
    'user[email]': 'paul.bauriegel@web.de',
    'user[password]': password,
    'user[remember_me]': '0'}
    login_post = requests.request("POST", url, data = payload, cookies=login_get.cookies, allow_redirects=True)
    odyssey_source = BeautifulSoup(login_post.text.encode('utf8'), 'html.parser')

    quest_string = odyssey_source\
        .select_one("div.current_quests h2")\
        .text\
        .split()[0]

    print(str(datetime.datetime.now()) + ": " + quest_string)

    if int(quest_string)<5:
        message = "You have {} free quest slot".format(5-int(quest_string))
        if platform.system() == 'Windows':
            toaster.show_toast(toast_caption,
                message,
                icon_path=None,
                duration=10)
        elif platform.system() == 'Linux':
            Notify.Notification.new(toast_caption, 
                message, 
                "dialog-information").show()
get_stuff()

from threading import Event, Thread

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func()
    Thread(target=loop).start()    
    return stopped.set

cancel_future_calls = call_repeatedly(300, get_stuff, [None])