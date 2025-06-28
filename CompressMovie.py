import subprocess
import os
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore, Style

init()

# === Dependencies ===
# FFmpeg & FFprobe have to be in the PATH
# You can download them from https://ffmpeg.org/download.html
# Make sure to add the bin directory to your PATH environment variable

# === Requirements ===
# Python 3.x
# colorama (for colored output in the terminal)
# tkinter (for file dialog)

# === Instructions ===
# 1. Run this script
# 2. Choose a video file
# 3. Choose the output container (MP4 or MKV)
# 4. The script will extract metadata and calculate the target video bitrate
# 5. It will generate a .bat file to compress the video to ~1.8 GB
# 6. The .bat file will be executed, and the output video will be created
# 7. The .bat file will be deleted after the compression is done

# === 1) Ask for the video file ===
print("Choose a video file.\n")
print(Fore.CYAN + "Tkinter should have opened a window to choose the file." + Style.RESET_ALL)

# Initialize Tkinter and hide the main window

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Choose a video file",
    filetypes=[("Videos", "*.mp4 *.mkv *.avi")]
)

if not file_path:
    print(Fore.RED + "No file selected." + Style.RESET_ALL)
    exit(1)

# === 2) Choisir le conteneur de sortie ===
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

duration = float(ffprobe(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-of",
                          "default=noprint_wrappers=1:nokey=1", file_path]))

audio_bitrate = int(ffprobe(["ffprobe", "-v", "error", "-select_streams",
                             "a:0", "-show_entries", "stream=bit_rate",
                             "-of", "default=noprint_wrappers=1:nokey=1",
                             file_path]))

print(f"Duration: {duration:.2f} s")
print(f"Audio Bitrate: {audio_bitrate} bps")

# === 4) Calculate target video bitrate for ~1.8 GB ===

target_bits = 1.8 * 1024 * 1024 * 1024 * 8  # 1.8 GB in bits
audio_bits_total = audio_bitrate * duration
video_bits_total = target_bits - audio_bits_total
video_bitrate = video_bits_total / duration
video_bitrate_kbps = int(video_bitrate / 1000)

print(f"Target Video Bitrate: {video_bitrate_kbps} kbps")

# === 5) Generate the .bat ===

output_file = os.path.splitext(file_path)[0] + f"_compressed.{ext}"
bat_filename = "compress_video.bat"

bat_content = f"""@echo off
ffmpeg -i "{file_path}" -c:v libx264 -b:v {video_bitrate_kbps}k -preset medium -c:a aac -b:a 192k -movflags +faststart "{output_file}"
pause
"""

with open(bat_filename, "w", encoding="utf-8") as f:
    f.write(bat_content)

print(f"\n✅ Batch file generated: {bat_filename}")
print(f"It will create: {output_file}")

# === 6) Launch the .bat and wait for it to finish ===

ret = subprocess.call([bat_filename], shell=True)

# === 7) Delete the .bat AFTER compression ===

if ret == 0:
    try:
        os.remove(bat_filename)
        print(Fore.GREEN + f"{bat_filename} deleted." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error deleting {bat_filename}: {e}" + Style.RESET_ALL)
else:
    print(Fore.RED + f"Batch file exited with code {ret}, file not deleted." + Style.RESET_ALL)
