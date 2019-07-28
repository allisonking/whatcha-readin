import os
from typing import List

import configparser
import requests
import xmltodict

from whatcha_readin.utils import WhatchaReadinPaths

SHELF = "currently-reading"
VERSION = 2
API_URL = "https://www.goodreads.com/review/list"


def get_currently_reading() -> List[str]:
    try:
        response = _make_goodreads_request()
        wrapped = xmltodict.parse(response.text)

        reviews = wrapped["GoodreadsResponse"]["reviews"]["review"]
        books = [r["book"] for r in reviews]
        book_titles = [b["title"] for b in books]
    except (requests.exceptions.RequestException, KeyError) as e:
        print(e)
        book_titles = []

    return book_titles


def _make_goodreads_request():
    config = configparser.ConfigParser()
    config.read(WhatchaReadinPaths.get_config_path())

    api_key = config["GOODREADS"]["api_key"]
    user_id = config["GOODREADS"]["user_id"]

    params = {"v": VERSION, "shelf": SHELF, "id": user_id, "key": api_key}

    response = requests.get(API_URL, params)
    return response
