import os
import sys
import threading
import time
import shutil
from tkinter import StringVar, BooleanVar
import customtkinter as ctk
from PIL import Image
import youtube_dl
from pynotifier import Notification
import requests
from bs4 import BeautifulSoup

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Ensure required directories exist
def check_required_folders():
    folders = ["Video Downloads", "Videos", "Pictures"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Main Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("PH Downloader")
        self.geometry("900x600")
        self.minsize(800, 550)
        
        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        # App logo/title
        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame, 
            text="PH Downloader",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Create navigation buttons
        self.video_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=0, 
            height=40, 
            border_spacing=10, 
            text="Video Downloader",
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.video_button_event
        )
        self.video_button.grid(row=1, column=0, sticky="ew")
        
        self.picture_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=0, 
            height=40, 
            border_spacing=10, 
            text="Picture Downloader",
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.picture_button_event
        )
        self.picture_button.grid(row=2, column=0, sticky="ew")
        
        self.category_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=0, 
            height=40, 
            border_spacing=10, 
            text="Category Manager",
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.category_button_event
        )
        self.category_button.grid(row=3, column=0, sticky="ew")
        
        # Appearance mode toggle
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, 
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")
        
        # Create video frame
        self.video_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.video_frame.grid_columnconfigure(0, weight=1)
        
        # Video download components
        self.video_frame_large_label = ctk.CTkLabel(
            self.video_frame, 
            text="Video Downloader", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.video_frame_large_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.video_frame_info_label = ctk.CTkLabel(
            self.video_frame, 
            text="Enter the URL of the video you want to download",
            font=ctk.CTkFont(size=14)
        )
        self.video_frame_info_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # URL entry
        self.video_url_frame = ctk.CTkFrame(self.video_frame)
        self.video_url_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.video_url_frame.grid_columnconfigure(0, weight=1)
        
        self.video_url_entry = ctk.CTkEntry(
            self.video_url_frame, 
            placeholder_text="Video URL"
        )
        self.video_url_entry.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="ew")
        
        self.video_download_button = ctk.CTkButton(
            self.video_url_frame, 
            text="Download",
            command=self.download_video
        )
        self.video_download_button.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Categories section
        self.categories_label = ctk.CTkLabel(
            self.video_frame, 
            text="Categories",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.categories_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Categories container frame
        self.categories_frame = ctk.CTkFrame(self.video_frame)
        self.categories_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.categories_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_rowconfigure(4, weight=1)
        
        # Categories scrollable frame
        self.categories_scrollable = ctk.CTkScrollableFrame(self.categories_frame, label_text="")
        self.categories_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # New category entry
        self.new_category_frame = ctk.CTkFrame(self.video_frame)
        self.new_category_frame.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.new_category_entry = ctk.CTkEntry(
            self.new_category_frame,
            placeholder_text="New category name"
        )
        self.new_category_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.add_category_button = ctk.CTkButton(
            self.new_category_frame,
            text="Add Category",
            command=self.add_new_category
        )
        self.add_category_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.new_category_frame.grid_columnconfigure(0, weight=1)
        
        # Progress bar and status
        self.progress_frame = ctk.CTkFrame(self.video_frame)
        self.progress_frame.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Create picture frame
        self.picture_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.picture_frame.grid_columnconfigure(0, weight=1)
        
        # Picture download components
        self.picture_frame_large_label = ctk.CTkLabel(
            self.picture_frame, 
            text="Picture Downloader", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.picture_frame_large_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.picture_frame_info_label = ctk.CTkLabel(
            self.picture_frame, 
            text="Enter the URL of the album or individual picture you want to download",
            font=ctk.CTkFont(size=14)
        )
        self.picture_frame_info_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Picture URL entry
        self.picture_url_frame = ctk.CTkFrame(self.picture_frame)
        self.picture_url_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.picture_url_frame.grid_columnconfigure(0, weight=1)
        
        self.picture_url_entry = ctk.CTkEntry(
            self.picture_url_frame, 
            placeholder_text="Album or Picture URL"
        )
        self.picture_url_entry.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="ew")
        
        self.picture_download_button = ctk.CTkButton(
            self.picture_url_frame, 
            text="Download",
            command=self.download_picture
        )
        self.picture_download_button.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Picture download progress
        self.picture_progress_frame = ctk.CTkFrame(self.picture_frame)
        self.picture_progress_frame.grid(row=3, column=0, padx=20, pady=(20, 20), sticky="ew")
        self.picture_progress_frame.grid_columnconfigure(0, weight=1)
        
        self.picture_status_label = ctk.CTkLabel(
            self.picture_progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=12)
        )
        self.picture_status_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.picture_progress_bar = ctk.CTkProgressBar(self.picture_progress_frame)
        self.picture_progress_bar.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.picture_progress_bar.set(0)
        
        # Picture download info
        self.picture_info_frame = ctk.CTkFrame(self.picture_frame)
        self.picture_info_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.picture_frame.grid_rowconfigure(4, weight=1)
        
        self.picture_info_scrollable = ctk.CTkScrollableFrame(self.picture_info_frame, label_text="Download Information")
        self.picture_info_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.picture_info_label = ctk.CTkLabel(
            self.picture_info_scrollable,
            text="No downloads in progress",
            font=ctk.CTkFont(size=12),
            wraplength=600
        )
        self.picture_info_label.pack(padx=10, pady=10, anchor="w")
        
        # Create category frame
        self.category_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.category_frame.grid_columnconfigure(0, weight=1)
        
        # Category manager components
        self.category_frame_large_label = ctk.CTkLabel(
            self.category_frame, 
            text="Category Manager", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.category_frame_large_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.category_frame_info_label = ctk.CTkLabel(
            self.category_frame, 
            text="Manage your video categories",
            font=ctk.CTkFont(size=14)
        )
        self.category_frame_info_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Categories list
        self.category_list_frame = ctk.CTkFrame(self.category_frame)
        self.category_list_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.category_frame.grid_rowconfigure(2, weight=1)
        
        self.category_list_label = ctk.CTkLabel(
            self.category_list_frame,
            text="Available Categories:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.category_list_label.pack(padx=10, pady=(10, 0), anchor="w")
        
        self.category_list_scrollable = ctk.CTkScrollableFrame(self.category_list_frame)
        self.category_list_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Category actions
        self.category_actions_frame = ctk.CTkFrame(self.category_frame)
        self.category_actions_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.category_actions_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.add_cat_button = ctk.CTkButton(
            self.category_actions_frame,
            text="Add Category",
            command=self.add_category_manager
        )
        self.add_cat_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.rename_cat_button = ctk.CTkButton(
            self.category_actions_frame,
            text="Rename Category",
            command=self.rename_category
        )
        self.rename_cat_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.merge_cat_button = ctk.CTkButton(
            self.category_actions_frame,
            text="Merge Categories",
            command=self.merge_categories
        )
        self.merge_cat_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.delete_cat_button = ctk.CTkButton(
            self.category_actions_frame,
            text="Delete Category",
            command=self.delete_category
        )
        self.delete_cat_button.grid(row=0, column=3, padx=10, pady=10)
        
        self.refresh_cat_button = ctk.CTkButton(
            self.category_actions_frame,
            text="Refresh List",
            command=self.refresh_category_list
        )
        self.refresh_cat_button.grid(row=0, column=4, padx=10, pady=10)
        
        # Select default frame
        self.select_frame_by_name("video")
        self.update_categories()
        self.update_category_list()
        
    def select_frame_by_name(self, name):
        # Set button colors for selected button
        self.video_button.configure(fg_color=("gray75", "gray25") if name == "video" else "transparent")
        self.picture_button.configure(fg_color=("gray75", "gray25") if name == "picture" else "transparent")
        self.category_button.configure(fg_color=("gray75", "gray25") if name == "category" else "transparent")
        
        # Show selected frame
        if name == "video":
            self.video_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.video_frame.grid_forget()
            
        if name == "picture":
            self.picture_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.picture_frame.grid_forget()
            
        if name == "category":
            self.category_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.category_frame.grid_forget()
    
    def video_button_event(self):
        self.select_frame_by_name("video")
        
    def picture_button_event(self):
        self.select_frame_by_name("picture")
        
    def category_button_event(self):
        self.select_frame_by_name("category")
        self.update_category_list()
        
    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def update_categories(self):
        # Clear existing categories
        for widget in self.categories_scrollable.winfo_children():
            widget.destroy()
            
        # Get categories
        category_list = [x[0][7:] for x in os.walk("Videos/")][1:]
        
        self.category_vars = {}
        
        # Create radio buttons for each category
        for i, category in enumerate(category_list):
            var = StringVar(value="")
            radio = ctk.CTkRadioButton(
                self.categories_scrollable,
                text=category,
                variable=var,
                value=category
            )
            radio.grid(row=i, column=0, padx=10, pady=(5, 5), sticky="w")
            self.category_vars[category] = var
            
        if not category_list:
            no_cat_label = ctk.CTkLabel(
                self.categories_scrollable,
                text="No categories found. Create one below.",
                font=ctk.CTkFont(size=12)
            )
            no_cat_label.pack(padx=10, pady=10)
            
    def update_category_list(self):
        # Clear existing categories
        for widget in self.category_list_scrollable.winfo_children():
            widget.destroy()
            
        # Get categories
        category_list = [x[0][7:] for x in os.walk("Videos/")][1:]
        
        # Create labels for each category
        for i, category in enumerate(category_list):
            cat_frame = ctk.CTkFrame(self.category_list_scrollable)
            cat_frame.pack(fill="x", padx=5, pady=5)
            
            cat_label = ctk.CTkLabel(
                cat_frame,
                text=category,
                font=ctk.CTkFont(size=14)
            )
            cat_label.pack(side="left", padx=10, pady=10)
            
        if not category_list:
            no_cat_label = ctk.CTkLabel(
                self.category_list_scrollable,
                text="No categories found. Create one using the Add Category button.",
                font=ctk.CTkFont(size=12)
            )
            no_cat_label.pack(padx=10, pady=10)
            
    def add_new_category(self):
        category_name = self.new_category_entry.get().strip()
        if category_name:
            if not os.path.exists(f"Videos/{category_name}"):
                os.makedirs(f"Videos/{category_name}")
                self.new_category_entry.delete(0, 'end')
                self.update_categories()
                self.show_toast("Category Added", f"Category '{category_name}' has been created.")
            else:
                self.show_toast("Category Exists", f"Category '{category_name}' already exists.")
        else:
            self.show_toast("Error", "Please enter a category name.")
            
    def add_category_manager(self):
        dialog = ctk.CTkInputDialog(text="Enter new category name:", title="Add Category")
        category_name = dialog.get_input()
        if category_name:
            if not os.path.exists(f"Videos/{category_name}"):
                os.makedirs(f"Videos/{category_name}")
                self.update_category_list()
                self.update_categories()
                self.show_toast("Category Added", f"Category '{category_name}' has been created.")
            else:
                self.show_toast("Category Exists", f"Category '{category_name}' already exists.")
                
    def rename_category(self):
        dialog1 = ctk.CTkInputDialog(text="Enter the category name to rename:", title="Rename Category")
        old_name = dialog1.get_input()
        
        if old_name and os.path.exists(f"Videos/{old_name}"):
            dialog2 = ctk.CTkInputDialog(text=f"Enter new name for '{old_name}':", title="Rename Category")
            new_name = dialog2.get_input()
            
            if new_name and new_name != old_name:
                if not os.path.exists(f"Videos/{new_name}"):
                    shutil.move(f"Videos/{old_name}", f"Videos/{new_name}")
                    self.update_category_list()
                    self.update_categories()
                    self.show_toast("Category Renamed", f"Category renamed from '{old_name}' to '{new_name}'.")
                else:
                    self.show_toast("Category Exists", f"Category '{new_name}' already exists.")
        elif old_name:
            self.show_toast("Category Not Found", f"Category '{old_name}' does not exist.")
            
    def merge_categories(self):
        dialog1 = ctk.CTkInputDialog(text="Enter the source category name:", title="Merge Categories")
        source_name = dialog1.get_input()
        
        if source_name and os.path.exists(f"Videos/{source_name}"):
            dialog2 = ctk.CTkInputDialog(text=f"Enter the target category name:", title="Merge Categories")
            target_name = dialog2.get_input()
            
            if target_name and os.path.exists(f"Videos/{target_name}"):
                # Merge operation involves copying files
                source_path = f"Videos/{source_name}"
                target_path = f"Videos/{target_name}"
                
                # Get all files from source
                files = os.listdir(source_path)
                
                # Thread the merge operation
                threading.Thread(target=self.merge_thread, args=(source_path, target_path, files)).start()
                
            elif target_name:
                self.show_toast("Category Not Found", f"Target category '{target_name}' does not exist.")
                
        elif source_name:
            self.show_toast("Category Not Found", f"Source category '{source_name}' does not exist.")
            
    def merge_thread(self, source_path, target_path, files):
        conflict_resolution = None
        
        for file in files:
            source_file = os.path.join(source_path, file)
            target_file = os.path.join(target_path, file)
            
            if os.path.exists(target_file) and conflict_resolution != "keep_all" and conflict_resolution != "skip_all":
                # Ask for conflict resolution
                # This is simplified for demonstration - in a real app you'd use a proper dialog
                dialog = ctk.CTkInputDialog(
                    text=f"File '{file}' already exists in target.\n'keep' to overwrite\n'skip' to skip\n'keep_all' to overwrite all\n'skip_all' to skip all",
                    title="File Conflict"
                )
                conflict_resolution = dialog.get_input()
                
            if not os.path.exists(target_file) or conflict_resolution == "keep" or conflict_resolution == "keep_all":
                shutil.copy2(source_file, target_file)
                
        self.update_category_list()
        self.update_categories()
        self.show_toast("Categories Merged", "Categories have been merged successfully.")
            
    def delete_category(self):
        dialog = ctk.CTkInputDialog(text="Enter the category name to delete:", title="Delete Category")
        category_name = dialog.get_input()
        
        if category_name and os.path.exists(f"Videos/{category_name}"):
            confirm_dialog = ctk.CTkInputDialog(text=f"Are you sure you want to delete '{category_name}'? Type 'yes' to confirm:", title="Confirm Deletion")
            confirm = confirm_dialog.get_input()
            
            if confirm and confirm.lower() == "yes":
                shutil.rmtree(f"Videos/{category_name}")
                self.update_category_list()
                self.update_categories()
                self.show_toast("Category Deleted", f"Category '{category_name}' has been deleted.")
        elif category_name:
            self.show_toast("Category Not Found", f"Category '{category_name}' does not exist.")
            
    def refresh_category_list(self):
        self.update_category_list()
        self.update_categories()
        self.show_toast("List Refreshed", "Category list has been refreshed.")
            
    def download_video(self):
        url = self.video_url_entry.get().strip()
        if url:
            # Change UI to indicate download in progress
            self.video_download_button.configure(state="disabled")
            self.status_label.configure(text="Download in progress...")
            self.progress_bar.set(0.1)  # Show some progress
            
            # Start download in a separate thread
            threading.Thread(target=self.video_download_thread, args=(url,)).start()
        else:
            self.show_toast("Error", "Please enter a valid URL")
            
    def video_download_thread(self, url):
        try:
            ydl_opts = {
                'outtmpl': 'Video Downloads/%(uploader)s - %(title)s - %(id)s.%(ext)s',
                'progress_hooks': [self.video_progress_hook]
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                
            # Update UI after download
            self.after(100, lambda: self.status_label.configure(text="Download complete!"))
            self.after(100, lambda: self.progress_bar.set(1.0))
            self.after(100, lambda: self.video_download_button.configure(state="normal"))
            
            # Show notification
            Notification(
                title='Download Complete',
                description=f'Finished downloading {result["title"]}',
                duration=5,
                urgency='normal'
            ).send()
            
            # Ask user if they want to keep the video
            file_path = f"Video Downloads/{result['uploader']} - {result['title']} - {result['id']}.mp4"
            self.after(500, lambda: self.confirm_keep_video(result, file_path))
            
        except Exception as e:
            self.after(100, lambda: self.status_label.configure(text=f"Error: {str(e)}"))
            self.after(100, lambda: self.video_download_button.configure(state="normal"))
            self.after(100, lambda: self.progress_bar.set(0))
            
    def video_progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and 'downloaded_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes']
                self.after(100, lambda: self.progress_bar.set(percent))
                self.after(100, lambda: self.status_label.configure(
                    text=f"Downloading: {percent*100:.1f}% of {d['total_bytes']/1024/1024:.1f} MB"
                ))
            else:
                self.after(100, lambda: self.progress_bar.set(0.2))  # Indeterminate progress
                
    def confirm_keep_video(self, result, file_path):
        dialog = ctk.CTkDialog(title="Keep Video?", text=f'Do you want to keep "{result["title"]}"?')
        response = dialog.get_input()
        
        if response and response.lower() == "yes":
            # Find selected category
            selected_category = None
            for category, var in self.category_vars.items():
                if var.get() == category:
                    selected_category = category
                    break
                    
            if not selected_category:
                # Ask for category
                category_dialog = ctk.CTkInputDialog(text="Enter category name:", title="Select Category")
                selected_category = category_dialog.get_input()
                
            if selected_category:
                # Create category if it doesn't exist
                if not os.path.exists(f"Videos/{selected_category}"):
                    os.makedirs(f"Videos/{selected_category}")
                    self.update_categories()
                
                # Move file to appropriate category
                target_path = f"Videos/{selected_category}/{result['uploader']} - {result['title']} - {result['id']}.mp4"
                shutil.move(file_path, target_path)
                self.show_toast("Video Saved", f"Video moved to {selected_category} category")
        else:
            # Delete the file
            if os.path.exists(file_path):
                os.remove(file_path)
                self.show_toast("Video Deleted", "Video has been deleted")
                
    def download_picture(self):
        url = self.picture_url_entry.get().strip()
        if url:
            # Change UI to indicate download in progress
            self.picture_download_button.configure(state="disabled")
            self.picture_status_label.configure(text="Download in progress...")
            self.picture_progress_bar.set(0.1)  # Show some progress
            
            # Start download in a separate thread
            threading.Thread(target=self.picture_download_thread, args=(url,)).start()
        else:
            self.show_toast("Error", "Please enter a valid URL")
            
    def picture_download_thread(self, url):
        try:
            self.after(100, lambda: self.picture_info_label.configure(text="Processing URL..."))
            
            # Process for album or single picture
            if "album" in url:
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'html.parser')
                
                title = soup.title.text.strip()
                self.after(100, lambda: self.picture_info_label.configure(text=f"Album: {title}"))
                
                # Extract child image URLs
                children = [f'https://www.pornhub.com{i.find("a")["href"]}' for i in soup.find("ul", "photosAlbumsListing").children if i != "\n"]
                
                # Ensure album directory exists
                if not os.path.exists(f"Pictures/{title}"):
                    os.makedirs(f"Pictures/{title}")
                
                # Download each image
                for index, image_url in enumerate(children):
                    self.download_single_picture(image_url, title, index + 1, len(children))
            else:
                # Single picture
                self.download_single_picture(url, None, 1, 1)
                
            # Update UI after download
            self.after(100, lambda: self.picture_status_label.configure(text="Download complete!"))
            self.after(100, lambda: self.picture_progress_bar.set(1.0))
            self.after(100, lambda: self.picture_download_button.configure(state="normal"))
            
            # Show notification
            Notification(
                title='Download Complete',
                description='Finished downloading pictures',
                duration=5,
                urgency='normal'
            ).send()
            
        except Exception as e:
            self.after(100, lambda: self.picture_status_label.configure(text=f"Error: {str(e)}"))
            self.after(100, lambda: self.picture_info_label.configure(text=f"Error: {str(e)}"))
            self.after(100, lambda: self.picture_download_button.configure(state="normal"))
            self.after(100, lambda: self.picture_progress_bar.set(0))
            
    def download_single_picture(self, url, album_title, index, total):
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            
            try:
                img = soup.find("div", "centerImage").find("img")["src"]
            except TypeError:
                # Might be a video source instead of image
                img = soup.find("div", "centerImage").find("video").find("source")["src"]
                
            title = soup.title.text.strip()
            album = soup.find("div", {"id": "thumbSlider"}).find("h2").text[8:]
            
            # If no album title provided, use the page title
            if not album_title:
                album_title = title
                if not os.path.exists(f"Pictures/{album_title}"):
                    os.makedirs(f"Pictures/{album_title}")
            
            # Download the image/video
            r = requests.get(img, stream=True)
            r.raw.decode_content = True
            
            file_path = f"Pictures/{album_title}/{album} - {url.split('/')[-1]}.{img.split('.')[-1]}".replace("\\", "")
            
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            
            # Update progress
            progress = index / total
            self.after(100, lambda: self.picture_progress_bar.set(progress))
            self.after(100, lambda: self.picture_status_label.configure(
                text=f"Downloading: {progress*100:.1f}% ({index}/{total})"
            ))
            self.after(100, lambda: self.picture_info_label.configure(
                text=f"Downloaded: {file_path}\n{self.picture_info_label.cget('text')}"
            ))
            
        except Exception as e:
            self.after(100, lambda: self.picture_info_label.configure(
                text=f"Error downloading {url}: {str(e)}\n{self.picture_info_label.cget('text')}"
            ))
    
    def show_toast(self, title, message):
        # System notification
        Notification(
            title=title,
            description=message,
            duration=5,
            urgency='normal'
        ).send()
        
        # You could also implement in-app toast notifications here

def main():
    # Ensure required folders exist
    check_required_folders()
    
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main() 
