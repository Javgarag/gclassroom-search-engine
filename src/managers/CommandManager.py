import asyncio
from managers import AnnouncementManager
from commands import *

def get_arguments(command, splits):
    return command.split(None, splits)[1:]

def exec(command):
    command_root = command.split()[0].lower()
    command_func = globals().get(command_root)
    if not command_func:
        print("No command called '" + command_root + "'")
        return

    print("\nExecuting command: " + command_root)
    if not asyncio.iscoroutinefunction(command_func):
        try:
            command_func(get_arguments(command, command_func.__annotations__.get("a", 1)))
        except (TypeError, Exception) as e:
            AnnouncementManager.send_announcement("ERROR: " + str(e))
    else:
        try:
            asyncio.get_event_loop().run_until_complete(command_func(get_arguments(command, command_func.__annotations__.get("a", 1))))
        except (TypeError, Exception) as e:
            AnnouncementManager.send_announcement("ERROR: " + str(e))

