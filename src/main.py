# Imports
import time, os
from managers import AnnouncementManager, APIManager

def main():
    APIManager.init()
    AnnouncementManager.init()
    print("Successful initialization! Looping...")

    while True:
        time.sleep(5)
        last_processed_announcement = AnnouncementManager.update(last_processed_announcement if "last_processed_announcement" in locals() else None)

if __name__ == "__main__":
  main()
