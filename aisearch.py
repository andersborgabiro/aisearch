import pathlib
import html


# Generate HTML markup with scaled images and links to full size images
def build_markup(path):
    path_url = pathlib.Path(path).as_uri()

    markup = ""
    markup += "<div>"
    markup += "<a href='" + html.escape(path_url) + "' target='_blank'>"
    markup += (
        "<img src='"
        + html.escape(path_url)
        + "' style='max-width: 320px; max-height: 320px;'/>"
    )
    markup += "<br/>"
    markup += html.escape(path)
    markup += "</a>"
    markup += "</div>"
    markup += "\n"

    return markup


path = input("Image path: ")

print("Indexing '" + path + "'...")

from image_searcher import Search

searcher = Search(image_dir_path=path, traverse=True, include_faces=False)

from PIL import Image

while True:
    search_criteria = input("Search terms or 'x': ")
    if search_criteria == "x":
        break

    if search_criteria == "":
        continue

    search_amount = 100
    search_amount_text = input("Amount (100): ")
    if search_amount_text != "":
        try:
            search_amount = int(search_amount_text)
        except:
            pass

    ranked_images = searcher.rank_images(search_criteria, n=search_amount)

    print(str(len(ranked_images)) + " ranked images")

    result = []
    for image in ranked_images:
        result.append(image.image_path)

    title = (
        "Searching for '"
        + search_criteria
        + "' resulting in "
        + str(len(result))
        + " pictures of max "
        + str(search_amount)
    )
    file_name = title + ".html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("<h2>" + title + "</h2>")
        for item in result:
            f.write(build_markup(item))

    print("Created " + file_name)

print("Thanks for using image search. We hope to see you again.")
