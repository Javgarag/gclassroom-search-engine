from configparser import ConfigParser
from managers import APIManager

config = ConfigParser()
config.read("config.ini")

def destroy(a): # Ends the script on execution, beware!
    if a[0] == config.get("base", "destruction_key"):
        APIManager.destroy_course()
