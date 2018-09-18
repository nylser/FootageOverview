#!/usr/bin/env python3
import glob
import fnmatch
import os
import subprocess
import time

def find_files(match):
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, match):
            matches.append(os.path.join(root, filename))

    return matches

def convert_files(files):
    for f in files:
        subprocess.call(["./convert", f])
        os.remove(f)

def make_playable(files):
    for f in files:
        #subprocess.call(["ffmpeg", "-framerate", "24", "-i", f, "-i", f.replace("mp4", "wav"), "-c:v", "copy", "-c:a", "aac", "-y", f.replace("_pre", "")])
        subprocess.call(["ffmpeg", "-framerate", "24", "-i", f, "-c", "copy", "-y", f.replace("_pre", "")])
        os.remove(f)
def do_convert():
    videos = find_files('*.264')
    convert_files(videos)
    new_mp4s = find_files("*_pre.mp4")
    make_playable(new_mp4s)
    for f in find_files('*.wav'):
        os.remove(f)

if __name__ == '__main__':
    do_convert()

