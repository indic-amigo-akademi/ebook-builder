from ebooklib import epub
import markdown
import yaml
import os
from bs4 import BeautifulSoup


def parse_markdown_with_yaml(file_path):
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

    yaml_data["filename"] = file_path.split("\\")[-1].split(".")[0] + ".epub"

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_part)

    return yaml_data, html_content


def create_book(data, content):
    book = epub.EpubBook()
    lang = data.get("language", "en")
    book.set_identifier(data.get("id", ""))
    book.set_title(data.get("title", ""))
    book.set_language(lang)
    book.add_author(data.get("author", ""))

    filename = os.path.join("books", data.get("filename", "book.epub"))

    soup = BeautifulSoup(content, "lxml")

    chapters = []
    for element in soup.recursiveChildGenerator():
        if element.name == "h2":
            chapter = epub.EpubHtml(
                title=element.text,
                file_name="chapter_{:05d}.xhtml".format(len(chapters)),
            )
            chapter.content = str(element)
            chapters.append(chapter)
        if element.name == "p":
            chapters[-1].content += str(element)

    # Add chapters to the book
    for chapter in chapters:
        book.add_item(chapter)

    # define Table Of Contents
    book.toc = tuple(
        [
            epub.Link(chapter.get_name(), chapter.title, chapter.title)
            for chapter in chapters
        ]
    )

    with open("styles/style.css", "r", encoding="utf-8") as file:
        style = file.read()

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="styles/style.css",
        media_type="text/css",
        content=style,
    )
    book.add_item(nav_css)

    # basic spine
    book.spine = ["nav", *chapters]

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav(title="সূচিপত্র" if lang == "bn" else "Table of Contents"))

    epub.write_epub(filename, book, {})


if not os.path.exists("books"):
    os.makedirs("books")

# Process all Markdown files in the "books" directory
for path in os.listdir("books"):
    if not path.endswith(".md"):
        continue
    path = os.path.join("books", path)
    print(f"Processing {path}...")
    # Parse the Markdown file with YAML front matter
    yaml_data, html_content = parse_markdown_with_yaml(path)
    create_book(yaml_data, html_content)
print("All books have been created.")
