import logging
from flask import request, Blueprint
from services.manga_service import MangaService


chapter_bp = Blueprint('chapter_bp', __name__)

"""Get all pages from a chapter"""


@chapter_bp.route("/chapter", methods=["GET"])
def get_all_chapter_pages():
    source = request.args.get("source", None)
    manga = request.args.get("manga", None)
    number = request.args.get("number", None)

    logging.info(f"{source}, {manga}, {number}")

    if not source or not manga or not number:
        return {"message": "Invalid request"}, 422

    mangaService = MangaService()

    images = mangaService.get_chapter_local(source, manga, number)

    if not images:
        images = mangaService.get_chapter_from_internet(source, manga, number, False)
        #return {"message": "Chapter not found"}, 404

    return {
        "manga": manga,
        "chapter": number,
        "pages": images
    }, 200
