# Generated by Django 2.0.13 on 2020-05-08 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_video_vedio_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='vedio_time',
            field=models.IntegerField(default=0, verbose_name='视频时长'),
        ),
    ]
