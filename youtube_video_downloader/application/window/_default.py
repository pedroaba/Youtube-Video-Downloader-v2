import webview

from youtube_video_downloader.application.exceptions.window import NonWindowInstance
from youtube_video_downloader.configs import application_config as app


class DefaultWindow:
    def __init__(self):
        self._window: webview.Window = None
        self.mount_window()

    def open_window(self):
        if self._window is None:
            raise NonWindowInstance()
        webview.start()

    def destroy(self):
        if self._window is None:
            raise NonWindowInstance()
        self._window.destroy()

    def mount_window(self, screen: str = ""):
        self._window = webview.create_window(
            f"{app.app_name} - {screen}",
        )
