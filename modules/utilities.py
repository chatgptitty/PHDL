import os
import subprocess
import sys

def display_categories(aditionalInfo = True): # Displays the categories
    if aditionalInfo: # Usefull in the categorie editor where we dont need to additional information it pastes to the console
        print("\n [+] Current categories:\n")

    categories = [f" [-] {x[0][7:]}" for x in os.walk("Videos/")][1:]
    print("\n".join(categories))

    if aditionalInfo:
        print("\n [+] Type any of the above (case insentensive) or a new category and it will be created for you")

def install(package): # Used to install packages
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
