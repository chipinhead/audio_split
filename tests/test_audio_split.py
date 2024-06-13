import unittest
import subprocess
import os
from pydub import AudioSegment
from unittest.mock import patch

class TestAudioSplit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a small MP3 file for testing
        cls.test_audio_path = 'test_audio.mp3'
        silent_segment = AudioSegment.silent(duration=10000)  # 10 seconds of silence
        silent_segment.export(cls.test_audio_path, format="mp3")

    @classmethod
    def tearDownClass(cls):
        # Remove the test MP3 file after tests
        if os.path.exists(cls.test_audio_path):
            os.remove(cls.test_audio_path)

    def test_file_not_found(self):
        result = subprocess.run(['python3', 'audio_split.py', 'non_existent_file.mp3'], capture_output=True, text=True)
        self.assertIn("Input file not found", result.stdout)

    def test_invalid_file_format(self):
        # Create a temporary text file
        with open("temp.txt", "w") as f:
            f.write("This is a test file.")
        
        result = subprocess.run(['python3', 'audio_split.py', 'temp.txt'], capture_output=True, text=True)
        self.assertIn("Invalid input file format", result.stdout)
        
        os.remove("temp.txt")

    def test_valid_audio_file_default_parameters(self):
        result = subprocess.run(['python3', 'audio_split.py', self.test_audio_path], capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        self.assertIn(f"Input file path: {self.test_audio_path}", result.stdout)
        self.assertIn("Silence threshold: -50", result.stdout)
        self.assertIn("Minimum silence duration: 1000", result.stdout)
        self.assertIn("Chunk size: 100", result.stdout)
        self.assertIn("Output format: wav", result.stdout)
        self.assertIn("Song Report:", result.stdout)

    def test_invalid_silence_threshold(self):
        result = subprocess.run(['python3', 'audio_split.py', self.test_audio_path, '--silence_threshold', 'invalid_threshold'], capture_output=True, text=True)
        self.assertIn("argument --silence_threshold: invalid float value: 'invalid_threshold'", result.stderr)
    
    def test_invalid_min_silence_duration(self):
        result = subprocess.run(['python3', 'audio_split.py', self.test_audio_path, '--min_silence_duration', 'invalid_duration'], capture_output=True, text=True)
        self.assertIn("argument --min_silence_duration: invalid int value: 'invalid_duration'", result.stderr)

    def test_invalid_chunk_size(self):
        result = subprocess.run(['python3', 'audio_split.py', self.test_audio_path, '--chunk_size', 'invalid_chunk_size'], capture_output=True, text=True)
        self.assertIn("argument --chunk_size: invalid int value: 'invalid_chunk_size'", result.stderr)

    def test_invalid_output_format(self):
        result = subprocess.run(['python3', 'audio_split.py', self.test_audio_path, '--output_format', 'invalid_format'], capture_output=True, text=True)
        self.assertIn("argument --output_format: invalid choice: 'invalid_format'", result.stderr)

if __name__ == '__main__':
    unittest.main()