"""
Title       : MP3_partionner.py
Description : Splits an MP3 files according to a text file containing timestamps.
              The text file must contain lines with « HH:MM:SS Title », the start time and title of
              a part in the audio file.
Author      : MathieuChayer@Github
Date        : 2023-04-08
"""

from pydub import AudioSegment
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from slugify import slugify
import os

# Time conversions
S = 1000;
M = 60*S;
H = 60*M;

# Prompt user for audio file, timestamps file and destination folder
current_dir = os.getcwd()

print("Select MP3 file : ")
audio_file = askopenfilename(
    initialdir = current_dir,
    title = 'Select MP3 file...',
    filetypes=[("MP3 files", ".mp3")])
print("\t",audio_file)

print("Select timestamps file : ")
timestamps_file = askopenfilename(
    initialdir = current_dir,
    title = 'Select Timestamps file...',
    filetypes=[("TXT files", ".txt")])
print("\t",timestamps_file)

print("Select destination folder : ")
destination_folder=askdirectory(
    initialdir=current_dir,
    title='Select destination folder...'
)
print("\t",destination_folder)

# Open and read timestamps text file
with open(timestamps_file) as f:
    lines = f.readlines()

# Parse file, convert timestamp to ms and slugify title
timestamps = []
titles = []
for parts in lines :
    [timestamp, title] = parts.strip("\n").split(" ", 1)
    timestamp = timestamp.split(":")
    if len(timestamp) == 2 :
        timestamp.insert(0,"00")
    timestamps.append(H*int(timestamp[0])+M*int(timestamp[1])+S*int(timestamp[2]))
    titles.append(slugify(title))

# Read audio
print("Now reading MP3 file...")
audio = AudioSegment.from_mp3(audio_file)

# Add EOF to timestamps
timestamps.append(len(audio))

# Split audio into parts and save files
while len(titles):
    split_start = timestamps[0]
    timestamps.pop(0)
    split_stop = timestamps[0]
    print("Processing "+titles[0]+"(",split_start,":",split_stop,")...")
    audio[split_start:split_stop].export(destination_folder + "/" + titles[0] + ".mp3", format="mp3")
    titles.pop(0)



