import argparse
import os
import glob
import re

import eyed3
from pydub import AudioSegment
from unidecode import unidecode


def get_mp3_files_in_folder(folder_path):
    mp3_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp3") or file.endswith(".m4a"):
                mp3_files.append(os.path.join(root, file))
                
    return mp3_files


def convert_m4a_to_mp3(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="m4a")
    audio.export(output_path, format="mp3")
    
    # Check if the new .mp3 file was successfully created
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        # Delete the old .m4a file
        os.remove(input_path)
        print(f"Old file '{input_path}' deleted.")
    else:
        print("Conversion failed or new file is empty.")    
    
    return output_path

def change_extension(input_path, new_extension):
    root, old_extension = os.path.splitext(input_path)
    new_path = root + new_extension
    
    return new_path


def main():
    parser = argparse.ArgumentParser(description="Process author and album information")
    parser.add_argument("author", help="Name of the author/artist")
    parser.add_argument("--album", help="Name of the album (optional)")

    args = parser.parse_args()

    print(f"Author: {args.author}")
    author = args.author
    if args.album:
        print(f"Album: {args.album}")
        album = args.album
        
    current_folder = os.getcwd()
    mp3_files_list = get_mp3_files_in_folder(current_folder)
    
    for mp3_file in mp3_files_list:
        print(mp3_file)
        if mp3_file.endswith(".m4a"):
            print("changing format to .mp3")
            output_path = change_extension(mp3_file, ".mp3")
            #os.rename(mp3_file, output_path)
            mp3_file = convert_m4a_to_mp3(mp3_file, output_path)
        
        
        audiofile = eyed3.load(mp3_file)

        if not audiofile.tag:
            audiofile.initTag()
            
        audiofile.tag.artist = author
        if args.album:
            audiofile.tag.album = album
        
        try:
            audiofile.tag.save()
        except Exception as e:
            print(e)
        #print(audiofile.tag.artist)
        #print(audiofile.tag.album)

if __name__ == "__main__":
    main()