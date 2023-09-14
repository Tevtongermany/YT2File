import tkinter
import customtkinter
import requests
import yt_dlp
import os
import threading
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
        pass

# I aint documenting everything so
# be careful

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window Settings
        self.geometry("450x400")
        self.title("yt2file 2.4.1")
        self.iconbitmap("favicon.ico")
        self.resizable(False, False)

        def download():
            try:
                if self.File.get() == "mp4":
                    url = self.linktofile.get()
                    with yt_dlp.YoutubeDL(ydl_opts_mp4) as ydl:
                        self.status.configure(text="Status: Downloading!")
                        ydl.download(url)

                elif self.File.get() == "mp3":
                    url = self.linktofile.get()
                    with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
                        self.status.configure(text="Status: Downloading!")
                        ydl.download(url)
                    
            except Exception as e:
                print(e)
                self.status.configure(text="Status: Something Went Wrong >:/")

        def progress(d):
            downloadper = d['_percent_str']
            print(d['status'])
            hs = downloadper.replace("\x1b[0;94m","")
            finaloutput = hs.replace("\x1b[0m","")
            calculated_downloadedper = float(finaloutput.replace("%",""))/100
            self.progressbar.set(value=calculated_downloadedper)
            if d['status'] == "finished":
                self.status.configure(text="Status: Done")

        ydl_opts_mp4 = {
        'logger': Logger(),
        'progress_hooks': [progress],
        "format":"mp4",
        'ffmpeg_location': 'ffmpeg/bin',
        'outtmpl':f"video/%(title)s.%(ext)s"
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
            }],
        'outtmpl':f"video/%(title)s.%(ext)s"

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

        def make_video_folder():
            if os.path.exists("video"):
                pass
            else:
                os.mkdir("video")

        def downloadffmpeg():
            r =requests.get(url="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip")
            open("ffmpeg.zip","wb").write(r.content)
            print("downloaded ffmpeg Starting Stage 2")
            stage2unzipffmpeg()
            
        def stage2unzipffmpeg():
            with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
                zip_ref.extractall("")
                os.rename("ffmpeg-master-latest-win64-gpl","ffmpeg")
            os.remove("ffmpeg.zip")

        if os.path.exists("ffmpeg"):
            pass
        else:
            downloadffmpeg()

        make_video_folder()



if __name__ == "__main__":
    app = App()
    app.mainloop()