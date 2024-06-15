import os
import sys
import mimetypes
import argparse
from pydub import AudioSegment
from pydub.silence import detect_silence
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

    if not os.path.isfile(audio_file_path):
        print("Input file not found")
        sys.exit(1)
    
    if not is_valid_audio_file(audio_file_path):
        print("Invalid input file format")
        sys.exit(1)

    # Load audio file
    audio = AudioSegment.from_file(audio_file_path)
    
    # Detect silence intervals
    silence_intervals = detect_silence(
        audio,
        min_silence_len=min_silence_duration,
        silence_thresh=silence_threshold
    )
    
    # Calculate start and end points
    start_end_points = []
    previous_end = 0
    for start, end in silence_intervals:
        if start != previous_end:
            start_end_points.append((previous_end, start))
        previous_end = end
    if previous_end < len(audio):
        start_end_points.append((previous_end, len(audio)))

    # Generate chunks
    chunks = [audio[start:end] for start, end in start_end_points]

    # Generate report and export chunks
    report = []
    for i, (start, end) in enumerate(start_end_points):
        duration = end - start
        report.append({
            'song': i + 1,
            'start': format_time(start),
            'end': format_time(end),
            'duration': format_time(duration)
        })
        chunk_number = f"{i + 1:02}"
        output_file = f"{os.path.splitext(audio_file_path)[0]}{chunk_number}.{output_format}"
        chunks[i].export(output_file, format=output_format)

    print("\nSong Report:")
    for song in report:
        print(f"Song {song['song']}: Start = {song['start']}, End = {song['end']}, Duration = {song['duration']}")

if __name__ == "__main__":
    main()