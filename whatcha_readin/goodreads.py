import os
from typing import List

import requests
import xmltodict

API_KEY = os.environ['GOODREADS_API_KEY']
USER_ID = "20891766"
SHELF = "currently-reading"
VERSION = 2

API_URL = "https://www.goodreads.com/review/list"

params = {"v": VERSION, "shelf": SHELF, "id": USER_ID, "key": API_KEY}


def get_currently_reading() -> List[str]:
    response = requests.get(API_URL, params)
    wrapped = xmltodict.parse(response.text)

    try:
        reviews = wrapped["GoodreadsResponse"]["reviews"]["review"]
        books = [r["book"] for r in reviews]
        book_titles = [b["title"] for b in books]
    except KeyError:
        book_titles = []

    return book_titles
