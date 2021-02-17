import sys
import urllib.request
import urllib.parse
from playsound import playsound
import time
from datetime import datetime
import json

def get_ip():
    try:
        f = urllib.request.urlopen('https://api.ipify.org/',timeout=10)
        ip = f.read()
        return ip.decode('utf-8')
    except:
        return False


def write_log(time_, message):
    time_str= time_.strftime("%Y-%m-%d %H:%M:%S")
    ip = get_ip()
    if ip:
        complete_message = f"{time_str}: {message} ({ip})"
    else:
        complete_message = f"{time_str}: {message} (connection problem)"
    print(complete_message)
    with open("log.txt","a",encoding="utf-8") as archivo:
        archivo.write(complete_message + "\n")


def load_dict(filepath,encoding="utf-8"):
    with open(filepath,"r",encoding=encoding) as archivo:
        dictionary = json.load(archivo)
    return dictionary


currently_active = False
wait_good = 15
wait_bad = 10

urls = load_dict("urls.json")
name = "author"
url = urls[name]

while True:
    
    now = datetime.now()
    try:
        f = urllib.request.urlopen(url, timeout=60)
        code = f.getcode()
        if code == 200:
            if currently_active:
                write_log(now, f"{name} SERVER OK")
                playsound('normal_notification.mp3')
                time.sleep(wait_good*60)
            else:
                write_log(now, f"{name} SERVER REACTIVATED")
                playsound('attention_notification.mp3')
                input("Revisar y reactivar descarga. Enter para continuar:")#Reactivar
                currently_active = True
        else:
            if currently_active:
                write_log(now, f"{name} SERVER RECENTLY DOWN: code {code}")
                playsound('attention_notification.mp3')
                input("Revisar y parar descarga. Enter para continuar:")#Parar descarga
                currently_active = False
            else:
                write_log(now, f"{name} SERVER STILL DOWN: code {code}")
                playsound('normal_down_notification.mp3')
                time.sleep(wait_bad*60)
    except:
        error = sys.exc_info()[0].__name__
        if currently_active:
            write_log(now, f"{name} SERVER RECENTLY DOWN: {error}")
            playsound('attention_notification.mp3')
            input("Revisar y parar descarga. Enter para continuar:")#Parar descarga
            currently_active = False
        else:
            write_log(now, f"ECTM SERVER STILL DOWN: {error}")
            playsound('normal_down_notification.mp3')
            time.sleep(wait_bad*60)
