from abc import ABC, abstractmethod

from plyer import notification as pl_notify
from winotify import Notification, audio

from youtube_video_downloader.configs import application_config as app

_ICON_PATH = (app.current_execution_path / "assets" / "icon.ico").absolute()
_ICON_PATH_STR = str(_ICON_PATH)


class NotificationSystem(ABC):
    @abstractmethod
    def __init__(self):
        """Abstract class for a notification system"""
        pass

    @staticmethod
    def send_windows_notification(message: str, *, label_to_show: str = None, link_to_open: str = None) -> None:
        def check_if_is_valid(value) -> bool:
            return value is not None and isinstance(value, str)

        notification = Notification(
            app_id=app.app_name,
            title="",
            msg=message,
            duration="long",
            icon=_ICON_PATH_STR
        )

        notification.set_audio(audio.Default, loop=False)
        if check_if_is_valid(label_to_show) and check_if_is_valid(link_to_open):
            notification.add_actions(label_to_show, link_to_open)
        notification.show()

    @staticmethod
    def send_generic_notification(message: str) -> None:
        pl_notify.notify(
            title=app.app_name,
            app_name=app.app_name,
            app_icon=_ICON_PATH_STR,
            message=message,
            timeout=5000,
            toast=True
        )
