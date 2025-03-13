import modules.utilities as utilities
from contextlib import contextmanager
import subprocess
import sys, os
import youtube_dl
import time
from pynotifier import Notification
import os
import shutil

def main():
    utilities.clear()
    url = input(" [?] Video URL: ")

    print(" [+] Downloading stand by\n")

    
    ydl = youtube_dl.YoutubeDL({'outtmpl': 'Video Downloads/%(uploader)s - %(title)s - %(id)s.%(ext)s'}) # If anyone knows how to mute the output of this send help :,)

    with ydl:
        result = ydl.extract_info(
            url,
            download = True
        )

    Notification(
    	title='Download Complete',
    	description='Finished downloading video',
    	duration=5,
    	urgency='normal'
    ).send()

    print(f"\n [!] Finished downloading '{result['title']}'")
    inp = input(" [?] Do you want to keep the video? (Y/n) ")

    if "y" in inp.lower() or inp == "":
        utilities.display_categories() # Show the avaliable categories to the user

        while True:
            category = input("\n [?] Category: ")

            if not os.path.exists(f"Videos/{category}"):
                inp = input(f" [?] Are you sure you want to create a new category named '{category}'? (Y/n) ")
                if "y" in inp.lower() or inp == "":
                    os.mkdir(f"Videos/{category}")
                    break

            else:
                break

        shutil.move(
            f"Video Downloads/{result['uploader']} - {result['title']} - {result['id']}.mp4",
            f"Videos/{category}/{result['uploader']} - {result['title']} - {result['id']}.mp4"
        )

    else:
        os.remove(f"Video Downloads/{result['uploader']} - {result['title']} - {result['id']}.mp4")
