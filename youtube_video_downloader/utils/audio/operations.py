from io import BytesIO
from pathlib import Path

from pydub import AudioSegment

from youtube_video_downloader.utils.file.operations import remove_file
from youtube_video_downloader.utils.audio.exceptions import InvalidAudioCodec


def convert_webm_audio_to_mp3(audio_path: str | Path) -> Path:
    if isinstance(audio_path, str):
        audio_path = Path(audio_path)
    mp3_sound_path = str(
        audio_path.with_suffix(".mp3").absolute()
    )

    bytes_io = BytesIO()
    with open(audio_path, "rb") as sound_file:
        bytes_io = BytesIO(sound_file.read())

    sound = AudioSegment.from_file(bytes_io, codec="opus")
    sound.export(mp3_sound_path)

    remove_file(audio_path)
    return Path(mp3_sound_path)


def convert_any_audio_to_mp3(audio_path: str | Path, codec: str) -> Path:
    if isinstance(audio_path, str):
        audio_path = Path(audio_path)

    mp3_sound_path = str(
        audio_path.with_suffix(".mp3").absolute()
    )

    try:
        sound = AudioSegment.from_file(
            str(audio_path.absolute()),
            codec=codec
        )

        sound.export(mp3_sound_path)
        remove_file(audio_path)
    except Exception as e:
        raise InvalidAudioCodec(
            f"Codec: {codec}\n"
            f"Exception Lib: {e}"
        )

    return Path(mp3_sound_path)
