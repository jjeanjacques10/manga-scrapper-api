
import os
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_chapter_pages(manga_name, chapter_number):
    folder = f"mangas/{manga_name}/{chapter_number}"

    # Get all images in the folder
    images = os.listdir(folder)

    for img in images:
        # Get the image path
        img_path = os.path.join(folder, img)

        url = "http://ec2-3-86-242-92.compute-1.amazonaws.com/page"

        payload = {
            'source': 'manga_livre',
            'manga': manga_name,
            'number': chapter_number,
            'page': img.split('.')[0]
        }
        files = [
            ('image', ('MangaJJLogo.png', open(img_path, 'rb'), 'image/png'))
        ]
        headers = {}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)

        if response.status_code != 201:
            logger.error(f"Error uploading image {img}")

    logger.info(f"Chapter {chapter_number} uploaded")
