import string
import tkinter
import customtkinter
from customtkinter import filedialog
from pytube import YouTube
import os
import random




customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


folderpath = "files/"


app = customtkinter.CTk()
app.geometry("450x200")

def button_function():
    print("button pressed")
    
def downloadmp3():
    url = linktofile.get()
    yt = YouTube(url=url)
    title = id_generator(10)
    download = yt.streams.get_highest_resolution()
    download.download(output_path=folderpath,filename=f"{title}.mp3")


def downloadmp4():
    url = linktofile.get()
    yt = YouTube(url=url)
    title = id_generator(10)
    download = yt.streams.get_highest_resolution()
    download.download(output_path=folderpath,filename=f"{title}.mp4")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))






    

text = customtkinter.CTkLabel(master=app,text="Youtube2File",width=10,height=10,corner_radius=8,font=("inter",20))
text.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER,)

linktofile = customtkinter.CTkEntry(master=app,width=300)
linktofile.place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)

buttonmp3 = customtkinter.CTkButton(master=app, text="download mp3", command=downloadmp3)
buttonmp3.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

buttonmp4 = customtkinter.CTkButton(master=app, text="download mp4", command=downloadmp4)
buttonmp4.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)


app.mainloop()
