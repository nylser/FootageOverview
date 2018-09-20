#!/usr/bin/env python3
import glob
import fnmatch
import os
import subprocess
import time
import sys


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
        subprocess.call(["ffmpeg", "-framerate", "24", "-i", f,
                         "-c", "copy", "-y", f.replace("_pre", "")])
        os.remove(f)
        create_thumbnail(f.replace("_pre", ""))


def create_thumbnail(file):
    filedir = os.path.dirname(file)
    thumbdir = os.path.join(filedir, '../thumbnail')
    if not os.path.exists(thumbdir):
        os.mkdir(thumbdir)
    thumbname = os.path.splitext(os.path.basename(file))[0]+".jpg"
    thumbfile = os.path.join(thumbdir, thumbname)
    print(thumbfile)
    subprocess.call(["ffmpeg", "-i", file, "-ss", "00:00:01",
                     "-vframes", "1", thumbfile])


def do_convert():
    videos = find_files('*.264')
    convert_files(videos)
    new_mp4s = find_files("*_pre.mp4")
    make_playable(new_mp4s)
    for f in find_files('*.wav'):
        os.remove(f)


def create_missing_thumbnails():
    vids = find_files("*.mp4")
    for vid in vids:
        filedir = os.path.dirname(vid)
        thumbdir = os.path.join(filedir, '../thumbnail')
        if not os.path.exists(thumbdir):
            os.mkdir(thumbdir)
        thumbname = os.path.splitext(os.path.basename(vid))[0]+".jpg"
        thumbfile = os.path.join(thumbdir, thumbname)
        if not os.path.exists(thumbfile):
            subprocess.call(["ffmpeg", "-i", vid, "-ss", "00:00:01",
                             "-vframes", "1", thumbfile])
        print(thumbfile)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        do_convert()
    else:
        if sys.argv[1] == "-t":
            create_missing_thumbnails()
