import os
import shutil
from utils import parse_markdown_with_yaml
from argparse import ArgumentParser

SUB_URL = "book-reader/"


def create_book_html(data, contents, author):
    folder = os.path.join("build", author)
    # Check if the folder exists, if not create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join("partials", "base.html")) as f:
        base_html = f.read()

    url = os.path.join("/", SUB_URL, author)

    # Create the HTML content
    html_content = base_html.format(
        title=data.get("title", "Book Title")
        + " - "
        + data.get("author", "Author Name"),
        lang=data.get("lang", "en"),
        content=contents,
        header_content=f"<a href='{url}'>&larr; Back</a>",
        sub_url="/" + SUB_URL,
    )

    # Create the HTML file for the book
    filename = os.path.join(folder, data.get("filename", "book.html"))
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created {filename}")


def create_author_html(booknames):
    folder = os.path.join("build", author)
    # Check if the folder exists, if not create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join("partials", "base.html")) as f:
        base_html = f.read()

    url = os.path.join("/", SUB_URL)

    contents = ""
    for book in booknames:
        contents += f"<li><a href='{book['filename']}'>{book['title']}</a></li>"
    contents = f"<h1>{booknames[0]['author']}</h1><ul>{contents}</ul>"

    # Create the HTML content
    html_content = base_html.format(
        title=booknames[0]["author"],
        lang="en",
        content=contents,
        header_content=f"<a href='{url}'>&larr; Back</a>",
        sub_url="/" + SUB_URL,
    )

    # Create the HTML file for the book
    filename = os.path.join(folder, "index.html")
    with open(filename, "w") as f:
        f.write(html_content)
    print(f"Created {filename}")


def create_main_html(authornames):
    folder = os.path.join("build")
    # Check if the folder exists, if not create it
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join("partials", "base.html")) as f:
        base_html = f.read()

    contents = ""
    for author in authornames:
        contents += f"<li><a href='{author['filename']}'>{author['author']}</a></li>"
    contents = f"<h1>Authors</h1><ul>{contents}</ul>"

    # Create the HTML content
    html_content = base_html.format(
        title="Authors",
        lang="en",
        content=contents,
        header_content="",
        sub_url="/" + SUB_URL,
    )
    # Create the HTML file for the book
    filename = os.path.join(folder, "index.html")
    with open(filename, "w") as f:
        f.write(html_content)
    print(f"Created {filename}")


if __name__ == "__main__":
    if not os.path.exists("books"):
        os.makedirs("books")
    if not os.path.exists("build"):
        os.makedirs("build")

    parser = ArgumentParser()
    parser.add_argument("--dev", action="store_true")
    parser.add_argument("--appname", type=str, default="")

    args = parser.parse_args()

    if args.dev:
        SUB_URL = ""
    elif args.appname:
        SUB_URL = args.appname + "/"

    # Process all Markdown files in the "books" directory
    authornames = []
    for author in os.listdir("books"):
        booknames = []
        for bookname in os.listdir(os.path.join("books", author)):
            path = os.path.join("books", author, bookname)
            if not path.endswith(".md"):
                continue
            print(f"Processing {path}...")
            # Parse the Markdown file with YAML front matter
            yaml_data, chapters_html = parse_markdown_with_yaml(path, extension=".html")

            page_counter = 0
            # Create the book HTML content
            chapters_html_content = ""
            # Add cover page if cover image present
            if yaml_data.get("cover", "") != "":
                with open(os.path.join("partials", "cover.html")) as f:
                    cover_html = f.read()
                cover_html_content = cover_html.format(
                    cover_image=os.path.join(
                        "/", SUB_URL, yaml_data.get("cover", "")
                    )
                )
                chapters_html_content += f"<div class='page'>{cover_html_content}</div>"
                page_counter += 1

            # Add title page
            with open(os.path.join("partials", "title.html")) as f:
                title_html = f.read()
            title_html_content = title_html.format(
                title=yaml_data.get("title", "Book Title"),
                author=yaml_data.get("author", "Author Name"),
                language=yaml_data.get("language", ""),
                publisher="Indic Amigo Akademia",
            )
            chapters_html_content += f"<div class='page'>{title_html_content}</div>"
            page_counter += 1

            # Add table of contents
            toc_html = "<h1>Table of Contents</h1><ul>"
            page_counter += 1
            for chapter in chapters_html:
                toc_html += f"<li><a href='/{SUB_URL}{author}/{yaml_data.get('filename', 'book.html').replace('.html', '')}?page={page_counter+1}'>{chapter['title']}</a></li>"
                page_counter += 1
            toc_html += "</ul>"
            chapters_html_content += f"<div class='page'>{toc_html}</div>"

            for chapter in chapters_html:
                chapters_html_content += f"<div class='page'>{chapter['content']}</div>"
            create_book_html(
                yaml_data,
                chapters_html_content,
                author,
            )
            booknames.append(
                {
                    "title": yaml_data.get("title", "Book Title"),
                    "author": yaml_data.get("author", "Author Name"),
                    "filename": "/"
                    + SUB_URL
                    + author
                    + "/"
                    + yaml_data.get("filename", "book.html"),
                }
            )

        if len(booknames) == 0:
            continue
        booknames.sort(key=lambda x: x["filename"])

        # Create the author HTML file
        create_author_html(booknames)
        authornames.append(
            {
                "author": booknames[0]["author"],
                "filename": "/" + SUB_URL + author + "/index.html",
            }
        )

    # Create the main HTML file
    create_main_html(authornames)

    # Copy styles
    if not os.path.exists("build/styles"):
        os.makedirs("build/styles")
    shutil.copyfile(
        os.path.join("assets", "styles", "style.css"),
        os.path.join("build", "styles", "style.css"),
    )

    # Copy scripts
    if not os.path.exists("build/scripts"):
        os.makedirs("build/scripts")
    shutil.copyfile(
        os.path.join("assets", "scripts", "script.js"),
        os.path.join("build", "scripts", "script.js"),
    )

    # Copy favicon
    shutil.copytree(
        os.path.join("assets", "favicon"),
        os.path.join("build", "favicon"),
        dirs_exist_ok=True,
    )
    shutil.copyfile(
        os.path.join("assets", "manifest.json"),
        os.path.join("build", "manifest.json"),
    )

    # Copy images
    if not os.path.exists("build/images"):
        os.makedirs("build/images")
    shutil.copytree(
        os.path.join("assets", "images"),
        os.path.join("build", "images"),
        dirs_exist_ok=True,
    )

    print("All books have been processed.")
