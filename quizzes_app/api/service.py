
import yt_dlp
import os
from .whisper import transcript
from .gemini import gemini

MEDIA_DIR = "media/temp"

def download_audio(url):

    os.makedirs(MEDIA_DIR, exist_ok=True)

    ydl_opts = { 
        "format": "bestaudio/best",
        "outtmpl": MEDIA_DIR + "/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def start_quiz_chain(audio_path):
    try:
        transcr = transcript(audio_path)
    except Exception:
        raise Exception("Transcription failed")   
    
    try:
        from_gemin_json = gemini(transcr)
    except Exception:
        raise Exception("Gemini request failed")   
    return from_gemin_json
    