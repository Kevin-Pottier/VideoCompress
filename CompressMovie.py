import subprocess
import os
import os.path
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.messagebox as messagebox
from colorama import init, Fore, Style

init()

# === Dependencies ===
# FFmpeg & FFprobe have to be in the PATH
# You can download them from https://ffmpeg.org/download.html
# Make sure to add the bin directory to your PATH environment variable

print(Fore.YELLOW + "Ensure FFmpeg and FFprobe are installed and available in your PATH." + Style.RESET_ALL)
print(Fore.YELLOW + "You can download them from https://ffmpeg.org/download.html\n" + Style.RESET_ALL)

# === Requirements ===
# Python 3.x
# colorama (for colored output in the terminal)
# tkinter (for file dialog)

# === Instructions ===
# 1. Run this script
# 2. Choose a video file
# 3. Choose the output container (MP4 or MKV)
# 4. The script will extract metadata and calculate the target video bitrate
# 5. It will generate a .bat file to compress the video to a maximum size asked to the user
# 6. The .bat file will be executed, and the output video will be created
# 7. The .bat file will be deleted after the compression is done


# === 1) Ask for the video file and subtitle options ===

class SubtitleChoice:
    def __init__(self):
        self.file_path = None
        self.root = tk.Tk()
        self.sub_option = tk.StringVar(master=self.root, value="none")
        self.sub_file = None
        self.root.title("Video and Subtitle Options")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Choose a video file:").pack(pady=5)
        tk.Button(self.root, text="Browse Video", command=self.browse_video).pack(pady=5)
        self.video_label = tk.Label(self.root, text="No file selected.")
        self.video_label.pack(pady=5)

        tk.Label(self.root, text="Subtitle options:").pack(pady=5)
        self.rb_none = tk.Radiobutton(self.root, text="No subtitles", variable=self.sub_option, value="none", command=self.toggle_sub)
        self.rb_soft = tk.Radiobutton(self.root, text="Softcode (attach .srt)", variable=self.sub_option, value="soft", command=self.toggle_sub)
        self.rb_hard = tk.Radiobutton(self.root, text="Hardcode (burn in)", variable=self.sub_option, value="hard", command=self.toggle_sub)
        self.rb_none.pack(anchor="w", padx=40)
        self.rb_soft.pack(anchor="w", padx=40)
        self.rb_hard.pack(anchor="w", padx=40)

        self.sub_button = tk.Button(self.root, text="Choose Subtitle File", command=self.browse_sub, state="disabled")
        self.sub_button.pack(pady=5)
        self.sub_label = tk.Label(self.root, text="No subtitle file selected.")
        self.sub_label.pack(pady=5)

        tk.Button(self.root, text="OK", command=self.root.quit).pack(pady=10)
        self.root.after(100, self.toggle_sub)  # Ensure correct initial state
        self.root.mainloop()
        self.root.destroy()

    def browse_video(self):
        path = filedialog.askopenfilename(title="Choose a video file", filetypes=[("Videos", "*.mp4 *.mkv *.avi")])
        if path:
            self.file_path = path
            self.video_label.config(text=os.path.basename(path))

    def browse_sub(self):
        path = filedialog.askopenfilename(title="Choose subtitle file", filetypes=[("Subtitles", "*.srt *.ass")])
        if path:
            self.sub_file = path
            self.sub_label.config(text=os.path.basename(path))

    def toggle_sub(self, *args):
        if self.sub_option.get() == "none":
            self.sub_button.config(state="disabled")
            self.sub_label.config(text="No subtitle file selected.")
            self.sub_file = None
        else:
            self.sub_button.config(state="normal")

# Launch the dialog
choice_dialog = SubtitleChoice()
file_path = choice_dialog.file_path
sub_option = choice_dialog.sub_option.get()
sub_file = choice_dialog.sub_file

if not file_path:
    print(Fore.RED + "No file selected." + Style.RESET_ALL)
    exit(1)

# === 2) Choose the output container ===
print("Choose the output container:")
print("1 - MP4")
print("2 - MKV")
choice = input("Enter 1 or 2: ")

if choice == "1":
    ext = "mp4"
elif choice == "2":
    ext = "mkv"
else:
    print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
    exit(1)

# === 3) Extract metadata ===

def ffprobe(cmd):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    return result.stdout.strip()


# --- Robust metadata extraction ---
duration_str = ffprobe([
    "ffprobe", "-v", "error", "-show_entries",
    "format=duration", "-of",
    "default=noprint_wrappers=1:nokey=1", file_path
])
try:
    duration = float(duration_str)
    if duration <= 0:
        raise ValueError
except Exception:
    print(Fore.RED + f"Could not determine video duration (got '{duration_str}'). Aborting." + Style.RESET_ALL)
    exit(1)

audio_bitrate_str = ffprobe([
    "ffprobe", "-v", "error", "-select_streams",
    "a:0", "-show_entries", "stream=bit_rate",
    "-of", "default=noprint_wrappers=1:nokey=1",
    file_path
])
if not audio_bitrate_str or audio_bitrate_str == "N/A" or audio_bitrate_str == "0":
    print(Fore.YELLOW + "Warning: Could not determine audio bitrate. Using default 128000 bps." + Style.RESET_ALL)
    audio_bitrate = 128000
else:
    try:
        audio_bitrate = int(audio_bitrate_str)
    except Exception:
        print(Fore.YELLOW + f"Warning: Unexpected audio bitrate value '{audio_bitrate_str}'. Using default 128000 bps." + Style.RESET_ALL)
        audio_bitrate = 128000

print(f"Duration: {duration:.2f} s")
print(f"Audio Bitrate: {audio_bitrate} bps")

# === 4) Calculate target video bitrate for a max video file size ===
max_size_gb = float(simpledialog.askstring("Target Video Size", "Enter the maximum file size in GB:"))

if max_size_gb <= 0:
    print(Fore.RED + "Invalid size. Must be greater than 0." + Style.RESET_ALL)
    exit(1)
# Make sure that the max size is smaller than the original file size

file_size = os.path.getsize(file_path) / (1024 * 1024 * 1024)  # in GB
print(f"Original File Size: {file_size:.2f} GB")

# if max_size_gb > file_size:
#     print(Fore.RED + f"Warning: The maximum size {max_size_gb} GB is larger than the original file size {file_size:.2f} GB." + Style.RESET_ALL)
#     exit(1)

# Calculate the target video bitrate
target_bits = max_size_gb * 1024 * 1024 * 1024 * 8  # in bits
audio_bits_total = audio_bitrate * duration # in bits
video_bits_total = target_bits - audio_bits_total # in bits
video_bitrate = video_bits_total / duration # in bits per second
video_bitrate_kbps = int(video_bitrate / 1000) # in kbps

print(f"Target Video Bitrate: {video_bitrate_kbps} kbps") 

# === 5) Build ffmpeg command based on subtitle option ===
output_file = os.path.splitext(file_path)[0] + f"_compressed.{ext}"

# Handle subtitle options


if sub_option == "soft":
    rel_sub_file = os.path.relpath(sub_file, start=os.path.dirname(file_path))
    ffmpeg_cmd = [
    "ffmpeg", "-i", file_path,
    "-i", rel_sub_file,
    "-c:s", "mov_text",
    "-map", "0:v", "-map", "0:a", "-map", "1:s",
    "-c:v", "libx264", "-b:v", f"{video_bitrate_kbps}k",
    "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart"
]

else:
    
    ffmpeg_cmd = [
            "ffmpeg", "-i", file_path, 
            "-c:v", "libx264", "-b:v", f"{video_bitrate_kbps}k",
            "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart"
        ]
    
    if sub_option == "hard" and sub_file:
        rel_sub_file = os.path.relpath(sub_file, start=os.path.dirname(file_path)).replace("\\", "/")
        ffmpeg_cmd += ["-vf", f"subtitles={rel_sub_file}"]
    
    

ffmpeg_cmd += [output_file, "-y"]

print(Fore.YELLOW + f"\nRunning ffmpeg with subtitles option: {sub_option}\n\n" + Style.RESET_ALL)
print("\tCommand:", " ".join(ffmpeg_cmd))
print()

ret = subprocess.call(ffmpeg_cmd)

if ret == 0:
    print(Fore.GREEN + f"\n✅ Compression finished. Output: {output_file}" + Style.RESET_ALL)
else:
    print(Fore.RED + f"\n❌ Compression failed." + Style.RESET_ALL)
