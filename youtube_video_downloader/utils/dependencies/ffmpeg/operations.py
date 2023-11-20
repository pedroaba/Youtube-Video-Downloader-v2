import platform

from youtube_video_downloader.utils.dependencies._checks import _check_packages_are_installed
from youtube_video_downloader.utils.dependencies.exceptions import UnknowOperationalSystem
from youtube_video_downloader.utils.dependencies.ffmpeg._installations import (
    _install_ffmpeg_on_windows,
    _install_ffmpeg_on_linux,
    _install_ffmpeg_on_macos
)


def check_if_ffmpeg_is_installed():
    return _check_packages_are_installed(["ffmpeg", "-version"])


def install_ffmpeg():
    system = platform.system()
    match system.upper():
        case "WINDOWS":
            _install_ffmpeg_on_windows()
        case "LINUX":
            _install_ffmpeg_on_linux()
        case "DARWIN":
            _install_ffmpeg_on_macos()
        case _:
            raise UnknowOperationalSystem(f"Unknow OS: {system}!")
