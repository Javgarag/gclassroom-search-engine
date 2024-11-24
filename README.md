# Google Classroom Search Engine
A Python script that allows you to access webpages through Google Classroom's class message board.

## How does it work?
Based on a series of "commands", students can interact with the teacher, which will answer with whatever has been requested attached to the response. This allows, for example, to search Google, all without leaving Classroom. For documentation on all commands, see ![src/messages/help.txt](https://github.com/Javgarag/gclassroom-search-engine/blob/main/src/messages/help.txt).

![](https://raw.githubusercontent.com/Javgarag/gclassroom-search-engine/refs/heads/main/images/search.jpg)

*Note that, since webpages are attached as PDF files, they are non-interactable, though links on buttons can still be copied and retrieved with the 'get' command.*

## API setup
In order to interact with the Google API, you will need to create a Google Cloud project with access to the Google Classroom API and the Google Drive API. You will also need to create an OAuth client, download it, and name it `client_file.json` inside `src/api`. 

On your first run, the script will prompt you to authorize your project by opening up a browser window. You should choose your teacher account here. Afterwards, a new file will be created, `src/api/token.json`, and the script will return your owned classes along with their corresponding IDs. Here, choose which one you want to operate on and copy its ID to `src/config.ini`, then re-run the script. If an initialization message is sent on the board, it is ready for use.

In order not to clutter up your Google Drive, you should also provide a Drive folder where all the files should be saved to. You can obtain its ID by copying the URL's last path location of the Drive page corresponding to that folder.

## Why?
This project stems from a desire to help bypass MDM restrictions, such as those imposed by schools. As long as the student's education account is set to the 'teacher' role (which is a one-time button press on behalf of the student when they first open Classroom), *a.k.a* being able to create classes, this script will work for them. Of course, it's all for educational purposes... 😉
