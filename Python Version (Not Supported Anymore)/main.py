import ctypes
import string
import subprocess
import sys
import time
import tkinter
import customtkinter
import requests
import yt_dlp
import os
import configparser
import threading
import shutil
import webbrowser
import zipfile

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
class Logger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

# I aint documenting everything so
# be careful

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window Settings
        self.geometry("450x400")
        self.title("yt2file 2.4")
        self.iconbitmap("Yt2file.ico")
        self.resizable(False, False)

        def download():
            try:
                if self.File.get() == "mp4":
                    url = self.linktofile.get()
                    with yt_dlp.YoutubeDL(ydl_opts_mp4) as ydl:
                        ydl.download(url)
                    self.status.configure(text="Status: Downloading!")
                elif self.File.get() == "mp3":
                    url = self.linktofile.get()
                    with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
                        ydl.download(url)
                    self.status.configure(text="Status: Downloading!")
            except:
                self.status.configure(text="Status: Something Went Wrong >:/")

        def progress(d):
            downloadper = d['_percent_str']
            calculated_downloadedper = float(downloadper.replace("%",""))/100
            self.progressbar.set(value=calculated_downloadedper)
            if calculated_downloadedper == 1:  # Do NOT ask a single question about this
                self.status.configure(text="Status: Done :3")

        ydl_opts_mp4 = {
        'logger': Logger(),
        'progress_hooks': [progress],
        "format":"mp4",
        'ffmpeg_location': 'ffmpeg/bin'
        }
        
        ydl_opts_mp3 = {
        'logger': Logger(),
        'progress_hooks': [progress],
        'format': 'bestaudio/best',
        'ffmpeg_location': 'ffmpeg/bin',
        'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',    
            }]
        
        }

        self.status = customtkinter.CTkLabel(master=self,text="Status: Idle")
        self.status.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.linktofile = customtkinter.CTkEntry(master=self,width=300)
        self.linktofile.place(relx=0.5, rely=0.4,anchor=tkinter.CENTER)


        self.File = customtkinter.CTkOptionMenu(master=self,values=["mp4","mp3"])
        self.File.place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)


        self.button = customtkinter.CTkButton(master=self, text="Start Download", command=lambda: threading.Thread(target=download).start())
        self.button.place(relx=0.50, rely=0.6, anchor=tkinter.CENTER)


        self.progressbar = customtkinter.CTkProgressBar(master=self)
        self.progressbar.place(relx=0.50, rely=0.7, anchor=tkinter.CENTER)

        self.text = customtkinter.CTkLabel(master=self,text="Youtube2File",width=10,height=10,corner_radius=8,font=("inter",20))
        self.text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)

        self.progressbar.set(value=0)
        # If FFmpeg doesn't exist shouldn't happen but if it happens this downloads it
        def downloadffmpeg():
            r =requests.get(url="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip")
            open("ffmpeg.zip","wb").write(r.content)
            print("downloaded ffmpeg Starting Stage 2")
            stage2unzipffmpeg()
            
        def stage2unzipffmpeg():
            with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
                zip_ref.extractall("")
                os.rename("ffmpeg-master-latest-win64-gpl","ffmpeg")

        if os.path.exists("ffmpeg"):
            pass
        else:
            downloadffmpeg()

if __name__ == "__main__":
    app = App()
    app.mainloop()