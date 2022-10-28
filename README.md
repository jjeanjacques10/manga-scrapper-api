# Manga Page Scraper

This is a simple script to scrape manga pages from a websites and save them to a folder on AWS EC2 instance.

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

```http
  GET /page
```

| Query Param   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `source` | `string` | **Required**. manga_livre or muito_manga |
| `manga` | `string` | **Required**. manga name |
| `number` | `string` | **Required**. chapter number |
| `page` | `string` | **Required**. page number |

```http
  POST /manga
```

| Form   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `source` | `string` | **Required**. manga_livre or muito_manga |
| `manga` | `string` | **Required**. manga name |
| `number` | `string` | **Required**. chapter number |
| `page` | `string` | **Required**. number of pages |
| `image` | `file` | **Required**. image file |

---
Developed by [Jean Jacques Barros](https://github.com/jeanjacques10)
