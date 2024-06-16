
# Audio Splitter

Audio Splitter is a Python script that splits a long audio file containing several songs into individual audio files for each song. The script detects silent intervals between songs to perform the split.

## Installation

### Prerequisites
Make sure you have the following installed on your system:
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
  - After installing Docker, ensure it is running on your machine.

### Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build the Docker image**:
    ```sh
    docker-compose build
    ```

3. **Start the Docker container**:
    ```sh
    docker-compose up -d
    ```

4. **Access the running container**:
    ```sh
    docker-compose exec app bash
    ```

You are now inside the Docker container where you can run the script and tests.

## Usage

To split a long audio file into individual songs, you need to run the script with the necessary parameters.

### Running the Script

Inside the Docker container, run the following command:

```sh
python audio_split.py <path_to_audio_file> [options]
```

Replace `<path_to_audio_file>` with the path to your long audio file.

### Example Command

```sh
python audio_split.py input_audio.mp3 --silence_threshold -50 --min_silence_duration 1000 --chunk_size 100 --output_format wav
```

This command will split `input_audio.mp3` into separate files for each song, based on the silent intervals.

### Command-Line Options

- `--silence_threshold`: Set the threshold below which is considered silence. Default is `-50`.
- `--min_silence_duration`: Set the minimum duration (in milliseconds) of silence to be considered a break between songs. Default is `1000`.
- `--chunk_size`: Set the chunk size (in milliseconds) for analysis when scanning for silence. Default is `100`.
- `--output_format`: Set the format of the output files. Options are `wav`, `mp3`, `ogg`. Default is `wav`.

### Viewing the Results

After running the script, the output files will be saved in the same directory as the input file. Each song will be saved as a separate file with names like `input_audio01.wav`, `input_audio02.wav`, etc.

## Testing

To run the tests, use the following command inside the Docker container:

```sh
python -m unittest discover -s tests -v
```

## Configuration

You can customize the behavior of the audio splitter script using the following command-line options:

1. **`input_file`** (required)
   - **Description**: The path to the long audio file you want to split.
   - **Usage**: `python audio_split.py <path_to_audio_file>`
   - **Example**: `python audio_split.py input_audio.mp3`

2. **`--silence_threshold`** (optional)
   - **Description**: The threshold below which is considered silence. This is measured in decibels.
   - **Default**: `-50`
   - **Usage**: `--silence_threshold <threshold_value>`
   - **Example**: `python audio_split.py input_audio.mp3 --silence_threshold -60`

3. **`--min_silence_duration`** (optional)
   - **Description**: The minimum duration (in milliseconds) a span of silence must be to be considered a break between songs.
   - **Default**: `1000` (1 second)
   - **Usage**: `--min_silence_duration <duration_value>`
   - **Example**: `python audio_split.py input_audio.mp3 --min_silence_duration 1500`

4. **`--chunk_size`** (optional)
   - **Description**: The chunk size (in milliseconds) for analysis when scanning for silence in the audio file.
   - **Default**: `100`
   - **Usage**: `--chunk_size <chunk_size_value>`
   - **Example**: `python audio_split.py input_audio.mp3 --chunk_size 200`

5. **`--output_format`** (optional)
   - **Description**: The format of the individual output audio files. Options are `wav`, `mp3`, `ogg`.
   - **Default**: `wav`
   - **Usage**: `--output_format <format>`
   - **Example**: `python audio_split.py input_audio.mp3 --output_format mp3`

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
