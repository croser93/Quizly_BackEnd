import json
import yt_dlp

URL = 'https://www.youtube.com/watch?v=i3a7B65b6w8'

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = { 
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    print(json.dumps(ydl.sanitize_info(info)))