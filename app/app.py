import os
from flask import Flask, request, send_file
from flask_cors import CORS
from utils.manga_utils import get_folder_name

from producer.producer import send_message

app = Flask(__name__)

HOST_API = os.environ.get("HOST_API", "http://localhost:3000")


@app.route("/page", methods=["POST"])
def save_page():
    """Save a image to the folder"""
    source = request.form.get("source", None)
    manga = request.form.get("manga", None)
    number = request.form.get("number", None)
    page = request.form.get("page", "1")

    # remove characters that are not numbers from page
    page = ''.join(filter(str.isdigit, page))

    print(source, manga, number, page)

    if not source or not manga or not number:
        return {"message": "Invalid request"}, 422

    image = request.files["image"]

    folder = get_folder_name(manga, number)
    if not os.path.exists(folder):
        os.makedirs(folder)

    image.save(os.path.join(folder, f"{page}.{'png' if source == 'manga_livre' else 'jpg'}"))
    return {
        "message": "Image saved"
    }, 201


@app.route("/page", methods=["GET"])
def get_page():
    """Get a image from the folder"""
    source = request.args.get("source", None)
    manga = request.args.get("manga", None)
    number = request.args.get("number", None)
    page = request.args.get("page", "1")

    print(source, manga, number, page)

    if not source or not manga or not number:
        return {"message": "Invalid request"}, 422

    folder = get_folder_name(manga, number)
    if not os.path.exists(folder):
        return {"message": "Page not found"}, 404

    # try png first then jpg
    try:
        image = open(os.path.join(folder, f"{page}.{'png' if source == 'manga_livre' else 'jpg'}"), "rb")
    except FileNotFoundError:
        image  = open(os.path.join(folder, f"{page}.{'jpg' if source == 'manga_livre' else 'png'}"), "rb")

    return send_file(image, mimetype='image/jpeg'), 200


@app.route("/chapter", methods=["GET"])
def get_all_chapter_pages():
    """Get all pages from a chapter"""
    source = request.args.get("source", None)
    manga = request.args.get("manga", None)
    number = request.args.get("number", None)

    print(source, manga, number)

    if not source or not manga or not number:
        return {"message": "Invalid request"}, 422

    folder = get_folder_name(manga, number)
    if not os.path.exists(folder):
        send_message({
            "source": source,
            "manga": manga,
            "chapter": number
        })
        return {"message": "Chapter not found"}, 404

    images = os.listdir(folder)

    for i, img in enumerate(images):
        images[
            i] = f"{HOST_API}/page?source={source}&manga={manga}&number={number}&page={img.split('.')[0]}"

    return {
        "manga": manga,
        "chapter": number,
        "pages": images
    }, 200


def main():
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
