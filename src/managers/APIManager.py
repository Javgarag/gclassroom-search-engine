import os, sys
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

CLIENT_FILE = "client_file.json"
SCOPES = [
"https://www.googleapis.com/auth/classroom.announcements",
"https://www.googleapis.com/auth/classroom.courses",
"https://www.googleapis.com/auth/drive.file",
"https://www.googleapis.com/auth/classroom.rosters.readonly",
"https://www.googleapis.com/auth/classroom.profile.emails"]

def init():
    global classroom_service, drive_service, course_id, creds
    creds = get_credentials()

    classroom_service = build("classroom", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    course_id = config.get("base", "course_id")

    debug_print_classes()

def get_credentials():
    if not os.path.exists("api/token.json"):
        print("Authorize the script using the following link:")
        flow = InstalledAppFlow.from_client_secrets_file("api/" + CLIENT_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
  
    creds = Credentials.from_authorized_user_file("api/token.json", SCOPES) if "creds" not in locals() else creds
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

    with open("api/token.json", "w") as token:
        token.write(creds.to_json())
    
    return creds


def debug_print_classes():
    courses = classroom_service.courses().list(teacherId="me").execute().get("courses", [])
    for course in courses:
      print('Owned class "' + course["name"] + '" has the ID of "' + course["id"] + '"')

def upload(location, name, extension, mimetype):
    """Upload the specified file to GDrive. The file will be deleted from the system on completion, beware!"""
        
    file_metadata = {"name": name + "." + extension, "parents": config.get("base", "drive_folder")}
    upload = MediaFileUpload(location, mimetype = mimetype, resumable = True)
    file = drive_service.files().create(body = file_metadata, media_body = upload, fields = "id").execute()
    print("File '" + name + "' with id '" + file["id"] + "' has been uploaded to Google Drive.")

    if not os.name == "nt":
        os.remove(location)

    return file

def destroy_course():
    classroom_service.courses().update(id = course_id, body={
        "courseState" : "ARCHIVED",
        "name" : classroom_service.courses().get(id = course_id).execute()["name"]
    }).execute()
    classroom_service.courses().delete(id = course_id).execute()

    print("Deleted course, terminating script.")
    sys.exit()

def send_announcement(message, file=None, file_name=None, extension=None):
    classroom_service.courses().announcements().create(body = {
        "text": message,
        "materials" : [{
            "driveFile": {
                "driveFile": {
                    "id": file.get("id"),
                    "title": file_name + "." + extension
                }
            }
        }],
    }, courseId = course_id).execute()

def send_announcement_simple(message):
    classroom_service.courses().announcements().create(body = {
        "text": message
    }, courseId = course_id).execute()

def get_announcement_list():
    return classroom_service.courses().announcements().list(courseId = course_id, pageSize = 1).execute()
