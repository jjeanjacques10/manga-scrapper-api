import logging
from src.services.save_page_service import upload_chapter_pages
from src.services.mangalivre_service import get_manga_from_mangalivre
from src.services.muitomanga_service import get_manga_from_muitomanga

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def process_message(event):
    source = event.get('source', None)
    manga = event.get('manga', None)
    chapter = str(event.get('chapter', None))
    try:
        process_manga_chapter(source, manga, chapter)
        # upload_chapter_pages(manga, chapter)
    except Exception as e:
        print(e)


def process_manga_chapter(source, manga, chapter):
    if source == "manga_livre":
        print(f"Mangalivre - {manga}")
        get_manga_from_mangalivre(manga, chapter)
    elif source == "muito_manga":
        print(f"Muitomanga - {manga}")
        get_manga_from_muitomanga(manga, chapter)
    else:
        raise Exception("Invalid option")
