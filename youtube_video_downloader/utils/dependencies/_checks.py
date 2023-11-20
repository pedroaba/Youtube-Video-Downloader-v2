from subprocess import CalledProcessError, PIPE, run


def _check_packages_are_installed(commands: list[str]) -> bool:
    try:
        run(
            commands,
            stdout=PIPE,
            stderr=PIPE,
            check=True
        )

        return True
    except CalledProcessError:
        return False
