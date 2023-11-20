import os

from moviepy.editor import VideoFileClip

from youtube_video_downloader.utils.file.exceptions import NotAFileError


def is_corrupt_video(video_path: str) -> bool:
    if not os.path.exists(video_path):
        raise FileExistsError()

    if not os.path.isfile(video_path):
        raise NotAFileError()

    try:
        video_clip = VideoFileClip(video_path)
        print("Video: ", video_clip.filename)
        print("Video Size (B): ", video_clip.size)

        return True
    except Exception:
        return False


