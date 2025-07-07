# CompressMovie

>This repository contains a simple Python script to compress video files to a target size using FFmpeg.

## Features
- Choose usage mode at launch: Film Compression or Subtitle Translation
- For Film Compression:
  - Select a video file via a GUI dialog (supports .mp4, .mkv, .avi)
  - Choose subtitle options via a dedicated dialog: no subtitles, softcode (attach .srt), or hardcode (burn in). If you select a subtitle option but do not choose a file, you will be prompted again.
  - Choose output container (MP4 or MKV) via a dialog
  - Enter the maximum output file size (in GB) via a dialog
  - Uses relative subtitle paths for better FFmpeg compatibility
  - Automatically calculates the required video bitrate for your target size
  - Runs FFmpeg directly (no batch file needed)
  - Shows the FFmpeg command used
- For Subtitle Translation:
  - Select a subtitle file to translate via a dialog
  - (Translation logic placeholder: currently just prints the selected file)

## Requirements
- Python 3
- FFmpeg and FFprobe installed and available in your system PATH
- Python packages listed in `requirements.txt`
- `colorama` (optional, for colored terminal output)

All required Python packages can be installed with:

```bash
pip install -r requirements.txt
```

## Usage
1. Run the script:
   `python CompressMovie.py`
2. Choose the usage mode:
   - **Film Compression**: Compress a video file with optional subtitles.
   - **Subtitle Translation**: Select a subtitle file for translation (feature placeholder).
3. Follow the dialogs for your chosen mode:
   - For Film Compression:
     - Select a video file.
     - Choose subtitle options (none, softcode, hardcode). If you select softcode or hardcode, you must also select a subtitle file.
     - Choose the output container (MP4 or MKV).
     - Enter the maximum output file size (in GB).
     - The script will extract video/audio metadata, calculate the required video bitrate, and run FFmpeg to compress the video.
     - The output video will be created in the same folder as the original.
   - For Subtitle Translation:
     - Select a subtitle file. (Translation logic not yet implemented.)

- Only `.py`, `.gitignore`, and `README.Md` are tracked by git (see `.gitignore`).
- All other files (videos, batch files, outputs) are ignored by git.

## Troubleshooting

- Only third-party packages (like `colorama`) are listed in `requirements.txt`. Standard Python libraries such as `os`, `subprocess`, and `tkinter` are included with every Python installation and do not need to be installed separately. If you encounter errors about missing standard libraries, your Python installation may be broken—reinstall Python from the official website to fix this.

---
Feel free to modify the script for your own needs!
