PLACEHOLDERS = [
    "@@CRYSTAL_DATA@@",
    "@@APP_VERSION@@"
]

from src.template_constants import PLACEHOLDERS

def validate_html(html_path):
    text = html_path.read_text(
        encoding="utf-8"
    )

    for token in PLACEHOLDERS:
        if token in text:
            raise RuntimeError(
                f"Placeholder não substituído: {token}"
            )