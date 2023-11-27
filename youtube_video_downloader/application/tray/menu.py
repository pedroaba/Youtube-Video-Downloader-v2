import sys
import inspect
import multiprocessing

from typing import Any, Callable

import pystray
from PIL import Image

from youtube_video_downloader.application.window import DownloadVideoScreen, HomeWindow, PlaylistScreen
from youtube_video_downloader.application.tray._enums import AvailableScreen
from youtube_video_downloader.application.exceptions.attributes import NonAssignableAttribute
from youtube_video_downloader.application.tray._notification import NotificationSystem
from youtube_video_downloader.configs import application_config


WEBVIEW_PROCESS: multiprocessing.Process | None = None

count = 0


def _run_webview_app(queue: multiprocessing.Queue):
    _screen = queue.get()
    if _screen is not None:
        match _screen:
            case AvailableScreen.HOME_SCREEN:
                screen = HomeWindow()
            case AvailableScreen.DOWNLOAD_SCREEN:
                screen = DownloadVideoScreen()
            case AvailableScreen.PLAYLIST_SCREEN:
                screen = PlaylistScreen()
            case _:
                return
        screen.open_window()


class TrayMenu:
    def __init__(
            self,
            _icon: str,
            name: str,
            menu_items: list[str] = None,
            *,
            close_fn: Callable[[], None] | Callable[[...], None] = None,
            close_fn_attrs: dict[str, Any] = None
    ):
        self.close_fn = close_fn
        self.close_fn_attrs = close_fn_attrs

        self._menu_name = name

        # tray configs
        self._icon_path = _icon
        self._menu_items = menu_items if menu_items is not None else []

        self._tray_icon: pystray.Icon  # type pystray.Icon
        self._current_window = AvailableScreen.EMPTY

        if sys.platform == "darwin":
            self._context = multiprocessing.get_context("spawn")
            self._process = self._context.Process
            self._queue = self._context.Queue()
        else:
            self._process = multiprocessing.Process
            self._queue = multiprocessing.Queue()
        self._create_subprocess()
        self._mount_menu()

    def main_loop(self):
        self._tray_icon.notify(
            message=f"{self._menu_name} is running!"
        )

        self._tray_icon.run()
        self._close_sub_process()

    def _mount_menu(self):
        import ctypes

        app_id = self._menu_name  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self._image_icon = Image.open(self._icon_path)
        self._tray_icon: pystray.Icon = pystray.Icon(
            self._menu_name,
            self._image_icon,
        )

        self._tray_icon.default_action = self._handle_default_click
        self._tray_icon.menu = pystray.Menu(
            pystray.MenuItem("Playlist", self._handle_on_click),
            pystray.MenuItem("Download", self._handle_on_click),
            pystray.MenuItem("Exit", self._close_application),
            pystray.MenuItem("default", self._handle_default_click, default=True, visible=False)
        )

    def _handle_default_click(self):
        self._current_window = AvailableScreen.HOME_SCREEN
        self._create_subprocess()

    def _handle_on_click(self, _icon, menu_item: pystray.MenuItem):
        match menu_item.text:
            case "Download":
                self._current_window = AvailableScreen.DOWNLOAD_SCREEN
                self._create_subprocess()
            case "Playlist":
                self._current_window = AvailableScreen.PLAYLIST_SCREEN
                self._create_subprocess()
        print("_handle_on_click", self._current_window)

    @staticmethod
    def _close_sub_process():
        global WEBVIEW_PROCESS
        if WEBVIEW_PROCESS is not None:
            WEBVIEW_PROCESS.terminate()

    def _create_subprocess(self):
        try:
            global WEBVIEW_PROCESS
            if WEBVIEW_PROCESS is not None and WEBVIEW_PROCESS.is_alive():
                return

            WEBVIEW_PROCESS = self._process(target=_run_webview_app, args=(self._queue, ))
            WEBVIEW_PROCESS.start()

            self._queue.put(self._current_window)
        except Exception as e:
            print(e)

    def _close_application(self):
        def function_has_args(fn: Callable) -> bool:
            fn_args = inspect.getfullargspec(fn)

            has_args = len(fn_args.args) > 0
            has_kwargs = fn_args.varkw is not None
            has_varargs = fn_args.varargs is not None
            has_defaults = fn_args.defaults is not None
            has_kwonlyargs = fn_args.kwonlyargs is not None
            has_kwonlydefaults = fn_args.kwonlydefaults is not None

            return has_args or has_kwargs or has_varargs or has_defaults or has_kwonlyargs or has_kwonlydefaults

        if self.close_fn is not None:
            if self.close_fn_attrs is not None and function_has_args(self.close_fn):
                self.close_fn(**self.close_fn_attrs)
            self.close_fn()

        self._close_sub_process()
        if self._tray_icon is not None:
            self._tray_icon.stop()

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
