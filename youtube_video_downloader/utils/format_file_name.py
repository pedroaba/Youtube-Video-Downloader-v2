from cleantext import clean


ALLOWED_SYMBOLS = [" ", "_", "-"]


def remove_emojis(text: str) -> str:
    return clean(text, no_emoji=True)


def sanitize_string_to_create_a_folder(text: str) -> str:
    text = remove_emojis(text)
    sanitized_string = filter(
        lambda character: str(character).isalnum() or character in ALLOWED_SYMBOLS,
        text
    )

    sanitized_string = list(sanitized_string)
    return "".join(sanitized_string)
