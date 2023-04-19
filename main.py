import ctypes
import string
import subprocess
import sys
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
Resolution = 720
folderpath = ""
settingsfilename = "settings.ini"

if os.path.exists(settingsfilename):
    config = configparser.ConfigParser()
    config.read(settingsfilename)
    filepath = config.get('Settings', 'FilePath')
    Resolution = config.get('Settings', 'Resolution')
else:
    config = configparser.ConfigParser()
    config['Settings'] = {'FilePath': '', 'Resolution': '720'}
    with open(settingsfilename, 'w') as f:
        config.write(f)

def check_install(*args):
    try:
        subprocess.check_output(args,
                    stderr=subprocess.STDOUT)
        return True
    except OSError as e:
        return False
    
def check_ffmpeg():
    return check_install('ffmpeg', "-version")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    

# class HelpWindow(customtkinter.CTkToplevel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("600x300")
#         self.title("yt2file Help Window")
#         self.iconbitmap("Yt2file.ico") 
#         self.resizable(False, False)
        
#         self.text = customtkinter.CTkLabel(master=self,text="Youtube2File",width=10,height=10,corner_radius=8,font=("inter",20))
#         self.text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)

#         self.text2 = customtkinter.CTkLabel(master=self,text="Before you hit Start download check if there is a link in the Entry Field if not put\n in one after that you can press confirm if the title appears then you did everything correct\n if not and something like Video Not Found! Appears you put in the wrong link,\n only links like https://www.youtube.com/watch?v=dQw4w9WgXcQ\n or https://youtu.be/dQw4w9WgXcQ are supported",font=("inter",15))
#         self.text2.pack(padx=0.5, pady=100, anchor="center")
#         # Motherfucker ^ 
# for later use


class ffmpeginstallwindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300")
        self.title("yt2file FFMPEG Missing!")
        self.iconbitmap("Yt2file.ico") 
        self.resizable(False, False)
        self.text = customtkinter.CTkLabel(master=self,text="FFmpeg Missing!",width=10,height=10,corner_radius=8,font=("inter",20))
        self.text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)
        self.infotext = customtkinter.CTkLabel(master=self,text="Looks like your system doesn't have ffmpeg installed\nif you want to install ffmpeg click on the 'Install FFmpeg' Button\nYou have to have at least 200mbs of free space on your c drive")
        self.infotext.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER,)
        self.status_text = customtkinter.CTkLabel(master=self,text="Status: Inactive")
        self.status_text.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER,)
        self.ffmpegdownload = customtkinter.CTkButton(master=self,text="Install FFmpeg",command=lambda: threading.Thread(target=downloadffmpeg).start())
        self.ffmpegdownload.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER,)

        def moveffmpeg():
            os.rename("ffmpeg-master-latest-win64-gpl","ffmpeg")
            shutil.move("ffmpeg","C:/")
        def downloadffmpeg():
            self.status_text.configure(text="Status: Downloading FFmpeg")
            self.ffmpegdownload.configure(state="disabled")
            r =requests.get(url="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip")
            open("ffmpeg.zip","wb").write(r.content)
            print("downloaded ffmpeg Starting Stage 2")
            stage2unzipffmpeg()
            
        def stage2unzipffmpeg():
            self.status_text.configure(text="Status: Unzipping FFmpeg")
            with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
                zip_ref.extractall("")
            print("ffmpeg Extracted! Moving to C:/")
            if os.path.exists("ffmpeg") and is_admin:
                moveffmpeg()
                print("Moved FFmpeg to C:/")
                self.status_text.configure(text="Status: Done! Opening last instruction")
                webbrowser.open("https://github.com/Tevtongermany/YT2FILE/blob/main/LastStep.md")
            else:
                print("User not admin requesting permission")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                moveffmpeg()
                print("Moved FFmpeg to C:/")
                self.status_text.configure(text="Status: Done! Opening last instruction")
                webbrowser.open("https://github.com/Tevtongermany/YT2FILE/blob/main/LastStep.md")
                
        
        


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window Settings
        self.geometry("450x400")
        self.title("yt2file 2.3")
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
                else:
                    self.open_FFMPEGWindow()
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
        }
        
        ydl_opts_mp3 = {
        'logger': Logger(),
        'progress_hooks': [progress],
        'format': 'bestaudio/best',
        'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',    
            }]
        
        }





        # def setres():
        #     try:
        #         dialog = customtkinter.CTkInputDialog(text="Dont include the p at the end\n Sidenote this does not affect audio", title="Resolution Configurator")
        #         Resolution = int(dialog.get_input())
        #         self.res.configure(text=f"Resolution: {str(Resolution)}p")
        #         config = configparser.ConfigParser()
        #         config['Settings'] = {'File Path': f'{filepath}','Resolution': f'{str(Resolution)}'}
        #         with open(settingsfilename, 'w') as f:
        #             config.write(f)
        #     except:
        #         pass





        self.yttitle = customtkinter.CTkLabel(master=self,text="Title: None")
        self.yttitle.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER,)

        self.status = customtkinter.CTkLabel(master=self,text="Status: Idle")
        self.status.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.res = customtkinter.CTkButton(master=self,text="Resolution disabled")
        self.res.place(relx=0.5, rely=0.32, anchor=tkinter.CENTER)

        self.linktofile = customtkinter.CTkEntry(master=self,width=300)
        self.linktofile.place(relx=0.5, rely=0.4,anchor=tkinter.CENTER)


        self.File = customtkinter.CTkOptionMenu(master=self,values=["mp4","mp3"])
        self.File.place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)


        self.button = customtkinter.CTkButton(master=self, text="Start Download", command=lambda: threading.Thread(target=download).start())
        self.button.place(relx=0.50, rely=0.6, anchor=tkinter.CENTER)
        if check_ffmpeg() == False:
            self.ffmpegbutton = customtkinter.CTkButton(master=self, text="!",width=20,height=20,command=self.open_FFMPEGWindow)
            self.ffmpegbutton.place(relx=0.03, rely=0.03, anchor=tkinter.CENTER)
            self.File.configure(values=["mp4","mp3 (ffmpeg missing)"],)



        # self.button2 = customtkinter.CTkButton(self, text="Help",width=9,command=self.open_HelpWindow)
        # self.button2.place(relx=0.95, rely=0.96, anchor=tkinter.CENTER)

        self.progressbar = customtkinter.CTkProgressBar(master=self)
        self.progressbar.place(relx=0.50, rely=0.7, anchor=tkinter.CENTER)

        self.text = customtkinter.CTkLabel(master=self,text="Youtube2File",width=10,height=10,corner_radius=8,font=("inter",20))
        self.text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)

        self.progressbar.set(value=0)
        #self.res.configure(text=f"Resolution: {str(Resolution)}p")
        self.res.configure(state="disabled")

        self.help_window = None
        self.ffmpeg_window = None

    # def open_HelpWindow(self):
    #     if self.help_window is None or not self.help_window.winfo_exists():
    #         self.help_window = HelpWindow(self)
    #     else:
    #         self.help_window.focus()

    def open_FFMPEGWindow(self):
        if self.ffmpeg_window is None or not self.ffmpeg_window.winfo_exists():
            self.ffmpeg_window = ffmpeginstallwindow(self)
        else:
            self.ffmpeg_window.focus()
    def remove_ffmpeg_button(self):
        self.ffmpegbutton.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    


