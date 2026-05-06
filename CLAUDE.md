# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Manga Scrapper API** — A Python/Flask API + async consumer system that scrapes manga pages from supported websites and stores them on disk (AWS EBS). Uses AWS SQS (or LocalStack for local dev) as the message queue between the API and the consumer workers.

## Architecture

```
┌─────────────┐    SQS Queue     ┌──────────────────┐
│  Flask API  │ ─────────────►  │  Consumer Worker  │
│  (app.py)   │                  │  (consumer.py)    │
└─────────────┘                  └──────────────────┘
       │                                  │
       ▼                                  ▼
  Save/Serve                        Scrape pages
  images from                       from websites
  local volume                      → save to volume
```

- **API** (`app/app.py`): Flask app that receives requests, saves/serves manga images, and enqueues scraping tasks via SQS.
- **Consumer** (`app/consumer.py`): Polls SQS queue and triggers scraping via `consumer_processor.py`.
- **Services** (`app/src/services/`): Site-specific scrapers (`mangalivre_service.py`, `muitomanga_service.py`) and a `save_page_service.py`.
- **Gateway** (`app/src/gateway/`): Producer (sends to SQS) and Consumer (processes messages) processors.

## Supported Sites

- [Manga Livre](https://mangalivre.net/) — source: `manga_livre`
- [Muito Manga](https://muitomanga.com/) — source: `muito_manga`

## Running Locally

```bash
# Run API + consumer (10 workers) with LocalStack SQS
docker-compose up --build --scale manga_consumer=10 -d
```

Docker Compose spins up:
- `sqs` — LocalStack container emulating AWS SQS on port 4576
- `manga_app` — Flask API on port 3000
- `manga_consumer` — Consumer worker(s) pulling from SQS

## API Endpoints

| Method | Path       | Description                    |
|--------|------------|-------------------------------|
| POST   | `/page`    | Save an image to disk          |
| GET    | `/page`    | Get a single manga page image  |
| GET    | `/chapter` | Get all pages of a chapter     |

Common query params: `source`, `manga`, `number`, `page`

## SQS Message Format

```json
{
  "source": "manga_livre",
  "manga": "Naruto",
  "chapter": "692"
}
```

## Environment Variables

| Variable           | Description                          |
|--------------------|--------------------------------------|
| `SQS_ENDPOINT`     | SQS endpoint URL (LocalStack or AWS) |
| `API_HOST`         | Base URL of the Flask API            |
| `AWS_ACCESS_KEY_ID`| AWS credentials                      |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials                 |
| `AWS_DEFAULT_REGION`    | AWS region (default: us-east-1) |
| `PORT`             | Flask port (default: 3000)           |

## Stack

- Python 3 + Flask + Flask-CORS
- boto3 (AWS SDK) for SQS
- BeautifulSoup4 for HTML scraping
- Docker + Docker Compose
- LocalStack for local SQS emulation
- GitHub Actions for CI/CD deploy to EC2

## Notes

- `docker-compose.yaml` should never contain real AWS credentials — use environment variables or `.env` files instead.
- The `manga_data` Docker volume persists scraped images across container restarts.
