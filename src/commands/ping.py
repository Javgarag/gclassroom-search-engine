from managers import AnnouncementManager
from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")

def ping(a):
    """Posts a simple announcement to the board to check if the script is alive."""
    AnnouncementManager.send_announcement("Pong!\nVersion: " + config.get("base", "version"))
