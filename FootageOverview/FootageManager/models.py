from django.db import models
from glob import glob
from datetime import datetime
from django.db.models.signals import post_init
import os.path
import pytz

from django.conf import settings


# Create your models here.

class Footage(models.Model):
    PIC_TIMEFORMAT = "%y%m%d%H%M%S%f"
    VID_TIMEFORMAT = "%y%m%d%H%M%S"

    date = models.DateTimeField('date recorded')
    VIDEO = 'VID'
    PICTURE = 'PIC'
    TYPE_CHOICES = (
        (VIDEO, 'Video'),
        (PICTURE, 'Picture'),
    )
    PERIODIC = 'PER'
    ALARM = 'ALA'
    CAUSE_CHOICES = (
        (PERIODIC, 'Periodic'),
        (ALARM, 'Alarm'),
    )
    footype = models.CharField(
        'type', max_length=3, choices=TYPE_CHOICES, default=PICTURE)
    foocause = models.CharField(
        'cause', max_length=3, choices=CAUSE_CHOICES, default=PERIODIC)
    filepath = models.FilePathField('Footage path', allow_files=True)
    staticpath = models.CharField('static_path', max_length=200)
    thumbnail_path = models.CharField('thumbnail_path', max_length=200)
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE)
    length = models.IntegerField('length', blank=True, default=0)

    def __str__(self):
        return self.get_footype_display() + " - " \
               + self.get_foocause_display() + " - " + str(self.date)


def parse_footage(filepath, camera):
    cause = None
    ftype = None
    date = None
    pre = os.path.basename(filepath)[0:1]
    staticpath = filepath.replace(settings.FOOTAGE_BASEPATH, '')
    if pre == "A":
        cause = Footage.ALARM
    else:
        cause = Footage.PERIODIC
    if os.path.splitext(filepath)[1] == ".jpg":
        ftype = Footage.PICTURE
    elif os.path.splitext(filepath)[1] == ".mp4":
        ftype = Footage.VIDEO
    datename = os.path.splitext(os.path.basename(filepath))[0][1:]
    if ftype == Footage.PICTURE:
        date = datetime.strptime(datename, Footage.PIC_TIMEFORMAT)
        date = pytz.utc.localize(date)
        return Footage(foocause=cause, footype=ftype,
                       date=date, filepath=filepath,
                       camera=camera, staticpath=staticpath,
                       thumbnail_path=staticpath)
    else:
        start = datetime.strptime(
            ''.join(datename.split("_")[0:2]), Footage.VID_TIMEFORMAT)
        end = datetime.strptime(datename.split(
            "_")[0]+datename.split("_")[2], Footage.VID_TIMEFORMAT)
        length = end - start
        thumbnailpath = staticpath.replace("record", "thumbnail")
        thumbnailpath = thumbnailpath.replace("mp4", "jpg")
        return Footage(foocause=cause, footype=ftype,
                       date=start, filepath=filepath, camera=camera,
                       length=length.total_seconds(),
                       staticpath=staticpath, thumbnail_path=thumbnailpath)


class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Camera(models.Model):
    name = models.CharField(max_length=200)
    directory = models.FilePathField(
        '../', allow_folders=True, allow_files=False)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.location.name

    def do_scan(self):
        # videos = glob(self.directory+"/**/*.264", recursive=True)
        videos = glob(self.directory+"/**/*.mp4", recursive=True)
        images = glob(self.directory+"/**/*.jpg", recursive=True)
        img_db = Footage.objects.filter(footype=Footage.PICTURE)
        vid_db = Footage.objects.filter(footype=Footage.VIDEO)
        vid_db = [obj.filepath for obj in vid_db]
        img_db = [obj.filepath for obj in img_db]

        to_add = []
        for image in images:
            if 'thumbnail' not in image and image not in img_db:
                to_add.append(image)
        for vid in videos:
            if not vid.endswith('_pre.mp4') and vid not in vid_db:
                to_add.append(vid)

        for footage in to_add:
            i = parse_footage(footage, self)
            i.save()
        return len(to_add)
