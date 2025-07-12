# BPMSort

A Python application for automatically analyzing and organizing music files by their BPM (Beats Per Minute) values. The program detects the tempo of audio files and sorts them into folders based on their BPM, making it easier to organize music collections for DJs, musicians, and music enthusiasts.

## Features

- **Automatic BPM Detection**: Uses librosa library for accurate tempo analysis
- **Smart Folder Organization**: Creates organized folder structure with BPM-named directories
- **Configurable Settings**: Customizable via `settings.py` for folder names, behavior, and output options
- **Batch Processing**: Processes entire folders of music files at once
- **Cross-Platform Support**: Windows-optimized version with Linux compatibility
- **Duplicate Handling**: Prevents overwriting files that already exist in destination folders
- **Multiple Audio Format Support**: Works with various audio file formats supported by librosa
- **Flexible File Operations**: Choose between copying or moving files
- **BPM Range Grouping**: Optional feature to group files by BPM ranges instead of exact values
- **Verbose Output**: Detailed processing information and progress tracking

## Requirements

- Python 3.8+
- librosa (for audio processing)
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/BPMSort.git
   cd BPMSort
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install librosa
   ```

## Usage

### Method 1: Using the main entry point
```bash
python main.py
```
This will prompt you to enter the path to your music folder.

### Method 2: Direct usage
```python
from bpm_win import folder_request
folder_request()
```

### Method 3: Programmatic usage
```python
from bpm_win import bpm_win
bpm_win("path/to/your/music/folder")
```

## Configuration

The application can be customized by modifying the `settings.py` file. Key configuration options include:

### Directory Settings
- `OUTPUT_FOLDER_NAME`: Name of the main output folder (default: "BPMSorted")
- `BPM_FOLDER_TEMPLATE`: Template for BPM-specific folder names (default: "{bpm} BPM Songs")
- `DEFAULT_INPUT_FOLDER`: Default folder to process if none specified

### Audio Processing Settings
- `DEFAULT_BPM`: BPM value to use if detection fails (default: 120)
- `SUPPORTED_AUDIO_EXTENSIONS`: List of supported audio file extensions

### Behavior Settings
- `COPY_FILES`: Whether to copy (True) or move (False) files (default: True)
- `SKIP_EXISTING_FILES`: Skip files that already exist in destination (default: True)
- `USE_BPM_RANGES`: Group files by BPM ranges instead of exact values (default: False)

### Display Settings
- `VERBOSE_OUTPUT`: Show detailed processing information (default: True)
- `SHOW_BPM_DETECTION`: Display BPM detection results (default: True)
- `SHOW_FILE_OPERATIONS`: Show file copy/move operations (default: True)

### Example Configuration
```python
# settings.py
OUTPUT_FOLDER_NAME = "MyMusicLibrary"
BPM_FOLDER_TEMPLATE = "Tempo_{bpm}"
COPY_FILES = False  # Move files instead of copying
USE_BPM_RANGES = True  # Group by ranges like "Fast (121-150 BPM)"
VERBOSE_OUTPUT = False  # Quiet mode
```

## How It Works

1. **Input**: You provide a folder path containing music files
2. **Configuration**: The program reads settings from `settings.py` for customization
3. **Analysis**: The program analyzes each audio file to detect its BPM using librosa's beat tracking algorithm
4. **Organization**: Creates a folder structure like:
   ```
   BPMSorted/
   ├── 120 BPM Songs/
   │   ├── song1.mp3
   │   └── song2.wav
   ├── 128 BPM Songs/
   │   ├── song3.mp3
   │   └── song4.flac
   └── 140 BPM Songs/
       └── song5.mp3
   ```
5. **File Operations**: Files are copied or moved based on your settings configuration

## File Structure

- `main.py` - Main entry point for the application
- `bpm_win.py` - Windows-optimized BPM detection and sorting logic
- `settings.py` - Configuration file for customizing application behavior
- `BPM.py` - Legacy version using Essentia library
- `README.md` - This documentation file
- `requirements.txt` - Python dependencies
- `LICENSE` - License information

## Classes and Methods

### BpmFolders Class
The main class that handles BPM analysis and file organization.

#### Methods:
- `get_bpm()` - Analyzes audio file and extracts BPM value
- `make_dir()` - Creates directory structure for BPM organization
- `move_music_file()` - Copies files to appropriate BPM folders

### Utility Functions:
- `bpm_read_folder()` - Processes all files in a target directory
- `review_target_folder()` - Validates that the target folder contains files
- `bpm_win()` - Main processing function
- `folder_request()` - Interactive folder selection

## Supported Audio Formats

The application supports various audio formats through librosa:
- WAV
- MP3
- FLAC
- M4A
- OGG
- And more...

## Example Output

```
BPM Sort - Music File Organizer
========================================

Current Settings:
BPM Sort Configuration:
- Output Folder: BPMSorted
- BPM Folder Template: {bpm} BPM Songs
- Default BPM: 120
- Copy Files: True
- Skip Existing: True
- Use BPM Ranges: False
- Verbose Output: True
- Supported Extensions: .mp3, .wav, .flac, .m4a, .aac, .ogg, .wma, .aiff, .au, .mp4, .3gp
========================================
Please enter the path to the music folder: C:\Music\MyCollection
Starting BPM Sort process...
Target folder: C:\Music\MyCollection
Output folder: BPMSorted
Copy files: True
Skip existing: True
--------------------------------------------------
Processing folder: C:\Music\MyCollection
Detected BPM: 120.0
Created output folder: C:\Users\User\BPMSorted
Created BPM folder: C:\Users\User\BPMSorted\120 BPM Songs
song1.mp3 copied to 120 BPM Folder
Detected BPM: 128.0
Created BPM folder: C:\Users\User\BPMSorted\128 BPM Songs
song2.wav copied to 128 BPM Folder

Processing complete:
- Files processed: 2
- Files skipped: 0
BPM Sort process completed!
```

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'librosa'**
   - Solution: Install librosa using `pip install librosa`

2. **Empty folder error**
   - Solution: Ensure your target folder contains audio files

3. **Permission errors**
   - Solution: Run with appropriate permissions or choose a different output location

## Version History

- **Current Version**: Windows-optimized version using librosa
- **Legacy Version**: Uses Essentia library (see `BPM.py`)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the terms specified in the LICENSE file.

## Notes

- The program creates copies of files rather than moving them to preserve your original collection
- BPM values are rounded to the nearest whole number for folder organization
- The application is optimized for Windows but should work on other platforms with minor modifications

---

*Updates and changes made by jade-spector are marked throughout the codebase for tracking modifications.*