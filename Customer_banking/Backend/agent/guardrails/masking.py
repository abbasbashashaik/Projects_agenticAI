import re
from langchain_core.tools import tool


def mask_value(value: str | None) -> str | None:
    """Keep the last four digits visible."""
    if not value:
        return value

    digits = re.sub(r"\D", "", value)

    if len(digits) <= 4:
        return "*" * len(digits)

    return "*" * (len(digits) - 4) + digits[-4:]
