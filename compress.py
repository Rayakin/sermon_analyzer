from pydub import AudioSegment
import os
import re
from audio_utilities import get_file_size, get_mp3_length

def compress_audio(input_file_path, output_file_path, target_bitrate="64k"):
    audio = AudioSegment.from_file(input_file_path)
    # Export with reduced bitrate
    audio.export(output_file_path, format="mp3", bitrate=target_bitrate)

def compress_all_mp3_in_directory(directory, target_bitrate="64k"):
    try:
        for filename in os.listdir(directory):
            target_bitrate = "64k"
            if not filename.endswith(".mp3"):
                continue
            file_size = get_file_size(f"./{directory}/{filename}")
            size_in_mb = file_size / (1024**2)
            audio_length = get_mp3_length(f"./{directory}/{filename}")
            # Estimated file size = (Bitrate (in kbps) × Length of Audio (in seconds)) / 8
            estimated_compressed_size = ((64 * audio_length) / 8) / (1024**2)
            output_filename = f"compressed_{filename}" if not filename.startswith("compressed_") else filename
            input_file_path = os.path.join(directory, filename)
            output_file_path = os.path.join(directory, output_filename)
            if size_in_mb > 25:
                if estimated_compressed_size > 25:
                    target_bitrate = "32k"
                compress_audio(input_file_path, output_file_path, target_bitrate)
                print(f"Compressed: {filename}")
            else:
                print(f"This one didn't need to be compressed: {filename}")
                continue

    except Exception as e:
        print(e)

# Usage
directory = "mp3s"
compress_all_mp3_in_directory(directory)
