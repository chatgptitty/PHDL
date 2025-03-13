import modules.utilities as utilities

import os
import shutil

def add_cat(): # Add a category
    name = input("\n [?] Name: ")

    os.mkdir(f"Videos/{name}")

    print(f" [+] Created category '{name}'")

def del_cat(): # Delete a category
    name = input("\n [?] Category name: ")

    inp = input(f" [!] Are you sure you want to remove '{inp}', the files cannot be undone (Y/n) ")
    if "y" in inp.lower() or inp == "":
        os.rmdir(os.mkdir(f"Videos/{name}"))

        print(f" [!] Removed '{name}'")
    else:
        print(" [-] Canseled")

def mer_cat(): # Merge category, used to combine 2 categories into 1
    name1 = input("\n [?] Category name 1 (The one that will be copied from): ")
    name2 = input(" [?] Category name 2 (The one that will be copied to): ")

    print(" [+] Started processing, stand by\n")

    ka = False
    sa = False

    path = os.walk(f"Videos/{name1}") # Get all the files in the folder
    for root, dirs, files in path:
        for i in files:
            path1 = f"Videos/{name1}/{i}"
            path2 = f"Videos/{name2}/{i}"

            if ka or not os.path.isfile(path2): # ka = Keep Always (BOOL)
                shutil.copyfile(path1, path2)
            elif sa and os.path.isfile(path2): # sa = Skip Always (BOOl)
                continue
            elif os.path.isfile(path2):
                inp = input(f" [!] Conflict, {i} already exists at destination, (K- keep, S- Skip, KA- Keep Always, SA- Skip Always) ")

                if inp.lower() == "s":
                    continue
                elif inp.lower() == "k":
                    shutil.copyfile(path1, path2)
                elif inp.lower() == "ka":
                    ka = True
                elif inp.lower() == "sa":
                    sa = True

def ren_cat():
    name1 = input("\n [?] Name 1 (The one that will be renamed): ")
    name2 = input(" [?] Name 2 (What it will be renamed to): ")

    path1 = f"Videos/{name1}"
    path2 = f"Videos/{name2}"

    shutil.move(path1, path2)

def main():
    utilities.clear()

    print(" [+] Current categories\n")
    utilities.display_categories(aditionalInfo = False)
    print()

    print(""" [1] Add category     [2] Remove category
 [3] Merge category   [4] Rename category""")

    inp = input("\n>>> ")

    if inp == "1":
        add_cat()
    elif inp == "2":
        del_cat()
    elif inp == "3":
        mer_cat()
    elif inp == "4":
        ren_cat()
