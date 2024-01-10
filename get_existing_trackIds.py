import os
import re

def get_existing_trackIds(directory):
    all_sermons_compressed = []
    try:
        for filename in os.listdir(directory):
            trackId_match = re.search(r"^compressed_(\d+)--", filename)
            if trackId_match:
                trackId = trackId_match.group(1)
                print(trackId)
                all_sermons_compressed.append(trackId)
            else:
                print("No ID found")
        return all_sermons_compressed
    except Exception as e:
        print(e)