
import yt_dlp
import os

MEDIA_DIR = "media/temp"

def download_audio(url):

    os.makedirs(MEDIA_DIR, exist_ok=True)

    ydl_opts = { 
        "format": "bestaudio/best",
        "outtmpl": MEDIA_DIR + "/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        # "cookiesfrombrowser": ("chrome",),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
