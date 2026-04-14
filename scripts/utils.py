import os
import markdown
import yaml
from bs4 import BeautifulSoup


def get_credits(data):
    credit_str = ""
    for credit in data.get("credits", []):
        if isinstance(credit, dict):
            credit_str += f"<a href='{credit.get('url', '')}'>{credit.get('name', '')}</a> - {credit.get('role', '')}<br>"
        elif isinstance(credit, str):
            credit_str += f"{credit}<br>"
    credit_str = credit_str.strip()
    return credit_str


def extract_title(md: str) -> str | None:
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find(["h1", "h2", "h3"])
    return heading.get_text(strip=True) if heading else None


DEFAULT_EXTENSION = ".epub"


def parse_markdown_with_yaml(file_path, extension=DEFAULT_EXTENSION):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split YAML front matter and Markdown content
    if content.startswith("---"):
        _, yaml_part, markdown_part = content.split("---", 2)
    else:
        yaml_part = ""
        markdown_part = content

    # Parse YAML
    yaml_data = yaml.safe_load(yaml_part)
    yaml_data["filename"] = file_path.split(os.path.sep)[-1].split(".")[0] + extension
    page_break = yaml_data.get("page_break", "<!-- pagebreak -->")
    yaml_data["credits"] = get_credits(yaml_data)

    # Remove YAML front matter
    chapters_md = markdown_part.split(page_break)

    chapters_html = []

    for chapter_md in chapters_md:
        if chapter_md.strip() == "":
            continue
        # Convert Markdown to HTML
        chapters_html.append(
            {
                "title": extract_title(chapter_md),
                "content": markdown.markdown(
                    chapter_md,
                    extensions=["footnotes"],
                )
            }
        )

    return yaml_data, chapters_html
