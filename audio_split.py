import os
import sys
import mimetypes
import argparse

def is_valid_audio_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('audio')

def main():
    parser = argparse.ArgumentParser(description='Split a long audio file into individual songs.')
    parser.add_argument('input_file', type=str, help='Path to the long audio file.')
    parser.add_argument('--silence_threshold', type=float, default=-50, help='Threshold below which is considered silence.')
    
    args = parser.parse_args()
    
    audio_file_path = args.input_file
    silence_threshold = args.silence_threshold
    
    if not os.path.isfile(audio_file_path):
        print("Input file not found")
        sys.exit(1)
    
    if not is_valid_audio_file(audio_file_path):
        print("Invalid input file format")
        sys.exit(1)
    
    print(f"Input file path: {audio_file_path}")
    print(f"Silence threshold: {silence_threshold}")

if __name__ == "__main__":
    main()