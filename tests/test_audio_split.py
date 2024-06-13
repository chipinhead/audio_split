import unittest
import subprocess
import os

class TestAudioSplit(unittest.TestCase):
    def test_file_not_found(self):
        result = subprocess.run(['python', 'audio_split.py', 'non_existent_file.mp3'], capture_output=True, text=True)
        self.assertIn("Input file not found", result.stdout)

    def test_invalid_file_format(self):
        # Create a temporary text file
        with open("temp.txt", "w") as f:
            f.write("This is a test file.")
        
        result = subprocess.run(['python', 'audio_split.py', 'temp.txt'], capture_output=True, text=True)
        self.assertIn("Invalid input file format", result.stdout)
        
        os.remove("temp.txt")

    def test_valid_audio_file_default_parameters(self):
        # Ensure you have a valid audio file for this test
        valid_audio_path = 'test_audio.mp3'
        with open(valid_audio_path, 'w') as f:
            f.write("RIFF....WAVEfmt ")  # Mocking a minimal WAV file header
        
        result = subprocess.run(['python', 'audio_split.py', valid_audio_path], capture_output=True, text=True)
        self.assertIn(f"Input file path: {valid_audio_path}", result.stdout)
        self.assertIn("Silence threshold: -50", result.stdout)
        self.assertIn("Minimum silence duration: 1000", result.stdout)
        self.assertIn("Chunk size: 100", result.stdout)
        
        os.remove(valid_audio_path)

    def test_valid_audio_file_custom_parameters(self):
        # Ensure you have a valid audio file for this test
        valid_audio_path = 'test_audio.mp3'
        with open(valid_audio_path, 'w') as f:
            f.write("RIFF....WAVEfmt ")  # Mocking a minimal WAV file header
        
        result = subprocess.run(['python', 'audio_split.py', valid_audio_path, '--silence_threshold', '-30', '--min_silence_duration', '1500', '--chunk_size', '200'], capture_output=True, text=True)
        self.assertIn(f"Input file path: {valid_audio_path}", result.stdout)
        self.assertIn("Silence threshold: -30", result.stdout)
        self.assertIn("Minimum silence duration: 1500", result.stdout)
        self.assertIn("Chunk size: 200", result.stdout)
        
        os.remove(valid_audio_path)
    
    def test_invalid_silence_threshold(self):
        valid_audio_path = 'test_audio.mp3'
        with open(valid_audio_path, 'w') as f:
            f.write("RIFF....WAVEfmt ")  # Mocking a minimal WAV file header
        
        result = subprocess.run(['python', 'audio_split.py', valid_audio_path, '--silence_threshold', 'invalid_threshold'], capture_output=True, text=True)
        self.assertIn("argument --silence_threshold: invalid float value: 'invalid_threshold'", result.stderr)
        
        os.remove(valid_audio_path)
    
    def test_invalid_min_silence_duration(self):
        valid_audio_path = 'test_audio.mp3'
        with open(valid_audio_path, 'w') as f:
            f.write("RIFF....WAVEfmt ")  # Mocking a minimal WAV file header
        
        result = subprocess.run(['python', 'audio_split.py', valid_audio_path, '--min_silence_duration', 'invalid_duration'], capture_output=True, text=True)
        self.assertIn("argument --min_silence_duration: invalid int value: 'invalid_duration'", result.stderr)
        
        os.remove(valid_audio_path)

    def test_invalid_chunk_size(self):
        valid_audio_path = 'test_audio.mp3'
        with open(valid_audio_path, 'w') as f:
            f.write("RIFF....WAVEfmt ")  # Mocking a minimal WAV file header
        
        result = subprocess.run(['python', 'audio_split.py', valid_audio_path, '--chunk_size', 'invalid_chunk_size'], capture_output=True, text=True)
        self.assertIn("argument --chunk_size: invalid int value: 'invalid_chunk_size'", result.stderr)
        
        os.remove(valid_audio_path)

if __name__ == '__main__':
    unittest.main()