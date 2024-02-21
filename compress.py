from pydub import AudioSegment
import os
import re
from audio_utilities import get_file_size, get_mp3_length

def compress_audio(input_file_path, output_file_path, target_bitrate="64k"):
    try:
        audio = AudioSegment.from_file(input_file_path)
        # Export with reduced bitrate
        audio.export(output_file_path, format="mp3", bitrate=target_bitrate)
        return True
    except Exception as e:
        print(e)
        return False

def calculate_bitrate(audio_length_seconds, target_size_mb=24):
    """
    Calculate the maximum bitrate to ensure the compressed file is under the target size.
    
    :param audio_length_seconds: Length of the audio in seconds
    :param target_size_mb: Target file size in MB
    :return: Maximum bitrate in kbps
    """
    # Convert target size from MB to KB (1 MB = 1024 KB)
    target_size_kb = target_size_mb * 1024
    print("This is what the bitrate calculator is using:")
    print(target_size_kb, audio_length_seconds)
    # Calculate maximum bitrate in kbps
    max_bitrate_kbps = (target_size_kb * 8) // audio_length_seconds  # Note: This already gives kbps
    
    return int(max_bitrate_kbps)

def compress_mp3(filepath, target_bitrate="64k"):
    try:
        file_size = get_file_size(filepath)
        size_in_mb = file_size / (1024**2)
        audio_length = get_mp3_length(filepath)
        # Estimated file size = (Bitrate (in kbps) × Length of Audio (in seconds)) / 8
        match = re.search(r"mp3s/(\w+)(\.mp3)?$", filepath)
        if match:
            filename = match.group(1)
        else: 
            print("No match found")
        print(f"This is what the filename looks like it should be: {filename}")
        output_filename = f"compressed_{filename}.mp3"
        output_file_path = os.path.join("mp3s", output_filename)
        if size_in_mb > 25:
            # print("This file is > 25MB and needs a smaller bitrate")
            # estimated_compressed_size = (64 * (audio_length / 1000)) / (8 * 1024)
            # print(f"This is the estimated size at the 64 bitrate: {estimated_compressed_size}")
            target_bitrate = f"{calculate_bitrate((audio_length/1000))}k"
            print(f"This is the bitrate: {target_bitrate}")
            compress_success = compress_audio(filepath, output_file_path, target_bitrate)
            print(f"Was the compression succesful?: {compress_success}")
            if compress_success:    
                print(f"Compressed: {filename}")
                return output_file_path
            else:
                return False
        else:
            print(f"This one didn't need to be compressed: {filename}")
            return filepath
    except Exception as e:
        print(e)

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