"""String utilities."""


def snake_to_pascal(snake_str: str) -> str:
    """Convert a snake_case string to PascalCase.

    Args:
        snake_str: A string in snake_case format.

    Returns:
        A string converted to PascalCase.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(snake_str, str):
        raise TypeError("Input must be a string")
    return ''.join(word.capitalize() for word in snake_str.strip('_').split('_') if word)


def snake_to_title(snake_str: str) -> str:
    """Convert a snake_case string to a space-separated title-style string.

    Args:
        snake_str: A string in snake_case format.

    Returns:
        A string with each word capitalized and separated by spaces.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(snake_str, str):
        raise TypeError("Input must be a string")
    return ' '.join(word for word in snake_str.strip('_').split('_') if word).capitalize()
