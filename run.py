import requests


def get_prices():
    url = 'https://api.blockchain.info/charts/market-price?' + \
          'format=json&timespan=all'
    r = requests.get.requests(url)
    prices = r.json()
    return prices


def get_tx_volume():
    url = 'https://api.blockchain.info/charts/n-transactions-' + \
          'excluding-popular?format=json&timespan=all'
    r = requests.get.requests(url)
    tx_volume = r.json()
    return tx_volume
