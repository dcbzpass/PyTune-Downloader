# PyTune Downloader 🎵

A simple, lightweight Python CLI tool that downloads audio from YouTube and automatically converts it to high-quality MP3 format.

## Features
- 🚀 **Fast Download**: Uses `yt-dlp` for reliable high-speed downloads.
- 🎧 **Auto-Conversion**: Automatically extracts audio and converts it to MP3 (320kbps).
- 📂 **Custom Save**: Prompts you for a save location (defaults to Documents if skipped).
- ⏯️ **Auto-Play**: Automatically opens the file after download.

## Requirements
Before running the script, ensure you have the following installed on your PC:

1. **Python 3.x**: [Download Python](https://www.python.org/downloads/)
2. **FFmpeg**: Required for audio conversion.
   - **Windows**: [Download build](https://gyan.dev/ffmpeg/builds/), extract it, and add the `bin` folder to your System PATH variables.
   - **Linux**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`

## Installation

1. Clone this repository or download the `main.py` file.
2. Install the required Python package:
   ```bash
   pip install yt-dlp
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. Paste the YouTube URL when prompted.
3. Choose a folder to save the file (or press Enter to save to your default Documents folder).

## License
[MIT](https://choosealicense.com/licenses/mit/)
