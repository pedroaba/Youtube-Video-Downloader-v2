from youtube_video_downloader.application.tray._enums import AvailableScreen


_CURRENT_WINDOW = AvailableScreen.EMPTY


def set_current_window(screen: AvailableScreen = AvailableScreen.EMPTY):
    global _CURRENT_WINDOW
    _CURRENT_WINDOW = screen


def get_current_window() -> AvailableScreen:
    global _CURRENT_WINDOW
    return _CURRENT_WINDOW
