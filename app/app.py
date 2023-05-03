import os
import sys
import logging
from flask import Flask
from flask_cors import CORS
from adapter.queue.consumer import Consumer

from adapter.web.routes.page import page_bp
from adapter.web.routes.chapter import chapter_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    logging.basicConfig(level=logging.DEBUG)

    app.register_blueprint(page_bp)
    app.register_blueprint(chapter_bp)

    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)


def create_consumer():
    consumer = Consumer()
    consumer.start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <app|consumer>")
        sys.exit(1)

    if sys.argv[1] == "app":
        create_app()
    elif sys.argv[1] == "consumer":
        create_consumer()
    else:
        print("Invalid argument:", sys.argv[1])
        sys.exit(1)
