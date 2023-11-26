from typing import Any

import PySimpleGUI as psg
from psgtray import SystemTray

from youtube_video_downloader.application.exceptions.attributes import NonAssignableAttribute
from youtube_video_downloader.application.tray._notification import NotificationSystem
from youtube_video_downloader.configs import application_config


class TrayMenu:
    def __init__(self, icon: str, name: str):
        self._menu_name = name

        # tray configs
        self._icon_path = icon
        self._mount_menu()

    def _mount_menu(self):
        import ctypes

        app_id = self._menu_name  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self._window = psg.Window(self._menu_name, [
            [psg.Text(self._menu_name)]
        ], finalize=True)

        self._window.hide()

        self._tray_icon = SystemTray(
            icon=self._icon_path,
            window=self._window,
            menu=[self._menu_name, ['Exit']],
            single_click_events=True,
        )

        self._tray_icon.title = self._menu_name

    def main_loop(self):
        self._tray_icon.show_message(
            message=f"{self._menu_name} is running!"
        )
        while True:
            event, values, *rest = self._window.read()
            match values:
                case ["Exit"] | psg.WIN_CLOSED:
                    self._close_application()

            print(event, values, rest)

    @staticmethod
    def _close_application():
        exit(0)

    def _notify_when_is_ready(self):
        message = f"{self._menu_name} is running!"
        match application_config.running_os:
            case "windows":
                NotificationSystem.send_windows_notification(
                    message
                )
            case "linux" | "macos":
                NotificationSystem.send_generic_notification(
                    message
                )
            case _:
                # not stop the tray, because don't need
                print("Unknown operational system")

    @property
    def name(self) -> str:
        return self._menu_name

    @name.setter
    def name(self, _: Any) -> None:
        raise NonAssignableAttribute("name")


if __name__ == "__main__":
    icon = "icon.ico" if application_config.running_os == "windows" else "icon.png"
    tray = TrayMenu(
        name=application_config.app_name,
        icon=str(
            (
                    application_config.current_execution_path / "assets" / icon
            ).absolute()
        )
    )

    tray.main_loop()
