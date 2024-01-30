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
            prompt="Hello, thank you for listening to my sermon today.",
            language="en",
            file=audio_file
        )
    except Exception as e:
        print(e)
        return False
    transcription_text = transcript.text
    return transcription_text

def get_all_transcripts_in_directory(directory):
    try:
        for filename in os.listdir(directory):
            if not filename.startswith("compressed_"):
                continue
            if not filename.endswith(".mp3"):
                continue
            trackId_match = re.search(r"(?:compressed_)?(\d+)", filename)
            if trackId_match:
                trackId = trackId_match.group(1)
                print(trackId)
                input_file_path = os.path.join(directory, filename)
                output_file_path = f"transcripts/New/{trackId}.txt"
                
                transcript = get_transcript(input_file_path)
                if transcript == False:
                    continue
                print(f"Transcripted: {filename}")
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(transcript)
    except Exception as e:
        print(e)

get_all_transcripts_in_directory('mp3s/Ready')
        
# text = get_transcript('mp3s/compressed_1000611933131--The Power of Weakness (II Cor 11:1-12:10) (Part 14).mp3')
# print(text)