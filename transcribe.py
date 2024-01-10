from openai import OpenAI
import os
import re
from get_existing_trackIds import get_existing_trackIds
client = OpenAI()

def get_transcript(input_file):
    audio_file = open(input_file, "rb")
    try: 
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    except Exception as e:
        print(e)
        return False
    transcription_text = transcript.text
    return transcription_text

def get_all_transcripts_in_directory(directory):
    retrieved_trackIds = get_existing_trackIds("transcripts2")
    try:
        for filename in os.listdir(directory):
            if not filename.startswith("compressed_"):
                continue
            if not filename.endswith(".mp3"):
                continue
            print(filename)
            trackId_match = re.search(r"(?:compressed_)?(\d+)--", filename)
            if trackId_match:
                trackId = trackId_match.group(1)
                print(trackId)
                if trackId in retrieved_trackIds:
                    print('Already got this one')
                    continue
                input_file_path = os.path.join(directory, filename)
                output_file_path = os.path.join("transcripts", trackId)
                
                transcript = get_transcript(input_file_path)
                if transcript == False:
                    continue
                print(f"Transcripted: {filename}")
                with open(output_file_path, 'w') as file:
                    file.write(f"{transcript}.txt")
    except Exception as e:
        print(e)

get_all_transcripts_in_directory('mp3s2')