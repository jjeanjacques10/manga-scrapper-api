import os
import logging
from flask import request, send_file, Blueprint
from utils.manga_utils import get_folder_name

page_bp = Blueprint('page_bp', __name__)

"""Save a image to the folder"""


@page_bp.route("/page", methods=["POST"])
def save_page():
    source = request.form.get("source", None)
    manga = request.form.get("manga", None)
    number = request.form.get("number", None)
    page = request.form.get("page", "1")

    # remove characters that are not numbers from page
    page = ''.join(filter(str.isdigit, page))

    logging.info(f"{source}, {manga}, {number}, {page}")

    if not source or not manga or not number:
        return {"message": "Invalid request"}, 422

    image = request.files["image"]

    folder = get_folder_name(manga, number)
    if not os.path.exists(folder):
        os.makedirs(folder)

    image.save(os.path.join(
        folder, f"{page}.{'png' if source == 'manga_livre' else 'jpg'}"))
    return {
        "message": "Image saved"
    }, 201


"""Get a image from the folder"""


@page_bp.route("/page", methods=["GET"])
def get_page():
    source = request.args.get("source", None)
    manga = request.args.get("manga", None)
    number = request.args.get("number", None)
    page = request.args.get("page", "1")

    logging.info(f"{source}, {manga}, {number}, {page}")

    if not source or not manga or not number:
        return {"message": "Invalid request"}, 422

    folder = get_folder_name(manga, number)
    if not os.path.exists(folder):
        return {"message": "Page not found"}, 404

    # try png first then jpg
    try:
        image = open(os.path.join(
            folder, f"{page}.{'png' if source == 'manga_livre' else 'jpg'}"), "rb")
    except FileNotFoundError:
        image = open(os.path.join(
            folder, f"{page}.{'jpg' if source == 'manga_livre' else 'png'}"), "rb")

    return send_file(image, mimetype='image/jpeg'), 200
