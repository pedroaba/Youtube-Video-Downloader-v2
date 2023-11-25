import uuid
import datetime

from pathlib import Path
from typing import TypeVar
from dataclasses import asdict

import pandas as pd

from pyyoutube import PlaylistItem
from userpaths import get_desktop

from youtube_video_downloader.core.base import Base
from youtube_video_downloader.core.types.video import VideoInfo
from youtube_video_downloader.core.types.file import AvailableExportType
from youtube_video_downloader.core.log import logger
from youtube_video_downloader.exceptions.runtime import InvalidExportType
from youtube_video_downloader.core.downloader import Downloader


T = TypeVar("T")


class Playlist(Base):
    MAX_OF_RETRIEVE = 50

    def __init__(self, api_key: str):
        super(Playlist, self).__init__(api_key=api_key)
        self._downloader = Downloader(api_key=api_key)

    def retrieve_videos_info(
            self,
            playlist_id: str,
            *,
            export_type: AvailableExportType = "csv",
            exports: bool = False
    ):
        logger.info(f"Starting listing of playlist: {playlist_id}")
        playlist_response = self._retrive_videos_from_playlist(playlist_id)

        videos = self.__format_videos(playlist_response.items)
        next_page_token = playlist_response.nextPageToken

        logger.info(f"Retrieved {len(videos)} videos.")
        while bool(next_page_token):
            playlist_response = self._retrive_videos_from_playlist(playlist_id, next_page_token)

            videos += self.__format_videos(playlist_response.items)
            logger.info(f"Retrieved {len(videos)} videos.")

            next_page_token = playlist_response.nextPageToken

            quantity_of_videos_retrieved = len(playlist_response.items)
            if quantity_of_videos_retrieved < Playlist.MAX_OF_RETRIEVE:
                break

        if exports:
            self._export(videos, export_type)
        return videos

    def download_all_videos_of_playlist(self, playlist_id: str, path_to_save_videos: str | Path):
        videos_info = self.retrieve_videos_info(playlist_id)
        for video in videos_info:
            self._downloader.download_video_by_id(
                video,
                path_to_save_videos,
                all_resolution=True
            )

    @staticmethod
    def _export(videos_info: list[VideoInfo], export_type: AvailableExportType) -> str:
        desktop_folder = Path(get_desktop())

        videos_info_dataframe = pd.json_normalize([asdict(video) for video in videos_info])

        export_id = str(uuid.uuid4())
        export_filepath = desktop_folder
        match export_type:
            case "csv":
                export_filepath /= f"{export_id}.csv"
                videos_info_dataframe.to_csv(
                    export_filepath,
                    index=False
                )

            case "excel":
                export_filepath /= f"{export_id}.xlsx"
                videos_info_dataframe.to_csv(
                    export_filepath,
                    index=False
                )

            case _:
                raise InvalidExportType(f"export passed: '{export_type}'")
        return str(export_filepath)

    def _format_video_info(self, video: PlaylistItem) -> VideoInfo:
        base_video_info = rf"{video.snippet.title} \o/ Id: {video.id}"
        logger.info(f"Converting Video: {base_video_info}")

        video_info = VideoInfo(
            id_on_playlist=video.id,
            title=video.snippet.title,
            _status=video.status.privacyStatus,
            channel_id=video.snippet.channelId,
            thumbnails=video.snippet.thumbnails,
            playlist_id=video.snippet.playlistId,
            channel_title=video.snippet.channelTitle,
            video_id=video.snippet.resourceId.videoId,
            position_on_playlist=video.snippet.position,
            video_description=video.snippet.description,
            video_owner_channel_id=video.snippet.videoOwnerChannelId,
            video_owner_channel_title=video.snippet.videoOwnerChannelTitle,
            published_at=datetime.datetime.fromisoformat(video.snippet.publishedAt),
        )

        logger.success(f"Converted Video: {base_video_info}")
        return video_info

    def _retrive_videos_from_playlist(self, playlist_id: str, page_token: str = None):
        logger.info(f"Making collect of playlist: {playlist_id} - page: {page_token}")
        return self.youtube_instance.get_playlist_items(
            playlist_id=playlist_id,
            page_token=page_token,
            count=Playlist.MAX_OF_RETRIEVE
        )

    def __format_videos(self, videos: list[T]) -> list[VideoInfo]:
        logger.info(f"Converting videos objects from youtube to domain")
        return list(
            map(
                self._format_video_info,
                videos
            )
        )
