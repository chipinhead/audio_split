
# Audio Splitter User Stories

## Initial Project Description:
We are creating a script that takes a long audio file containing several songs and splits it into several audio files, one for each song in the original. The name of this project is "audio_split".

## User Stories:

### User Story 1:
As an audio split user, I should be able to provide a path to a long audio file as input via the command line. Having provided a path as a command line parameter I should see the name of the path printed in the output of my terminal.

### User Story 2:
As an audio split user, I should be able to provide an optional parameter, "silence_threshold" which specifies the threshold below which is considered silence. If not provided the value should default to -50. When running the audio split script, I should see the silence_threshold setting printed in my terminal.

### User Story 3:
As an audio split user, I should be able to provide an optional named parameter, "min_silence_duration" which specifies the minimum duration (in milliseconds) a span of silence must be, in order for it to be considered a break between songs. The default value should be 1000. When running the audio split script, I should see the min_silence_duration setting printed in my terminal.

### User Story 4:
As an audio split user, I should be able to provide an optional named parameter, "chunk_size" which specifies the Chunk size (in milliseconds) for analysis when scanning for silence in the audio file. The default value should be 100. When running the audio split script, I should see the chunk_size setting printed in my terminal.

### User Story 5:
As an audio split user, I should be able to provide an optional named parameter, "output_format" which specifies the file format of the individual audio files. The choices are 'wav', 'mp3', 'ogg'. When running the audio split script, I should see the output_format setting printed in my terminal.

### User Story 6:
As an audio split user, Given I have provided a path to a long audio file, and may have provided optional parameters, I should see a report printed in the terminal that tells me the beginning, end and duration of each song in the file. I should see the beginning, end, and duration in "HH:mm:ss" format.

### User Story 7:
As an audio split user, Given I have run the script with an input file and may have provided parameters, I should see one audio file created per song found in the input audio file. I should see that each audio file has the same name as the input file, with the chunk number appended. I should see tracks with a chunk number of 1 digit have a "0" prepended to their chunk number. Examples: Input: audio.wav, Chunk 1: audio01.wav, Chunk 10: audio10.wav.
