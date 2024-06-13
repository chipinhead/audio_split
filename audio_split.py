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
    parser.add_argument('--min_silence_duration', type=int, default=1000, help='Minimum duration of silence (in milliseconds) to be considered a break between songs.')
    parser.add_argument('--chunk_size', type=int, default=100, help='Chunk size (in milliseconds) for analysis when scanning for silence.')
    
    args = parser.parse_args()
    
    audio_file_path = args.input_file
    silence_threshold = args.silence_threshold
    min_silence_duration = args.min_silence_duration
    chunk_size = args.chunk_size
    
    if not os.path.isfile(audio_file_path):
        print("Input file not found")
        sys.exit(1)
    
    if not is_valid_audio_file(audio_file_path):
        print("Invalid input file format")
        sys.exit(1)
    
    print(f"Input file path: {audio_file_path}")
    print(f"Silence threshold: {silence_threshold}")
    print(f"Minimum silence duration: {min_silence_duration}")
    print(f"Chunk size: {chunk_size}")

if __name__ == "__main__":
    main()