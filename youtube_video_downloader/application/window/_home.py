from youtube_video_downloader.application.window._default import DefaultWindow


class HomeWindow(DefaultWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()

    def mount_window(self, screen: str = "Home"):
        super(HomeWindow, self).mount_window(screen)
