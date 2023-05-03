import os
from services.producer_processor import send_message

from services.mangalivre_service import get_manga_from_mangalivre
from services.muitomanga_service import get_manga_from_muitomanga
from utils.manga_utils import get_folder_name

HOST_API = os.environ.get("API_HOST", "http://localhost:3000")


class MangaService:

    def __init__(self) -> None:
        pass

    def get_chapter_local(self, source: str, manga: str, chapter: str):
        folder = get_folder_name(manga, chapter)
        if not os.path.exists(folder):
            send_message({
                "source": source,
                "manga": manga,
                "chapter": chapter
            })
            return None

        images = os.listdir(folder)

        for i, img in enumerate(images):
            images[
                i] = f"{HOST_API}/page?source={source}&manga={manga}&number={chapter}&page={img.split('.')[0]}"
        return self.order_pages(images)

    def get_chapter_from_internet(self, source: str, manga: str, chapter: str, download_pages: bool):
        if source == "manga_livre":
            print(f"Mangalivre - {manga}")
            return get_manga_from_mangalivre(manga, chapter, download_pages)
        elif source == "muito_manga":
            print(f"Muitomanga - {manga}")
            return get_manga_from_muitomanga(manga, chapter, download_pages)
        else:
            raise Exception("Invalid option")

    def order_pages(self, pages: list):
        pages.sort(key=lambda x: int(x.split("=").pop().split("_")[0]))
        return pages
