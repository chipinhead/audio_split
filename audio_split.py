import os
import sys
import mimetypes
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import timedelta

def is_valid_audio_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('audio')

def format_time(milliseconds):
    return str(timedelta(milliseconds=milliseconds))

def main():
    parser = argparse.ArgumentParser(description='Split a long audio file into individual songs.')
    parser.add_argument('input_file', type=str, help='Path to the long audio file.')
    parser.add_argument('--silence_threshold', type=float, default=-50, help='Threshold below which is considered silence.')
    parser.add_argument('--min_silence_duration', type=int, default=1000, help='Minimum duration of silence (in milliseconds) to be considered a break between songs.')
    parser.add_argument('--chunk_size', type=int, default=100, help='Chunk size (in milliseconds) for analysis when scanning for silence.')
    parser.add_argument('--output_format', type=str, choices=['wav', 'mp3', 'ogg'], default='wav', help='Output file format for individual audio files.')

    args = parser.parse_args()
    
    audio_file_path = args.input_file
    silence_threshold = args.silence_threshold
    min_silence_duration = args.min_silence_duration
    chunk_size = args.chunk_size
    output_format = args.output_format

    print(f"Checking if file exists: {audio_file_path}")
    
    if not os.path.isfile(audio_file_path):
        print("Input file not found")
        sys.exit(1)
    
    print(f"Checking if valid audio file: {audio_file_path}")
    
    if not is_valid_audio_file(audio_file_path):
        print("Invalid input file format")
        sys.exit(1)
    
    print(f"Input file path: {audio_file_path}")
    print(f"Silence threshold: {silence_threshold}")
    print(f"Minimum silence duration: {min_silence_duration}")
    print(f"Chunk size: {chunk_size}")
    print(f"Output format: {output_format}")

    # Load audio file
    audio = AudioSegment.from_file(audio_file_path)
    
    print(f"Audio length: {len(audio)} milliseconds")
    
    # Split on silence
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_duration,
        silence_thresh=silence_threshold
    )

    # Generate report
    report = []
    current_time = 0
    for i, chunk in enumerate(chunks):
        start_time = current_time
        end_time = start_time + len(chunk)
        duration = len(chunk)
        report.append({
            'song': i + 1,
            'start': format_time(start_time),
            'end': format_time(end_time),
            'duration': format_time(duration)
        })
        print(f"Chunk {i+1}: Start = {start_time}ms, End = {end_time}ms, Duration = {duration}ms")  # Intermediate log
        current_time = end_time

    print("\nSong Report:")
    for song in report:
        print(f"Song {song['song']}: Start = {song['start']}, End = {song['end']}, Duration = {song['duration']}")
    
    # Save chunks
    for i, chunk in enumerate(chunks):
        output_file = f"{os.path.splitext(audio_file_path)[0]}_chunk_{i + 1}.{output_format}"
        print(f"Exporting chunk {i+1} to {output_file}")
        chunk.export(output_file, format=output_format)

if __name__ == "__main__":
    main()