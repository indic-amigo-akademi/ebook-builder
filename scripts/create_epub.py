from ebooklib import epub
from utils import parse_markdown_with_yaml
import os
from bs4 import BeautifulSoup
from datetime import datetime
from i18n_constants import i18n



def get_epub_html_from_xml(xml_path, title=None, uid=None, data=None):
    with open(xml_path, "r", encoding="utf-8") as file:
        content = file.read()

    if data is not None:
        content = content.format(**data)

    filename = xml_path.split(os.path.sep)[-1].split(".")[0] + ".xhtml"
    return epub.EpubHtml(title=title, content=content, file_name=filename, uid=uid)


def create_book_epub(data, contents):
    filename = os.path.join("output", data.get("filename", "book.epub"))
    # Check if the file already exists
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping.")
        return

    lang = data.get("lang", "en")
    title = data.get("title", "Book Title")
    author = data.get("author", "Author Name")
    release_date = datetime.now().strftime("%B %d, %Y")
    data["release_date"] = release_date
    data["language"] = i18n[lang]["language"]

    book = epub.EpubBook()
    book.set_identifier(data.get("id", ""))
    book.set_title(title)
    book.set_language(lang)
    book.add_author(author)

    # Add cover image if provided
    cover_image = data.get("cover")
    if cover_image:
        with open(cover_image, "rb") as img_file:
            book.add_item(
                epub.EpubImage(
                    uid="cover_photo",
                    file_name="cover.jpg",
                    content=img_file.read(),
                )
            )
        cover_item = epub.EpubCoverHtml(
            file_name="cover.xhtml", image_name="cover.jpg", title=title, uid="00000_cover"
        )
        book.add_item(cover_item)

    # Get Copyright HTML
    copyright_item = get_epub_html_from_xml(
        os.path.join("partials", "copyright.html"),
        f"{i18n[lang]['copyright']}: {title}",
        data=data,
        uid="00001_copyright",
    )
    book.add_item(copyright_item)

    chapters = []

    for i, chapter_content in enumerate(contents):
        soup = BeautifulSoup(chapter_content, "lxml")
        chapter = epub.EpubHtml(
            title=(
                soup.find("h2").text
                if soup.find("h2")
                else "{} {}".format(i18n[lang]["chapter"], i + 1)
            ),
            lang=lang,
            content=str(soup),
            file_name="ch_{:05d}.xhtml".format(i),
            uid="{:05d}_chapter".format(i+2),
        )
        chapters.append(chapter)
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
    book_spine = []
    if cover_image is not None:
        book_spine.append(cover_item)
    book_spine.extend(
        [
            copyright_item,
            "nav",
            *chapters,
        ]
    )
    book.spine = book_spine

    # add default Ncx and Nav file
    ncx = epub.EpubNcx()
    nav = epub.EpubNav(title=i18n[lang]["toc"], uid="nav")
    book.add_item(ncx)
    book.add_item(nav)

    epub.write_epub(filename, book, {})
    print(f"Created {yaml_data['filename']}.")


if __name__ == "__main__":
    if not os.path.exists("books"):
        os.makedirs("books")

    # Process all Markdown files in the "books" directory
    for author in os.listdir("books"):
        for bookname in os.listdir(os.path.join("books", author)):
            path = os.path.join("books", author, bookname)
            if not path.endswith(".md"):
                continue
            print(f"Processing {path}...")
            # Parse the Markdown file with YAML front matter
            yaml_data, chapters_html = parse_markdown_with_yaml(path)
            create_book_epub(yaml_data, chapters_html)
    print("All books have been created.")
