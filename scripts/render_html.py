from pathlib import Path


def render_html(
    template_file: Path,
    output_file: Path,
    replacements: dict
):
    html = template_file.read_text(
        encoding="utf-8"
    )

    for key, value in replacements.items():
        html = html.replace(
            f"@@{key}@@",
            value
        )

    output_file.write_text(
        html,
        encoding="utf-8"
    )