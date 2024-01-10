from pydub import AudioSegment
import os
import re
from get_existing_trackIds import get_existing_trackIds

def compress_audio(input_file_path, output_file_path, target_bitrate="32k"):
    # Load audio file
    audio = AudioSegment.from_file(input_file_path)

    # Export with reduced bitrate
    audio.export(output_file_path, format="mp3", bitrate=target_bitrate)

def compress_all_mp3_in_directory(directory, target_bitrate="32k"):
    retrieved_trackIds = get_existing_trackIds(directory)
    print(retrieved_trackIds)
    # try:
    #     for filename in os.listdir(directory):
    #         print(filename)
    #         trackId_match = re.search(r"^compressed_(\d+)--", filename)
    #         if trackId_match:
    #             trackId = trackId_match.group(1)
    #             print(trackId)
    #             if trackId in retrieved_trackIds:
    #                 print('Already got this one')
    #                 continue
    #             if filename.endswith(".mp3"):
    #                 input_file_path = os.path.join(directory, filename)
    #                 output_file_path = os.path.join(directory, f"compressed_{filename}")
    #             compress_audio(input_file_path, output_file_path, target_bitrate)
    #             print(f"Compressed: {filename}")
    # except Exception as e:
    #     print(e)
    try:
        for filename in os.listdir(directory):
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

                output_filename = f"compressed_{filename}" if not filename.startswith("compressed_") else filename
                input_file_path = os.path.join(directory, filename)
                output_file_path = os.path.join(directory, output_filename)
                
                compress_audio(input_file_path, output_file_path, target_bitrate)
                print(f"Compressed: {filename}")
            else:
                print("Couldn't get an id.")

    except Exception as e:
        print(e)

# Usage
directory = "mp3s2"
compress_all_mp3_in_directory(directory)
