import os
from pydub import AudioSegment

def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    try:
        size = os.path.getsize(file_path)
        return size
    except OSError as e:
        print(f"Error: {e}")
        return None

def get_mp3_length(file_path):
    """Returns the length of an MP3 file in seconds."""
    audio = AudioSegment.from_file(file_path)
    return len(audio)  # Duration in milliseconds, to convert to seconds divide by 1000