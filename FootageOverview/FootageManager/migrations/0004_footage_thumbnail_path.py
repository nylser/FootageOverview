# Generated by Django 2.1.1 on 2018-09-20 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FootageManager', '0003_footage_staticpath'),
    ]

    operations = [
        migrations.AddField(
            model_name='footage',
            name='thumbnail_path',
            field=models.CharField(default='', max_length=200, verbose_name='thumbnail_path'),
            preserve_default=False,
        ),
    ]