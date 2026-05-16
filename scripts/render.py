# scripts/render.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "j2"]),
)


def render_digest(digest: dict) -> str:
    template = _env.get_template("digest.html.j2")
    return template.render(**digest)
