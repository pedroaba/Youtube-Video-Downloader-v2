import abc

from pyyoutube import Api, PlaylistItem

from youtube_video_downloader.exceptions.runtime import InvalidApiKey
from youtube_video_downloader.core.types.video import VideoInfo


class Base:
    def __init__(self, api_key: str = None):
        if api_key is None or not api_key:
            raise InvalidApiKey("Please check your api key")

        self._api_key = api_key
        self.object_name = self.__class__.__name__ + "__youtube"
        self.youtube_instance = Api(api_key=api_key)

    @abc.abstractmethod
    def _format_video_info(self, video: PlaylistItem) -> VideoInfo:
        pass
