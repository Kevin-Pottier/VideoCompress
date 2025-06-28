import subprocess
import os
import tkinter as tk
from tkinter import filedialog

# === Dépendances ===
# FFmpeg & FFprobe doivent être dans le PATH

# === 1) Demander le fichier vidéo ===
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Choisir un fichier vidéo",
    filetypes=[("Vidéos", "*.mp4 *.mkv")]
)

if not file_path:
    print("Aucun fichier sélectionné.")
    exit(1)

# === 2) Choisir le conteneur de sortie ===
print("Choisir le conteneur de sortie :")
print("1 - MP4")
print("2 - MKV")
choice = input("Entrer 1 ou 2 : ")

if choice == "1":
    ext = "mp4"
elif choice == "2":
    ext = "mkv"
else:
    print("Choix invalide.")
    exit(1)

# === 3) Extraire les métadonnées ===

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

print(f"Durée : {duration:.2f} s")
print(f"Bitrate audio : {audio_bitrate} bps")

# === 4) Calculer le bitrate vidéo cible pour ~1.8 Go ===

target_bits = 1.8 * 1024 * 1024 * 1024 * 8  # 1.8 Go en bits
audio_bits_total = audio_bitrate * duration
video_bits_total = target_bits - audio_bits_total
video_bitrate = video_bits_total / duration
video_bitrate_kbps = int(video_bitrate / 1000)

print(f"Bitrate vidéo cible : {video_bitrate_kbps} kbps")

# === 5) Générer le .bat ===

output_file = os.path.splitext(file_path)[0] + f"_compressed.{ext}"
bat_filename = "compress_video.bat"

bat_content = f"""@echo off
ffmpeg -i "{file_path}" -c:v libx264 -b:v {video_bitrate_kbps}k -preset medium -c:a aac -b:a 192k -movflags +faststart "{output_file}"
pause
"""

with open(bat_filename, "w", encoding="utf-8") as f:
    f.write(bat_content)

print(f"\n✅ Fichier batch généré : {bat_filename}")
print(f"Il va créer : {output_file}")

# === 6) Lancer le .bat et attendre la fin ===

ret = subprocess.call([bat_filename], shell=True)

# === 7) Supprimer le .bat APRÈS la compression ===

if ret == 0:
    try:
        os.remove(bat_filename)
        print(f"{bat_filename} supprimé.")
    except Exception as e:
        print(f"Erreur lors de la suppression de {bat_filename} : {e}")
else:
    print(f"Le batch s'est terminé avec le code {ret}, le fichier n'a pas été supprimé.")
