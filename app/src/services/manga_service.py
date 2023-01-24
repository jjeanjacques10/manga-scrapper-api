import os
from src.producer.producer import send_message
from src.services.mangalivre_service import get_manga_from_mangalivre
from src.services.muitomanga_service import get_manga_from_muitomanga
from utils.manga_utils import get_folder_name

HOST_API = os.environ.get("API_HOST", "http://localhost:3000")

class MangaService:

    def __init__(self) -> None:
        pass

    def get_chapter(self, source: str, manga: str, chapter: str):
        folder = get_folder_name(manga, chapter)
        if not os.path.exists(folder):
            send_message({
                "source": source,
                "manga": manga,
                "chapter": chapter
            })
            return self.get_chapter_from_internet(source, manga, chapter)

        images = os.listdir(folder)

        for i, img in enumerate(images):
            images[
                i] = f"{HOST_API}/page?source={source}&manga={manga}&number={chapter}&page={img.split('.')[0]}"
        return images


    def get_chapter_from_internet(self, source: str, manga: str, chapter: str):
        if source == "manga_livre":
            print(f"Mangalivre - {manga}")
            return get_manga_from_mangalivre(manga, chapter, save_pages=False)
        elif source == "muito_manga":
            print("Implement this - muito_manga")
        else:
            raise Exception("Invalid option")