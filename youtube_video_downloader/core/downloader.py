import sys
from pathlib import Path

from pytube import YouTube, Stream
from pyyoutube import PlaylistItem
from moviepy.editor import VideoFileClip, AudioFileClip

from youtube_video_downloader.core.base import Base
from youtube_video_downloader.core.types.video import VideoInfo, VideoResolutions
from youtube_video_downloader.utils.file.format import sanitize_string_to_create_a_folder
from youtube_video_downloader.utils.audio.operations import convert_webm_audio_to_mp3, convert_any_audio_to_mp3
from youtube_video_downloader.utils.file.operations import remove_file


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
    ) -> None:
        if not isinstance(path_to_save_video, Path):
            path_to_save_video = Path(path_to_save_video)

        if not path_to_save_video.exists():
            path_to_save_video.mkdir(exist_ok=True)

        youtube_video = YouTube(
            video.video_url,
            on_progress_callback=self._handle_progress
        )

        sanitized_title = sanitize_string_to_create_a_folder(youtube_video.title)
        if all_resolution:
            folder_to_save_videos = path_to_save_video / sanitized_title
            folder_to_save_videos.mkdir(parents=True, exist_ok=True)

            for stream in youtube_video.streams.filter(type="video").all():
                video_path = stream.download(
                    folder_to_save_videos,
                    filename_prefix=f"{stream.resolution}_{stream.subtype}_",
                    filename=f"{sanitized_title}.{stream.subtype}",
                    max_retries=10,
                )

                self._handle_video_after_downlaod(video_path, stream, youtube_video)
            return

        if only_best_resolution:
            video_stream = youtube_video.streams.filter(type="video").get_highest_resolution()
        elif only_lowest_resolution:
            video_stream = youtube_video.streams.filter(type="video").get_lowest_resolution()
        else:
            video_stream = youtube_video.streams.filter(
                resolution=resolution.value,
                type="video",
            ).first()
        video_path = video_stream.download(path_to_save_video, filename=f"{sanitized_title}.{video_stream.subtype}")
        self._handle_video_after_downlaod(video_path, video_stream, youtube_video)

    def _handle_video_after_downlaod(self, video_path: str, stream: Stream, youtube_instance: YouTube):
        sanitized_title = sanitize_string_to_create_a_folder(youtube_instance.title)

        video_path_obj = Path(video_path)
        folder_to_save_audios = video_path_obj.parent / "audios"
        folder_to_save_audios.mkdir(parents=True, exist_ok=True)

        is_progressive_stream = stream.is_progressive
        if not is_progressive_stream:
            audio_stream = youtube_instance.streams.filter(type="audio").order_by("abr").desc().first()
            audio_path = folder_to_save_audios / f"{sanitized_title}.{audio_stream.subtype}"
            audio_path_mp3 = folder_to_save_audios / f"{sanitized_title}.mp3"
            audio_already_downloaded = audio_path.exists()
            audio_mp3_already_downloaded = audio_path_mp3.exists()

            if not audio_already_downloaded or not audio_mp3_already_downloaded:
                audio_stream.download(
                    folder_to_save_audios,
                    filename=f"{sanitized_title}.{audio_stream.subtype}"
                )

            if audio_stream.subtype == "webm":
                audio_path_mp3 = convert_webm_audio_to_mp3(audio_path)
            else:
                audio_path_mp3 = convert_any_audio_to_mp3(audio_path, codec=stream.audio_codec)

            self._put_audio_in_video(
                video_path,
                str(audio_path_mp3)
            )

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

    def _put_audio_in_video(self, video_path: str, audio_path: str):
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            new_video_path = Path(video_path)
            new_video_path = new_video_path.parent / f"{new_video_path.stem}_with_audio.mp4"
            new_video_path_str = str(new_video_path)

            video: VideoFileClip = video.set_audio(audio)
            video.write_videofile(new_video_path_str)

            remove_file(video_path)
        except Exception as e:
            err_msg = str(e)

            if "THE SYSTEM CAN NOT FIND THE FILE SPECIFIED" in err_msg.upper():
                # TODO - make program download ffmeg for correct platform if not has it on system
                pass

                return self._put_audio_in_video(video_path, audio_path)

            # file is corrupt, deleting him
            # TODO - identify what file is corrupt and delete him

    def _format_video_info(self, video: PlaylistItem) -> VideoInfo:
        pass
