# tasks.py
from celery import shared_task
from .models import SingleAudioFile, AudioFile
from .audio_processor import process_audio


@shared_task
def process_audio_task():
    # 获取单个音频文件路径
    latest_single_audio = SingleAudioFile.objects.latest("id")
    single_audio_path = latest_single_audio.file.path

    # 获取所有音频文件路径
    all_audio_files = AudioFile.objects.all()
    folder_paths = [audio_file.file.path for audio_file in all_audio_files]

    # 调用处理函数
    results = process_audio(single_audio_path, folder_paths)

    #  reserve for more process, store result to database
    # and send result to front end

    return results
