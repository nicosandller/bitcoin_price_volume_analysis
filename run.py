import sys

import matplotlib.pyplot as plt

from tx_and_prices import get_prices, get_tx_volumes

SMOOTH_FACTOR = 150000
TIMESPAN = sys.argv[1]


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
tx_volumes, transformed, tx_vol_dates = get_tx_volumes(SMOOTH_FACTOR, TIMESPAN)
# graph_chart(prices, tx_volumes, dates)
if prices is not False:
    if TIMESPAN == 'all':
        print 'transformed series'
        graph_chart(prices, transformed, dates)
    else:
        graph_chart(prices, tx_volumes, dates)
