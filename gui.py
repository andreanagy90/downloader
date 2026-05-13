#!/usr/bin/env python3

from tkinter import *
import pyfiglet
import subprocess
import yt_dlp, sys, threading, os
from tkinter import messagebox

format = ["mp4 - HIGH", "mp4 - LOW", "mp3"]

WIDTH = 600
HEIGHT = 800

stop_flag = False

music_folder = "Musics"
video_folder = "Videos"

os.makedirs(music_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

rename_to = None
new_name = ""


def check_update():
    check_script = "yt-dlp --version"
    available="curl -s https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest | grep '\"tag_name\"' | grep -o '[0-9]\\{4\\}.[0-9]\\{2\\}.[0-9]\\{2\\}'"

    version = subprocess.getoutput(check_script)
    available_version = subprocess.getoutput(available)

    output_console.insert("end", f" Telepített Verzió: {version}\n")
    output_console.see("end")


    if version != available_version:
        output_console.insert("end", f" Elérhető új Verzió\n")
    else: 
        output_console.insert("end", f" Legfrissebb verzió telepítve\n")
        
    output_console.see("end")


def update():
    output_console.insert("end", " Frissítés folyamatban...\n")
    output_console.insert("end", " Ne zárja be a programot!\n")

    output_console.see("end")
    update_script = """
    python3 -m pip install --upgrade --force-reinstall "git+https://github.com/yt-dlp/yt-dlp.git@master" --break-system-packages
    """
    subprocess.run(update_script, shell=True, executable="/bin/bash")

    check_script = "yt-dlp --version"
    version = subprocess.getoutput(check_script)


    output_console.insert("end", f" Frissítés sikeres, új verzió : {version}\n")
    output_console.see("end")

def update_sh():
    threading.Thread(target=update).start()


def log(self,msg):
    global rename_to
    if not msg:
        return

    # ÚJ yt-dlp üzenet
    if "exists, skipping" in msg:
        output_console.insert("end", "A fájl már létezik " + msg + "\n")
        output_console.see("end")

        messagebox.showinfo("A fájl már létezik",msg)

    # RÉGI yt-dlp üzenet
    if "has already been downloaded" in msg:
        output_console.insert("end", "A fájl már létezik" + msg + "\n")
        output_console.see("end")

        messagebox.showinfo("A fájl már létezik",msg)

    lower = msg.lower()

    if lower.startswith("error") or "unsupported url" in lower or "failed" in lower:
        output_console.insert("end", "❌ " + msg + "\n")
        output_console.see("end")


def open_music():
    subprocess.Popen(["xdg-open", music_folder])

def open_video():
    subprocess.Popen(["xdg-open", video_folder])


def progress_hook(d):
    global stop_flag


    if stop_flag:
        output_console.insert("end", "⛔ Letöltés megszakítva a felhasználó által.\n")
        output_console.see("end")
        raise yt_dlp.utils.DownloadError("Letöltés megszakítva a felhasználó által.") 

    if d['status'] == 'downloading':
        output_console.insert("end", f"⬇️  Letöltés: {d['_percent_str']} ({d['_speed_str']})\n")
        output_console.see("end")

    elif d['status'] == 'finished':
        output_console.insert("end", "✅ Letöltés kész.\n")
        output_console.see("end")

    elif d['status'] == 'error':
        output_console.insert("end", "❌ Hiba történt!\n")
        output_console.see("end")


def download_video(url):
    ydl_opts = {
        'format': '((bv*[vcodec^=avc1]+ba[acodec^=mp4a])/bestvideo+bestaudio/best)',
        'merge_output_format': 'mp4',  # Átkonvertálás .mp4-re
        'outtmpl': f'{video_folder}/%(title)s.%(ext)s',
        'verbose': True,
        'writesubtitles': False,        # Feliratok letöltése
        'writeautomaticsub': False,     # Automatikusan generált felirat is jöhet
        'subtitleslangs': [],
        'concurrent_fragment_downloads': 10,
        'subtitleslangs': ['hu','en'],# Magyar vagy angol, ha van
        'subtitlesformat': 'srt',
        'noplaylist': True,
        'extract_flat': 'discard_in_playlist',
        'logger': type("L", (), {"debug": log, "info": log, "warning": log, "error": log})(),
        'progress_hooks': [progress_hook]
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_video_low(url):
    ydl_opts = {
        'format': '((bv*[vcodec^=avc1]+ba[acodec^=mp4a])/bestvideo+bestaudio/best)',
        'merge_output_format': 'mp4',  # Átkonvertálás .mp4-re
        'outtmpl': f'{video_folder}/%(title)s.%(ext)s',
        'verbose': True,
        'writesubtitles': False,        # Feliratok letöltése
        'writeautomaticsub': False,     # Automatikusan generált felirat is jöhet
        'subtitleslangs': ['hu','en'],# Magyar vagy angol, ha van
        'subtitleslangs': [],
        'concurrent_fragment_downloads': 10,
        'subtitlesformat': 'srt',
        'noplaylist': True,
        'extract_flat': 'discard_in_playlist',
        'logger': type("L", (), {"debug": log, "info": log, "warning": log, "error": log})(),

        'progress_hooks': [progress_hook]
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_mp3(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
       
        'outtmpl': f'{music_folder}/%(title)s.%(ext)s',
        'verbose': True,
        'postprocessors': [{
		'key' : 'FFmpegExtractAudio',
		'preferredcodec':'mp3',
       	'preferredquality':'192'}],
        'noplaylist': True,
        'extract_flat': 'discard_in_playlist',
        'subtitleslangs': [],

        'logger': type("L", (), {"debug": log, "info": log, "warning": log, "error": log})(),

        'progress_hooks': [progress_hook]
       
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download():
    link = url.get()
    format_opt = f.get()

    if not link:
        return
    

    #output_console.insert()
    if format_opt == 0:
        download_video(link)
    elif format_opt == 1:
        download_video_low(link)
    elif format_opt == 2:
        download_mp3(link)

def start_download():
    global stop_flag
    stop_flag = False
    threading.Thread(target=download).start()
   
def stop_download():
    global stop_flag
    stop_flag = True
    output_console.insert("end", "⛔ Letöltés megszakítása...\n")
    output_console.see("end")

def info():
    infos = "Szoftververzió    : 1.0\nFejlesztve:        : 13/05/2026\nLast update:       : 13/05/2026\nSzerzői jogvédelem alatt!\nLoveQuinn - Fejlesztő\nE-mail:        andrea.nagy1990@icloud.com"
    messagebox.showinfo(title= "Szoftverinformáció", message=infos)

window = Tk()
window.geometry("600x800+5+5")
window.title("LQ Downloader")
window.config(background="black")
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", lambda: (os._exit(0)))

menubar = Menu(window, bg="black", fg="#1bd91b")
window.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0, bg="black", fg="#1bd91b")
info_menu = Menu(menubar, tearoff=0, bg="black", fg="#1bd91b")


menubar.add_cascade(label= "Fájl", menu=file_menu, background="black", foreground= "#1bd91b")
menubar.add_cascade(label= "Info", menu=info_menu, background="black", foreground= "#1bd91b")


file_menu.add_command(label="Open Video Directory", command=open_video)
file_menu.add_command(label="Open Music Directory", command=open_music)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)

info_menu.add_command(label="Check version", command=check_update)
info_menu.add_command(label="Update", command=update_sh)
info_menu.add_command(label="Software Info", command=info)


frame = Frame(window, bg="black", bd=5)
frame.pack()



title_art = pyfiglet.figlet_format("LQ Downloader", font="standard")
title_label = Label(frame, text=title_art, font=("Courier", 8), fg="#1bd91b", bg="black",padx= 10, pady=20,
                    justify="left", anchor="nw")
title_label.pack()

url_text = Label(frame, text= " Enter or Paste ( Ctrl + V ) URL ", font=("Arial, 18"), fg= "#1bd91b", bg= "black", padx= 5, pady= 5)
url_text.pack()


url = Entry(frame, font=("Arial", 10), fg="#1bd91b", bg="black", width=250, insertbackground="#1bd91b")
url.pack(padx= 10, pady= 10)

f = IntVar()

for i in range(len(format)):
    radio_button = Radiobutton(frame, text=format[i],
                               variable=f,
                               value=i,
                               font=("Arial", 10),
                               width= 40,
                               fg="#1bd91b",
                               bg = "black",
                               padx= 5,
                               pady= 5,
                               activebackground="#2B2E2B",
                               activeforeground="#175c17")
    
    radio_button.pack()

output_console = Text(frame, height= 15, width= 70, bg="#2B2E2B", fg="#1c881c", bd=3, highlightcolor="#1c881c",
                      highlightbackground="#64d364")
output_console.pack(pady= 10)

download_button = Button(frame, text= " Download ", font= ("Arial", 10),
                        fg= "#1bd91b", bg="#2B2E2B", padx= 10, pady= 10,width= 50,
                        relief=GROOVE, command=start_download)

download_button.pack(pady=10)

stop_button = Button(frame, text= " STOP ", font= ("Arial", 10),
                        fg= "#cc1b1b", bg="#2B2E2B", padx= 10, pady= 10,width= 50,
                        relief=GROOVE, command=stop_download)

stop_button.pack(pady=10)



window.mainloop()
