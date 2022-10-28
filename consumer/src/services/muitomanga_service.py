import logging
import multiprocessing
from multiprocessing import Process
import os

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def search_manga(manga_name):
    url = f"https://muitomanga.com/buscar?q={manga_name}"

    headers = {
        'Cookie': 'PHPSESSID=pt9g3ip57qeearso69ocvvh2lv'
    }

    response = requests.get(url, headers=headers, data={})

    soup = BeautifulSoup(response.text, 'html.parser')
    mangas = []
    i = 0
    for manga in soup.find_all("div", {"class": "anime"}):
        i = i + 1
        mangas.append([
            i,
            manga.find("a").get("href").split("/")[-1]
        ])
    return mangas


def get_chapter(manga_name, chapter_number):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # Try to get 30 pages (max)
    pages = []
    for page in range(1, 30):
        p = Process(target=download_page, args=(
            manga_name, chapter_number, page, return_dict))
        pages.append(p)
        p.start()

    for page in pages:
        page.join()

    return return_dict.values()


def download_page(manga_name, chapter_number, page):
    url = f"https://imgs.muitomanga.com/imgs/{manga_name}/{chapter_number}/{page}.jpg"
    response = requests.get(url)

    # Create folder if not exists
    folder = f"mangas/{manga_name}/{chapter_number}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    if response.status_code == 200:
        print(f"Downloading {manga_name} {chapter_number} page {page}")
        with open(f"{folder}/{page}.jpg", "wb") as f:
            f.write(response.content)
        return url
    else:
        print(f"Page {page} not found")
        return


def get_manga_from_muitomanga(name, chapter):
    mangas = search_manga(name.replace(" ", "+"))

    if len(mangas) == 0:
        logger.error("Manga não encontrado")
        raise Exception("Manga não encontrado")

    id_manga = mangas[0][0]
    logger.info(f"Manga encontrado: {id_manga}")
    manga_name = mangas[id_manga][1]
    logger.info(f"Nome do manga: {manga_name}")

    logger.info(f"Downloading {manga_name} chapter {chapter}")
    get_chapter(manga_name, chapter)
