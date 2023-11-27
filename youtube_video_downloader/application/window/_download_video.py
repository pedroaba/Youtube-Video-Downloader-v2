from youtube_video_downloader.application.window._default import DefaultWindow


class DownloadVideoScreen(DefaultWindow):
    def __init__(self):
        super(DownloadVideoScreen, self).__init__()

    def mount_window(self, screen: str = "Download Video"):
        super(DownloadVideoScreen, self).mount_window(screen)
