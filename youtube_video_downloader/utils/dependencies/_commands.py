class Command:
    def __init__(self, command: str, is_main_command: bool):
        self.__command = command
        self.__main_command = is_main_command

    @property
    def command(self) -> str:
        return self.__command

    @property
    def main_command(self) -> bool:
        return self.__main_command
