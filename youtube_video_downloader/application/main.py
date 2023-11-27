from youtube_video_downloader.application.tray.menu import TrayMenu
from youtube_video_downloader.configs import application_config

icon = "icon.ico" if application_config.running_os == "windows" else "icon.png"
tray = TrayMenu(
    name=application_config.app_name,
    _icon=str(
        (
                application_config.current_execution_path / "assets" / icon
        ).absolute()
    ),
    menu_items=[
        "Download Video",
        "Playlist"
    ]
)

tray.main_loop()
