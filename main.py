import string
import tkinter
import customtkinter
from pytube import YouTube
import pytube
import os
import configparser
import threading
import time
import datetime



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# I aint documenting everything so
# be careful
Resolution = 720
folderpath = ""
settingsfilename = "settings.ini"

if os.path.exists(settingsfilename):
    config = configparser.ConfigParser()
    config.read(settingsfilename)
    filepath = config.get('Settings', 'File Path')
    Resolution = config.get('Settings', 'Resolution')
else:
    config = configparser.ConfigParser()
    config['Settings'] = {'File Path': '', 'Resolution': '720'}
    with open(settingsfilename, 'w') as f:
        config.write(f)


class HelpWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300")
        self.title("yt2file Help Window")
        self.iconbitmap("Yt2file.ico") 
        self.resizable(False, False)
        
        self.text = customtkinter.CTkLabel(master=self,text="Youtube2File",width=10,height=10,corner_radius=8,font=("inter",20))
        self.text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)

        self.text2 = customtkinter.CTkLabel(master=self,text="Before you hit Start download check if there is a link in the Entry Field if not put\n in one after that you can press confirm if the title appears then you did everything correct\n if not and something like Video Not Found! Appears you put in the wrong link,\n only links like https://www.youtube.com/watch?v=dQw4w9WgXcQ\n or https://youtu.be/dQw4w9WgXcQ are supported",font=("inter",15))
        self.text2.pack(padx=0.5, pady=100, anchor="center")
        # Motherfucker ^ 

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window Settings
        self.geometry("450x400")
        self.title("yt2file 2.2")
        self.iconbitmap("Yt2file.ico") 
        self.resizable(False, False)

        
        link = ""

        def download():
            try:
                if self.File.get() == "mp4":
                    url = self.linktofile.get()
                    yt = YouTube(url=url)
                    yt.register_on_progress_callback(func=progress)
                    yt.register_on_complete_callback(func=downloaddone)
                    title = yt.streams.first().default_filename
                    self.status.configure(text="Status: Downloading!")
                    yt.streams.filter(resolution=f"{str(Resolution)}p").first().download(output_path=folderpath,filename=f"{title}.mp4",)
                    
                else:
                    url = self.linktofile.get()
                    yt = YouTube(url=url)
                    yt.register_on_progress_callback(func=progress)
                    yt.register_on_complete_callback(func=downloaddone)
                    title = yt.streams.first().default_filename
                    self.status.configure(text="Status: Downloading!")
                    yt.streams.filter(only_audio=True).first().download(output_path=folderpath,filename=f"{title}.mp3")
            except:
                self.status.configure(text="Status: Something Went Wrong >:/")


        def progress(stream, chunk, bytes_remaining):
            size = stream.filesize
            downloaded = size - bytes_remaining
            completed = downloaded / size
            self.progressbar.set(value=completed)

        def downloaddone(stream,file_path):
            self.status.configure(text=f"Status: Done :3 ")
            time.sleep(2)
            self.progressbar.set(value=0)



        def confirm_video():
            link = self.linktofile.get()
            try:
                yt = YouTube(url=link)
                self.yttitle.configure(text=f"Title: {yt.title}")
            except:
                self.yttitle.configure(text=f"Title: Video Not Found!")

        def setres():
            try:
                dialog = customtkinter.CTkInputDialog(text="Dont include the p at the end\n Sidenote this does not affect audio", title="Resolution Configurator")
                Resolution = int(dialog.get_input())
                self.res.configure(text=f"Resolution: {str(Resolution)}p")
                config = configparser.ConfigParser()
                config['Settings'] = {'File Path': f'{filepath}','Resolution': f'{str(Resolution)}'}
                with open(settingsfilename, 'w') as f:
                    config.write(f)
            except:
                pass



        self.yttitle = customtkinter.CTkLabel(master=self,text="Title: None")
        self.yttitle.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER,)

        self.status = customtkinter.CTkLabel(master=self,text="Status: Idle")
        self.status.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.res = customtkinter.CTkButton(master=self,text="Resolution: 1080p",command=setres)
        self.res.place(relx=0.5, rely=0.32, anchor=tkinter.CENTER)

        self.linktofile = customtkinter.CTkEntry(master=self,width=300)
        self.linktofile.place(relx=0.5, rely=0.4,anchor=tkinter.CENTER)


        self.File = customtkinter.CTkComboBox(master=self,values=["mp4","mp3"])
        self.File.pack(padx=0.5, pady=190,anchor="center")


        self.confirmbutton = customtkinter.CTkButton(master=self,text="Confirm",width=10,command=lambda: threading.Thread(target=confirm_video).start())
        self.confirmbutton.place(relx=0.91, rely=0.4, anchor=tkinter.CENTER)

        self.button = customtkinter.CTkButton(master=self, text="Start Download", command=lambda: threading.Thread(target=download).start())
        self.button.place(relx=0.50, rely=0.6, anchor=tkinter.CENTER)

        self.button2 = customtkinter.CTkButton(self, text="Help",width=9,command=self.open_HelpWindow)
        self.button2.place(relx=0.95, rely=0.96, anchor=tkinter.CENTER)

        self.progressbar = customtkinter.CTkProgressBar(master=self)
        self.progressbar.place(relx=0.50, rely=0.7, anchor=tkinter.CENTER)

        self.text = customtkinter.CTkLabel(master=self,text="Youtube2File",width=10,height=10,corner_radius=8,font=("inter",20))
        self.text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)

        self.progressbar.set(value=0)
        self.res.configure(text=f"Resolution: {str(Resolution)}p")

        self.help_window = None

    def open_HelpWindow(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = HelpWindow(self)
        else:
            self.help_window.focus()

if __name__ == "__main__":
    app = App()
    app.mainloop()


