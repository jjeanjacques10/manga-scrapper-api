from src.services.manga_service import MangaService
from src.services.save_page_service import upload_chapter_pages


def process_message(event):
    source = event.get('source', None)
    manga = event.get('manga', None)
    chapter = str(event.get('chapter', None))
    try:
        manga_service = MangaService()
        manga_service.get_chapter_from_internet(source, manga, chapter, True)
        upload_chapter_pages(manga, chapter)
    except Exception as e:
        print(e)
