import os

def append_png_extension(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file_name in files:
            file_path = os.path.join(subdir, file_name)
            new_file_path = file_path + '.png'
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_path} to {new_file_path}")

# Provide the root directory path here
root_directory = "C:/Users/Felicia/Desktop/storedatascrape/storedatascraping/StoreData/images/WOMEN - Copy"
append_png_extension(root_directory)
