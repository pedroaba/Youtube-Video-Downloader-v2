from pathlib import Path
from dataclasses import dataclass

from appdata import AppDataPaths


APP_NAME = "YoutubeVideoDownloader"


@dataclass(frozen=True, init=False)
class AppConfig:
    app_name: str = APP_NAME
    _app_data = AppDataPaths(APP_NAME)

    @property
    def log_folder(self) -> Path:
        return Path(self._app_data.logs_path)

    @property
    def app_folder(self) -> Path:
        return Path(self._app_data.app_data_path)

    @property
    def config_file(self) -> Path:
        return Path(self._app_data.config_path)

    @property
    def temp_folder(self) -> Path:
        temp_folder = self.app_folder / "temp"
        if not temp_folder.exists():
            temp_folder.mkdir(exist_ok=True)
        return temp_folder

    def get_log_filepath(self, filename: str, *, _extra_folders: list[str] = None) -> Path:
        filepath = self.log_folder
        if _extra_folders is not None:
            for folder in _extra_folders:
                filepath /= folder
        return filepath / filename

    def __repr__(self):
        return f"<App appname='{self.app_name}'>"
