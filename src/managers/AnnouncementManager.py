import datetime
from configparser import ConfigParser
from managers import CommandManager, APIManager

config = ConfigParser()
config.read("config.ini")

def init():
    send_announcement(open("messages/init.txt", encoding = "utf8").read())

def send_announcement(message, file=None, file_name=None, extension=None):
    if not file or not extension or not file_name:
        APIManager.send_announcement_simple(message)
    else:
        APIManager.send_announcement(message, file, file_name, extension)
    print("Sent announcement at " + str(datetime.datetime.now()) + ".")

def update(last_processed_announcement = ""):
    announcement_list = APIManager.get_announcement_list()
    for announcement in announcement_list.get("announcements", []):
        if announcement["text"] != last_processed_announcement:
            CommandManager.exec(announcement["text"])
        
        return announcement["text"]
