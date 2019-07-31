import requests
import os

import responses
from whatcha_readin.goodreads import get_currently_reading, API_URL

ROOT_DIR = os.path.abspath(os.curdir)


@responses.activate
def test_get_currently_reading_fail():
    responses.add(
        responses.GET, API_URL, body=requests.exceptions.RequestException(), status=500
    )
    books = get_currently_reading()
    assert books == []


@responses.activate
def test_get_currently_reading():
    goodreads_response = open(
        "{}/tests/static_files/goodreads_response.xml".format(ROOT_DIR), "r"
    ).read()
    responses.add(responses.GET, API_URL, body=goodreads_response, status=200)
    books = get_currently_reading()
    assert books == [
        (
            "When America First Met China: An Exotic History of Tea, Drugs",
            "and Money in the Age of Sail",
        ),
        (
            "The Trainable Cat: A Practical Guide to Making Life Happier for",
            "You and Your Cat",
        ),
        "Fevre Dream",
    ]
