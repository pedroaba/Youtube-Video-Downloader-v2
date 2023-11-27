from youtube_video_downloader.application.window._default import DefaultWindow


class PlaylistScreen(DefaultWindow):
    def __init__(self):
        super(PlaylistScreen, self).__init__()

    def mount_window(self, screen: str = "Playlist"):
        super(PlaylistScreen, self).mount_window(screen)
