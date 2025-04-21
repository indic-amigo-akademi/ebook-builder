import os
from utils import parse_markdown_with_yaml


def create_book_html(data, contents, author):
    folder = os.path.join("build", author)
    # Check if the folder exists, if not create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join("partials", "base.html")) as f:
        base_html = f.read()

    # Create the HTML content
    html_content = base_html.format(
        title=data.get("title", "Book Title")
        + " - "
        + data.get("author", "Author Name"),
        lang=data.get("lang", "en"),
        content=contents,
    )

    # Create the HTML file for the book
    filename = os.path.join(folder, data.get("filename", "book.html"))
    try:
        f.write(html_content)
    except Exception as e:
        print(f"Error writing to file: {e}")
    print(f"Created {filename}")


def create_author_html(booknames):
    folder = os.path.join("build", author)
    # Check if the folder exists, if not create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join("partials", "base.html")) as f:
        base_html = f.read()

    contents = ""
    for book in booknames:
        contents += f"<li><a href='{book['filename']}'>{book['title']}</a></li>"
    contents = f"<h1>{booknames[0]['author']}</h1><ul>{contents}</ul>"

    # Create the HTML content
    html_content = base_html.format(
        title=booknames[0]["author"],
        lang="en",
        content=contents,
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

            # Create the book HTML content
            create_book_html(
                yaml_data,
                "\n".join(chapters_html),
                author,
            )
            booknames.append(
                {
                    "title": yaml_data.get("title", "Book Title"),
                    "author": yaml_data.get("author", "Author Name"),
                    "filename": "/"
                    + author
                    + "/"
                    + yaml_data.get("filename", "book.html"),
                }
            )

        # Create the author HTML file
        create_author_html(booknames)
        authornames.append(
            {
                "author": booknames[0]["author"],
                "filename": "/" + author + "/index.html",
            }
        )

    # Create the main HTML file
    create_main_html(authornames)

    print("All books have been processed.")
