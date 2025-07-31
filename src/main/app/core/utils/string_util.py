"""String utilities."""

import re
from typing import Optional, Any, Collection, Union


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
    return "".join(word.capitalize() for word in snake_str.strip("_").split("_") if word)


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
    return " ".join(word for word in snake_str.strip("_").split("_") if word).capitalize()


def parse_type_params(type_str: str) -> tuple[str, []]:
    """
    Parse type string and return type name and parameters dict

    Args:
        type_str: Type string like 'DECIMAL(10, 2)' or 'BIGINT(display_width=20)' or VARCHAR(20)

    Returns:
        tuple: (type_name, params_dict)
        e.g.: ('decimal', {'precision': 10, 'scale': 2})
    """
    # Match type name and parameters in parentheses
    match = re.match(r"(\w+)\((.*)\)", type_str)
    if not match:
        return type_str, {}

    type_name = match.group(1)
    params_str = match.group(2)

    # Parse parameters
    params = []
    if params_str:
        # Split multiple parameters
        param_pairs = params_str.split(",")
        for pair in param_pairs:
            params.append(pair)

    return type_name, params


class StringUtils:
    @staticmethod
    def is_empty(s: str) -> bool:
        if s is None:
            return True
        return not s.strip()

    @staticmethod
    def to_camel_case(snake_str: str) -> str:
        components = snake_str.split("_")
        return components[0].lower() + "".join(x.title() for x in components[1:])

    @staticmethod
    def to_upper_camel_case(snake_str: str) -> str:
        components = snake_str.split("_")
        return components[0].title() + "".join(x.title() for x in components[1:])

    @staticmethod
    def substring(s: str, start: int, end: int) -> str:
        return s[start:end]

    @staticmethod
    def substring_before(s: str, delimiter: str) -> str:
        return s.split(delimiter)[0]

    @staticmethod
    def substring_between(s: str, start: str, end: str) -> str:
        return s[s.find(start) + 1 : s.rfind(end)]

    @staticmethod
    def ends_with_ignore_case(s: str, suffix: str) -> bool:
        return s.lower().endswith(suffix.lower())

    @staticmethod
    def split(s: str, delimiter: str) -> list[str]:
        if is_empty(s):
            return []
        return s.split(delimiter)

    @staticmethod
    def is_not_empty(s: str) -> bool:
        return not is_empty(s)

    @staticmethod
    def convert_to_string(s: str) -> Optional[list[str]]:
        if is_empty(s):
            return []
        return s.split(",")

    @staticmethod
    def process_code_string(code: str) -> str:
        if is_empty(code):
            return ""
        return code.replace("\\n", "\n")


NULLSTR = ""
SEPARATOR = "_"
ASTERISK = "*"


def nvl(value: Any, default_value: Any) -> Any:
    """Get parameter non-null value."""
    return value if value is not None else default_value


def is_empty(coll: Optional[Collection]) -> bool:
    """Check if a collection is empty."""
    return coll is None or len(coll) == 0


def is_not_empty(coll: Optional[Collection]) -> bool:
    """Check if a collection is not empty."""
    return not is_empty(coll)


def is_empty_array(objects: Optional[list]) -> bool:
    """Check if an array is empty."""
    return objects is None or len(objects) == 0


def is_not_empty_array(objects: Optional[list]) -> bool:
    """Check if an array is not empty."""
    return not is_empty_array(objects)


def is_empty_map(map_obj: Optional[dict]) -> bool:
    """Check if a map is empty."""
    return map_obj is None or len(map_obj) == 0


def is_not_empty_map(map_obj: Optional[dict]) -> bool:
    """Check if a map is not empty."""
    return not is_empty_map(map_obj)


def is_empty_string(string: Optional[str]) -> bool:
    """Check if a string is empty or contains only whitespace."""
    return string is None or string.strip() == NULLSTR


def is_not_empty_string(string: Optional[str]) -> bool:
    """Check if a string is not empty."""
    return not is_empty_string(string)


def is_null(obj: Any) -> bool:
    """Check if an object is null."""
    return obj is None


def is_not_null(obj: Any) -> bool:
    """Check if an object is not null."""
    return obj is not None


def is_array(obj: Any) -> bool:
    """Check if an object is an array type."""
    return isinstance(obj, list)


def trim(string: Optional[str]) -> str:
    """Trim whitespace from a string."""
    return string.strip() if string is not None else NULLSTR


def hide(string: Union[str, None], start_include: int, end_exclude: int) -> str:
    """Replace characters in a specific range with '*'."""
    if is_empty_string(string):
        return NULLSTR
    str_length = len(string)
    if start_include > str_length:
        return NULLSTR
    if end_exclude > str_length:
        end_exclude = str_length
    if start_include > end_exclude:
        return NULLSTR
    return "".join(
        ASTERISK if start_include <= i < end_exclude else c for i, c in enumerate(string)
    )


def substring(string: Optional[str], start: int, end: Optional[int] = None) -> str:
    """Substring of a string."""
    if string is None:
        return NULLSTR
    length = len(string)
    if end is None:
        end = length
    if start < 0:
        start += length
    if end < 0:
        end += length
    if start < 0:
        start = 0
    if end > length:
        end = length
    if start > end:
        return NULLSTR
    return string[start:end]


def has_text(string: Optional[str]) -> bool:
    """Check if a string has text."""
    return bool(string and any(c.isalnum() for c in string))


def format(template: str, *params: Any) -> str:
    """Format text with placeholders."""
    if is_empty_array(params) or is_empty_string(template):
        return template
    # Simple implementation, replace '{}' with parameters
    for param in params:
        template = template.replace("{}", str(param), 1)
    return template


def is_http(link: Optional[str]) -> bool:
    """Check if a link starts with 'http://' or 'https://'."""
    return link.startswith(("http://", "https://")) if link else False


def contains_any(collection: Collection[str], *array: str) -> bool:
    """Check if any element in array is in collection."""
    return any(item in collection for item in array)


def to_under_score_case(string: Optional[str]) -> Optional[str]:
    """Convert camelCase to under_score_case."""
    if string is None:
        return None
    return re.sub(r"([a-z])([A-Z])", r"\1_\2", string).lower()


def matches(string: str, patterns: list[str]) -> bool:
    """Check if a string matches any pattern in a list."""
    if is_empty_string(string) or is_empty(patterns):
        return False
    for pattern in patterns:
        if is_match(pattern, string):
            return True
    return False


def is_match(pattern: str, string: str) -> bool:
    """Check if a URL matches a pattern using simple wildcards."""
    # This function uses shell-style wildcards for matching
    pattern = pattern.replace("**", ".*").replace("*", "[^/]*").replace("?", ".")
    return re.fullmatch(pattern, string) is not None


def convert_to_camel_case(name: Optional[str]) -> str:
    """Convert under_score_case to CamelCase."""
    if not name or not name.strip():
        return ""
    if "_" not in name:
        return name[0].upper() + name[1:]
    parts = name.split("_")
    return "".join(part.capitalize() for part in parts if part)


def to_camel_case(s: Optional[str]) -> Optional[str]:
    """Convert under_score_case to camelCase."""
    if s is None:
        return None
    if SEPARATOR not in s:
        return s
    parts = s.split(SEPARATOR)
    # Join parts, capitalizing each part except the first
    return parts[0] + "".join(word.capitalize() for word in parts[1:])
