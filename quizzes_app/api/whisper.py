import whisper

def transcript(path):
    model = whisper.load_model("turbo")
    result = model.transcribe(path)
    return result["text"]