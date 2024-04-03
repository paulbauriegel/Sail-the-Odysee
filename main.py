import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText
import threading
from threading import Thread
import datetime
import platform
import challenge_bot

# Init Toaster
toast_caption = "New Quest Slots available"
if platform.system() == 'Windows':
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
elif platform.system() == 'Linux':
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    Notify.init(toast_caption)

user_name = "<email>"
password = input("Enter your Password: ")

def get_quests(user_name, password):
    url = "https://odyssey.wildcodeschool.com/users/login?locale=en"
    login_get = requests.request("GET", url)
    login_source = BeautifulSoup(login_get.text.encode('utf8'), 'html.parser')
    authenticity_token = login_source.select_one("#new_user input[name=authenticity_token]").get("value") #authenticity_token

    payload = {'utf8': 'true',
    'authenticity_token': authenticity_token,
    'commit': 'Sign in',
    'user[email]': user_name,
    'user[password]': password,
    'user[remember_me]': '0'}
    login_post = requests.request("POST", url, data = payload, cookies=login_get.cookies, allow_redirects=True)
    odyssey_source = BeautifulSoup(login_post.text.encode('utf8'), 'html.parser')
    login_cookie = [cookie for cookie in login_get.cookies if cookie.name=="_odyssey_session"][0].value

    quest_string = odyssey_source\
        .select_one("div.current_quests h2")\
        .text\
        .split()[0]

    print("{}: {} Ongoing Quests".format(datetime.datetime.now(), quest_string))
    return login_cookie, int(quest_string)

def notify(message):
    if platform.system() == 'Windows':
        toaster.show_toast(toast_caption,
            message,
            icon_path=None,
            duration=10)
    elif platform.system() == 'Linux':
        Notify.Notification.new(toast_caption, 
            message, 
            "dialog-information").show()
def get_stuff():
    login_cookie, running_quests = get_quests(user_name, password)
    if running_quests<5:
        message = "You have {} free quest slot".format(5-running_quests)
        notify(message)
    challenges_validation = challenge_bot.get_challenges(user_name, password)
    message = "{} challenges require validation".format(len(challenges_validation))
    print(challenges_validation)
    notify(message)
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
