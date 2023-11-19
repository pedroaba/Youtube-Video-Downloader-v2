import os

from dotenv import load_dotenv
from youtube_video_downloader.core.playlist import Playlist


load_dotenv()

API_KEY = os.getenv("MY_YOUTUBE_API_KEY", None)
playlist = Playlist(API_KEY)

videos = playlist.retrieve_videos_info(playlist_id="PLqjhHHte7WL_GNHB1qpnTVk1p9ztz-mbc")
print(videos)
