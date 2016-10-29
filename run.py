import requests


def get_prices():
    url = 'https://api.blockchain.info/charts/market-price?' + \
          'format=json&timespan=all'
    r = requests.get(url)
    if r.status_code != 200:
        print 'Connection error'
        return False
    prices = [datapoint['y'] for datapoint in r.json()['values']]
    dates = [datapoint['y'] for datapoint in r.json()['values']]
    return prices, dates


def get_tx_volumes():
    url = 'https://api.blockchain.info/charts/n-transactions-' + \
          'excluding-popular?format=json&timespan=all'
    r = requests.get(url)
    if r.status_code != 200:
        print 'Connection error'
        return False
    tx_volumes = [datapoint['y'] for datapoint in r.json()['values']]
    return tx_volumes


def graph_chart(prices, tx_volumes):
    return
