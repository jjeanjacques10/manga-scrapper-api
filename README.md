# Manga Page Scraper

<p align="center">
    <img src="https://raw.githubusercontent.com/jjeanjacques10/mangajj/main/files/MangaJJLogo.jpg" width="300"/>
    <br />
    <br />
    <a href="https://github.com/jjeanjacques10/manga-scrapper-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/jjeanjacques10/manga-scrapper-api/issues">Request Feature</a>
</p>

This is a simple script to scrape manga pages from a websites and save them to a folder on AWS EC2 instance. There is an api and a consumer, the api is a Flask app that takes a chapter from a manga and if not already scraped, send a message to the consumer SQS to scrape the pages.

## SQS Queue

SQS Message

``` json
{
    "source": "manga_livre",
    "manga": "Naruto",
    "chapter": "692"
}
```

## Endpoints

- Get a single chapter page

`GET /page`

| Query Param   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `source` | `string` | **Required**. manga_livre or muito_manga |
| `manga` | `string` | **Required**. manga name |
| `number` | `string` | **Required**. chapter number |
| `page` | `string` | **Required**. page number |

- Save a single chapter page on EBS

`POST /page`

| Form   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `source` | `string` | **Required**. manga_livre or muito_manga |
| `manga` | `string` | **Required**. manga name |
| `number` | `string` | **Required**. chapter number |
| `page` | `string` | **Required**. number of pages |
| `image` | `file` | **Required**. image file |

- Get a chapter

`GET /chapter`

| Query Param   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `source` | `string` | **Required**. manga_livre or muito_manga |
| `manga` | `string` | **Required**. manga name |
| `number` | `string` | **Required**. chapter number |

## Sites Supported

- [Manga Livre](https://mangalivre.net/)
- [Muito Manga](https://muitomanga.com/)

## Architecture

<img src="./files/diagram.jpg" width=600>

## GitHub Actions

- Variables to be set in the repository secrets

``` bash
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
AWS_SECURITY_GROUP =
SSH_PRIVATE_KEY=
HOSTNAME=
USERNAME=
```

- Workflow to deploy to EC2 instance

> [.github/workflows/deploy.yml](.github/workflows/deploy.yml)

- Script to config the EC2 instance, install docker, update nginx and run the container

> [app.sh](app.sh)

## Run Locally

Use docker-compose to run both the api and the consumer

``` bash
docker-compose up --build --scale manga_consumer=10 -d
```

```--scale manga_consumer=10``` will run 10 consumers in parallel

## Licença

[MIT](https://choosealicense.com/licenses/mit/)

---
Developed by [Jean Jacques Barros](https://github.com/jeanjacques10)
