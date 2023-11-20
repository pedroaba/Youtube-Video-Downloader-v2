import os
from pathlib import Path

from dotenv import load_dotenv
from youtube_video_downloader.core.playlist import Playlist


load_dotenv()

API_KEY = os.getenv("MY_YOUTUBE_API_KEY", None)
playlist = Playlist(API_KEY)

playlist.download_all_videos_of_playlist(
    playlist_id="PLqjhHHte7WL_GNHB1qpnTVk1p9ztz-mbc",
    path_to_save_videos=(Path(".") / "videos")
)
