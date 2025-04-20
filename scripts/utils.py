import os
import markdown
import yaml

def get_credits(data):
    credit_str = ""
    for credit in data.get("credits", []):
        if isinstance(credit, dict):
            credit_str += f"<a href='{credit.get('url', '')}'>{credit.get('name', '')}</a> - {credit.get('role', '')}<br>"
        elif isinstance(credit, str):
            credit_str += f"{credit}<br>"
    credit_str = credit_str.strip()
    return credit_str


def parse_markdown_with_yaml(file_path, extension=".epub"):
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

    chapters_md = markdown_part.split(page_break)

    chapters_html = []

    for chapter_md in chapters_md:
        if chapter_md.strip() == "":
            continue
        # Convert Markdown to HTML
        chapters_html.append(
            markdown.markdown(
                chapter_md,
                extensions=["footnotes"],
            )
        )

    return yaml_data, chapters_html
