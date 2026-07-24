
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
    """
    Transcribe the audio at audio_path and generate a quiz from it.

    audio_path = local path to the downloaded audio file
    transcr = text transcript of the audio, produced by transcript()
    from_gemin_json = raw JSON string produced by gemini(), built from transcr
    returns = from_gemin_json (title, description, questions)
    """
    
    transcr = transcript(audio_path)
    from_gemin_json = gemini(transcr)
    return from_gemin_json
    