import modules.utilities as utilities

import os
import shutil
import random

def shuffle(): # Shuffle all the files in the folder by adding 4 random numbers infront of the file name
    utilities.display_categories()
    category = input(' [?] Category: ')
    print("") # Add newline

    path = os.walk(f"Videos/{category}") # Get all the files in the folder
    for root, dirs, files in path:
        for i in files:
            shutil.move( # Rename the file
                f"Videos/{category}/{i}",
                f"Videos/{category}/{random.randint(1000, 9999)} # {i}"
            )
            print(f" [+] Videos/{category}/{random.randint(1000, 9999)} # {i}") # Print the result for debugging and updating the user on whats going on

def unshuffle(): # Used to unshuffle the whole list, will preserve file names of those who does not have the numbers in thir name
    utilities.display_categories()
    category = input(' [?] Category: ')
    print("")

    path = os.walk(f"Videos/{category}") # Get all the files in the path
    for root, dirs, files in path:
        for i in files:
            if "#" in i[:7]: # Check if the # is within the first 6 chareters of the filename
                shutil.move( # Rename the file
                    f"Videos/{category}/{i}",
                    f"Videos/{category}/{i[6:].strip()}"
                )
                print(f" [+] Videos/{category}/{i[7:]}")

def main():
    utilities.clear()

    print(" [1] Shuffle    [2] Unshuffle \n")

    inp = input(">>> ")

    if inp == "1":
        shuffle()
    elif inp == "2":
        unshuffle()
    else:
        print(" [!] Invalid option")
