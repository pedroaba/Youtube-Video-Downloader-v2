import os
import traceback

from youtube_video_downloader.utils.dependencies._commands import Command


def _install_package(commands: list[Command] | Command):
    if not isinstance(commands, list):
        commands = [commands]

    for _command in commands:
        if _command.main_command:
            os.system(_command.command)
        else:
            try:
                os.system(_command.command)
            except Exception as e:
                print(traceback.format_exc())
                print(e)
