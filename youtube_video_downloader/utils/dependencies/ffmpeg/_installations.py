from youtube_video_downloader.utils.dependencies._checks import _check_packages_are_installed
from youtube_video_downloader.utils.dependencies.exceptions import NotFoundAPackageManager
from youtube_video_downloader.utils.dependencies._installations import _install_package
from youtube_video_downloader.utils.dependencies._commands import Command


def _install_ffmpeg_on_windows():
    is_choco_installed = _check_packages_are_installed(["choco", "-v"])
    is_winget_installed = _check_packages_are_installed(["winget", "-v"])
    is_scoop_installed = _check_packages_are_installed(["scoop", "-v"])

    command_line = "{pkg} install ffmpeg"
    if is_scoop_installed:
        command_line = command_line.format(pkg="scoop")
    elif is_winget_installed:
        command_line = command_line.format(pkg="winget")
    elif is_choco_installed:
        command_line = command_line.format(pkg="choco")
    else:
        raise NotFoundAPackageManager("Please install some package manager: ['scoop', 'winget', 'choco']")

    command = Command(command=command_line, is_main_command=True)
    _install_package(command)


def _install_ffmpeg_on_linux():
    command = Command(command="sudo apt install ffmpeg", is_main_command=True)
    _install_package(command)


def _install_ffmpeg_on_macos():
    command = Command(command="brew install ffmpeg", is_main_command=True)
    _install_package(command)
