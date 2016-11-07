import requests
import sys
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import interpolate

SMOOTH_FACTOR = 150000
TIMESPAN = sys.argv[1]


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
    dates = [datetime.fromtimestamp(datapoint['x'])
             for datapoint in r.json()['values']]
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
    return tx_volumes, transformed


def graph_chart(prices, tx_volumes, dates):
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Price', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax1.plot(dates, prices, 'b-')
    #
    ax2 = ax1.twinx()
    ax2.set_ylabel('Transaction volume (thousands)', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    ax2.plot(dates, tx_volumes, 'r-')
    #
    ax1.set_xlabel('time')
    plt.show()
    return True

prices, dates = get_prices(TIMESPAN)
tx_volumes, transformed = get_tx_volumes(SMOOTH_FACTOR, TIMESPAN)
# graph_chart(prices, tx_volumes, dates)
if prices is not False:
    if TIMESPAN == 'all':
        print 'transformed series'
        graph_chart(prices, transformed, dates)
    else:
        graph_chart(prices, tx_volumes, dates)
