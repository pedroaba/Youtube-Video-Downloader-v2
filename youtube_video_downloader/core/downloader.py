import sys
from pathlib import Path

from pytube import YouTube, Stream
from pyyoutube import PlaylistItem

from youtube_video_downloader.core.base import Base
from youtube_video_downloader.core.types.video import VideoInfo, VideoResolutions
from youtube_video_downloader.utils.format_file_name import sanitize_string_to_create_a_folder
from youtube_video_downloader.configs import application_config


class Downloader(Base):
    def __init__(self, api_key: str):
        super(Downloader, self).__init__(api_key)

    def download_video_by_id(
            self,
            video: VideoInfo,
            path_to_save_video: str | Path,
            *,
            all_resolution: bool = False,
            resolution: VideoResolutions = VideoResolutions.MEDIUM,
            only_best_resolution: bool = False,
            only_lowest_resolution: bool = False
    ):
        if not isinstance(path_to_save_video, Path):
            path_to_save_video = Path(path_to_save_video)

        if not path_to_save_video.exists():
            path_to_save_video.mkdir(exist_ok=True)

        youtube_video = YouTube(
            video.video_url,
            on_progress_callback=self._handle_progress
        )

        if all_resolution:
            sanitized_title = sanitize_string_to_create_a_folder(youtube_video.title)

            folder_to_save_videos = path_to_save_video / sanitized_title
            folder_to_save_videos.mkdir(exist_ok=True)

            folder_to_save_audios = application_config.temp_folder / sanitized_title / "audio"

            for stream in youtube_video.streams.filter(type="video").all():
                video_path = stream.download(
                    folder_to_save_videos,
                    filename_prefix=f"{stream.resolution}_{stream.subtype}_"
                )

                is_progressive_stream = stream.is_progressive
                if not is_progressive_stream:
                    audio = youtube_video.streams.filter(type="audio").order_by("abr").desc().first()
                    audio_already_downloaded = (folder_to_save_audios / f"{audio.title}.{audio.subtype}").exists()

                    if not audio_already_downloaded:
                        audio.download(
                            folder_to_save_audios
                        )

                    # TODO - join video with audio
            return

        if only_best_resolution:
            video_stream = youtube_video.streams.filter(type="video").get_highest_resolution()
        elif only_lowest_resolution:
            video_stream = youtube_video.streams.filter(type="video").get_lowest_resolution()
        else:
            video_stream = youtube_video.streams.filter(resolution=resolution.value, type="video").first()
        video_stream.download(path_to_save_video)

    @staticmethod
    def _handle_progress(stream: Stream, _: bytes, bytes_remaining: int):
        current = ((stream.filesize - bytes_remaining) / stream.filesize)
        percent = '{0:.1f}'.format(current * 100)
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)

        sys.stdout.write(' ↳ Downloading: {video_title} [{type}] |{bar}| {percent}%\r'.format(
                bar=status,
                percent=percent,
                video_title=stream.title,
                type=f"{stream.resolution} - {stream.subtype}"
            )
        )
        sys.stdout.flush()

    def _format_video_info(self, video: PlaylistItem) -> VideoInfo:
        pass
