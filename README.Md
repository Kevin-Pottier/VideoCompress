# CompressMovie

>This repository contains a simple Python script to compress video files to a target size using FFmpeg.

## Features
- Select a video file via a GUI dialog (supports .mp4, .mkv, .avi)
- Choose output container (MP4 or MKV)
- Enter the maximum output file size (in GB) via a dialog
- Automatically calculates the required video bitrate for your target size
- Generates and runs a batch file for compression
- Cleans up after compression

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
1. Run `CompressMovie.py` with Python 3.
2. Select your video file in the dialog.
3. Choose the output format (MP4 or MKV).
4. Enter the maximum output file size (in GB) when prompted.
5. The script will generate and run a batch file to compress your video to the target size.
6. The batch file is deleted after successful compression.

- Only `.py`, `.gitignore`, and `README.Md` are tracked by git (see `.gitignore`).
- All other files (videos, batch files, outputs) are ignored by git.

## Troubleshooting

- Only third-party packages (like `colorama`) are listed in `requirements.txt`. Standard Python libraries such as `os`, `subprocess`, and `tkinter` are included with every Python installation and do not need to be installed separately. If you encounter errors about missing standard libraries, your Python installation may be broken—reinstall Python from the official website to fix this.

---
Feel free to modify the script for your own needs!
