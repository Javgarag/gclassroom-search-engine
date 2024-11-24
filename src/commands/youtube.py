import os
from pytubefix import YouTube
from managers import AnnouncementManager, APIManager, ScrapeManager
from commands import format_google_redirect

async def youtube(a):
    if "https://www.google.com/url?esrc=s&q=&rct=j&sa=U&url=" in a[0]:
        a[0] = await format_google_redirect(a[0])

    try: # Videos may be restricted or unobtainable
        video = YouTube(a[0])
        title = await ScrapeManager.format_file_name(video.title)
        hq_stream = video.streams
        if hq_stream.get_by_resolution("720p") != None:
            filter_mp4 = hq_stream.get_by_itag(22)
        else:
            filter_mp4 = hq_stream.filter(file_extension = "mp4", res=hq_stream.get_highest_resolution()).first()

        if not os.path.exists(".temp"):
            os.mkdir(".temp")
        
        filter_mp4.download(output_path=".temp", filename=title)

        file = APIManager.upload(".temp/" + title + ".mp4", title, "mp4", "video/mp4")
        AnnouncementManager.send_announcement(title, file, title, "mp4")

    except Exception as e:
        AnnouncementManager.send_announcement("ERROR: " + str(e))

yt = youtube
