from managers import AnnouncementManager

def help(a):
    """Posts a help message to the announcement board."""
    AnnouncementManager.send_announcement(open("messages/help.txt", encoding = "utf8").read())