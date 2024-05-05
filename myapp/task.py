# tasks.py
from celery import shared_task
from .models import SingleAudioFile, AudioFile, AudioComparisonResult
from .audio_processor import process_audio


@shared_task
def process_audio_task():
    # get single audio path
    latest_single_audio = SingleAudioFile.objects.latest("id")
    single_audio_path = latest_single_audio.file.path

    # get multilple audio paths
    all_audio_files = AudioFile.objects.all()
    folder_paths = [audio_file.file.path for audio_file in all_audio_files]

    # Call the processing function
    results = process_audio(single_audio_path, folder_paths)

    # Store only the results where audio files are similar in the database
    for result in results:
        if "similar" in result:
            source, compared = parse_result_without_distance(result)
            AudioComparisonResult.objects.create(
                source_audio=source, compared_audio=compared, similarity=True
            )

    return results


def parse_result_without_distance(result):
    # Extracts only the file names from the result string for similar files
    parts = result.split(":")
    audio_parts = parts[0].split(" is similar to ")
    source_audio = audio_parts[0].replace("Audio ", "").strip()
    compared_audio = audio_parts[1].strip()
    return source_audio, compared_audio
