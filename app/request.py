import requests


def posting():
    get_posting = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return get_posting