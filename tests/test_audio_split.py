import unittest
import subprocess
import os
from pydub import AudioSegment
from pydub.generators import Sine

class TestAudioSplit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test MP3 file with 1s silence, 2s tone, 1s silence, 2s tone, 1s silence
        cls.test_audio_path = 'test_audio.mp3'
        silent_segment = AudioSegment.silent(duration=1000)  # 1 second of silence
        tone_segment = Sine(440).to_audio_segment(duration=2000)  # 2 seconds of tone
        audio = silent_segment + tone_segment + silent_segment + tone_segment + silent_segment
        audio.export(cls.test_audio_path, format="mp3")

        # Verify the file can be opened and played
        try:
            audio = AudioSegment.from_file(cls.test_audio_path)
        except Exception as e:
            raise RuntimeError(f"Error opening test audio file: {e}")

    @classmethod
    def tearDownClass(cls):
        # Remove the test MP3 file and any generated chunks after tests
        if os.path.exists(cls.test_audio_path):
            os.remove(cls.test_audio_path)
        for i in range(1, 21):  # Assuming a max of 20 chunks for cleanup
            for fmt in ['wav', 'mp3', 'ogg']:
                chunk_file = f"test_audio{i:02}.{fmt}"
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)

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

        self.assertIn("Song Report:", result.stdout)
        self.assertTrue(os.path.exists('test_audio01.wav'))
        self.assertTrue(os.path.exists('test_audio02.wav'))

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