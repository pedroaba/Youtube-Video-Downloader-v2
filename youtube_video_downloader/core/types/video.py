from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pyyoutube import Thumbnails


@dataclass
class VideoInfo:
    channel_id: str
    playlist_id: str
    channel_title: str
    id_on_playlist: str
    position_on_playlist: int

    title: str
    video_id: str
    video_description: str
    published_at: datetime

    thumbnails: dict

    video_owner_channel_id: str
    video_owner_channel_title: str

    _status: str

    def __init__(
            self,
            title: str,
            _status: str,
            video_id: str,
            channel_id: str,
            playlist_id: str,
            channel_title: str,
            id_on_playlist: str,
            video_description: str,
            thumbnails: Thumbnails,
            published_at: datetime,
            position_on_playlist: int,
            video_owner_channel_id: str,
            video_owner_channel_title: str
    ):
        self.title = title
        self._status = _status
        self.channel_id = channel_id
        self.playlist_id = playlist_id
        self.published_at = published_at
        self.channel_title = channel_title
        self.id_on_playlist = id_on_playlist
        self.thumbnails = thumbnails.to_dict()
        self.video_description = video_description
        self.position_on_playlist = position_on_playlist
        self.video_owner_channel_id = video_owner_channel_id
        self.video_id = video_id.replace("=-", "")
        self.video_owner_channel_title = video_owner_channel_title

    @property
    def is_public(self) -> bool:
        return self._status == "public"

    @property
    def video_url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"

    @staticmethod
    def get_columns_for_df() -> dict[str, str]:
        return {
            "channel_id": "Channel ID",
            "playlist_id": "Playlist ID",
            "channel_title": "Channel Title",
            "id_on_playlist": "ID on Playlist",
            "position_on_playlist": "Position on Playlist",
            "title": "Title",
            "video_id": "Video ID",
            "video_description": "Video Description",
            "published_at": "Publish At",
            "thumbnails": "Thumbnails",
            "video_owner_channel_id": "Video Owner Channel ID",
            "video_owner_channel_title": "Video Owner Channel Title"
        }

    def __repr__(self):
        return f"<VideoInfo title='{self.title}' url='{self.video_url}'>"


class VideoResolutions(Enum):
    LOWEST = "144p"
    LOWER = "240p"
    LOW = "360p"
    MEDIUM = "480p"
    HIGH = "720p"
    HIGHER = "1080p"
