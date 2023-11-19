import sys
from enum import Enum
from datetime import datetime

from loguru import logger as _logger
from youtube_video_downloader.configs import application_config


class _CustomLogLevel(Enum):
    ...


current_date = datetime.now()
current_formatted_date = current_date.strftime("%m-%d-%Y-%Hh%Mm%Ss")
current_month = current_date.strftime("%B")
current_day = current_date.strftime("%A")

log_filepath = application_config.get_log_filepath(
    f"log_{current_formatted_date}",
    _extra_folders=[
        current_month,
        current_day
    ]
)


_logger.add(
    sys.stdout,
    enqueue=True,
    colorize=True,
    diagnose=True,
    backtrace=True,
)

_logger.add(
    sink=str(log_filepath),
    enqueue=True,
    backtrace=True,
    diagnose=True
)

for custom_enum in _CustomLogLevel:
    _logger.level(custom_enum.name, custom_enum.value, color="<fg #8FB339>")
