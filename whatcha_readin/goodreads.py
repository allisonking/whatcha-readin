import requests
import xmltodict

KEY = 'NTvl08balpMZU1socckSw'
USER_ID = '20891766'
SHELF = 'currently-reading'
VERSION = 2

API_URL = 'https://www.goodreads.com/review/list'

params = {
  'v': VERSION,
  'shelf': SHELF,
  'id': USER_ID,
  'key': KEY
}

response = requests.get(API_URL, params)
wrapped = xmltodict.parse(response.text)

try:
  books = wrapped['GoodreadsResponse']['reviews']['review']
except KeyError:
  books = []



print(books)