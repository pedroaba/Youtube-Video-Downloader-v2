import traceback
from pathlib import Path

from youtube_video_downloader.utils.file.exceptions import NotAFileError


def remove_file(filepath: str | Path) -> None:
    if isinstance(filepath, str):
        filepath = Path(filepath)

    if not filepath.is_file():
        raise NotAFileError()

    try:
        filepath.unlink(missing_ok=True)
    except Exception as e:
        print(traceback.format_exc())
        print(e.args)
