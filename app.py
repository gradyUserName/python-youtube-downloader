import customtkinter as ctk
import tkinter.messagebox
import tkinter
from pytube import YouTube
import validators
import os
import sys
import threading

# auto-py-to-exe to create installer

# Get releative path (used to set app icon in a way that doesn't break when packaged by pyinstaller)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

# App
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        # Configure window
        self.title("YouTube Video Downloader")
        self.geometry("600x300")
        
        # Font
        my_font = ctk.CTkFont(size=15)

        # Configure grid layout
        self.grid_rowconfigure((1), weight=0)
        self.grid_columnconfigure((1), weight=1)

        # Enter the URL
        self.url_label = ctk.CTkLabel(self, text="Video URL:", font=my_font)
        self.url_label.grid(row=1, column=1, padx=(20, 20), pady=(20, 10))
        self.url = ctk.CTkEntry(self, placeholder_text="e.g. https://www.youtube.com/watch?v=abcd1234etc", font=my_font)
        self.url.grid(row=2, column=1, padx=(20, 20), pady=(0, 0), sticky="ew")

        # Save location label
        self.save_location_label = ctk.CTkLabel(self, text="Save location:", font=my_font)
        self.save_location_label.grid(row=3, column=1, padx=(20, 20), pady=(20, 10))

        # Save location radio button frame
        self.radio_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_button_frame.grid(row=4, column=1, sticky="ew")
        self.radio_button_frame.grid_columnconfigure((1, 2, 3), weight=1)

        # Save location radio buttons
        self.radio_var = tkinter.IntVar(value=0)
        self.rb_desktop = ctk.CTkRadioButton(self.radio_button_frame, variable=self.radio_var, value=0, text="Desktop")
        self.rb_desktop.grid(row=1, column=1)
        self.rb_downloads = ctk.CTkRadioButton(self.radio_button_frame, variable=self.radio_var, value=1, text="Downloads")
        self.rb_downloads.grid(row=1, column=2)
        self.rb_videos = ctk.CTkRadioButton(self.radio_button_frame, variable=self.radio_var, value=2, text="Videos")
        self.rb_videos.grid(row=1, column=3)

        # Download button
        self.download_button = ctk.CTkButton(self, text="Download", font=my_font, command=self.download_start)
        self.download_button.grid(row=5, column=1, padx=(20, 20), pady=(30, 20))
    
    # Download starter
    def download_start(self):
        # Loading bar
        self.loading_bar = ctk.CTkProgressBar(self, orientation="horizontal", mode="indeterminate")
        self.loading_bar.grid(row=6, column=1)
        self.loading_bar.start()

        # Set home path
        home_path = os.path.expanduser("~")

        # Set url
        url = self.url.get().strip('\n \r\n \t')

        # If valid url, start self.download in new thread
        if validators.url(url):
            threading.Thread(target=self.download, args=(self, url, home_path), daemon=True).start()
        else:
            tkinter.messagebox.showerror(title="Error", message="Invalid URL")
            self.loading_bar.destroy()
    
    # Actual download
    def download(self, dot, url, home_path):
        # Get yt object
        try:
            yt = YouTube(url).streams.get_highest_resolution()
        except:
            tkinter.messagebox.showerror(title="Error", message="Error occurred while fetching video streams")
        
        # Download stream
        match self.radio_var.get():
            case 0:
                try:
                    yt.download("".join([home_path, "\Desktop"]))
                    tkinter.messagebox.showinfo(title="Download Complete!", message=("Saved to " + "".join([home_path, "\Desktop"])))
                except:
                    tkinter.messagebox.showerror(title="Error", message="Error occurred while downloading video")
            case 1:
                try:
                    yt.download("".join([home_path, "\Downloads"]))
                    tkinter.messagebox.showinfo(title="Download Complete!", message=("Saved to " + "".join([home_path, "\Downloads"])))
                except:
                    tkinter.messagebox.showerror(title="Error", message="Error occurred while downloading video")
            case 2:
                try:
                    yt.download("".join([home_path, "\Videos"]))
                    tkinter.messagebox.showinfo(title="Download Complete!", message=("Saved to " + "".join([home_path, "\Videos"])))
                except:
                    tkinter.messagebox.showerror(title="Error", message="Error occurred while downloading video")

        # Destroy loading bar
        self.loading_bar.destroy()
        

app = App()
app.resizable(False, False)
app.iconbitmap(resource_path("ytd_icon.ico"))
app.mainloop()
