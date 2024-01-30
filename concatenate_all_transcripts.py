import os

def read_files_from_directory(directory):
    aggregated_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                aggregated_text += file.read() + " "
    return aggregated_text