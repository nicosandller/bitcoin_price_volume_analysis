import requests
from datetime import datetime
from scipy import interpolate


def get_prices(timespan='all'):
    url = 'https://api.blockchain.info/charts/market-price?' + \
          'format=json&timespan=' + timespan
    r = requests.get(url)
    if r.status_code != 200:
        print 'Connection error'
        return False
    if 'error' in r.json():
        print r.json()['error']
    prices = [datapoint['y'] for datapoint in r.json()['values']]
    dates = [datetime.fromtimestamp(datapoint['x']) for datapoint in r.json()['values']]
    return prices, dates


def get_tx_volumes(smooth_factor, timespan='all'):
    url = 'https://api.blockchain.info/charts/n-transactions-' + \
          'excluding-popular?format=json&timespan=' + timespan
    r = requests.get(url)
    if r.status_code != 200:
        print 'Connection error'
        return False
    if 'error' in r.json():
        print r.json()['error']
    tx_volumes = [datapoint['y'] / 1000 for datapoint in r.json()['values']]
    x = [datapoint['x'] for datapoint in r.json()['values']]
    tck = interpolate.splrep(x, tx_volumes, k=3, s=smooth_factor)
    transformed = interpolate.splev(x, tck, der=0)
    dates = [datetime.fromtimestamp(datapoint['x']) for datapoint in r.json()['values']]
    return tx_volumes, transformed, dates
