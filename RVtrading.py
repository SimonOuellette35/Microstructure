import numpy as np
from DataGeneration.Asset import Asset
from DataGeneration.Cointegration import Cointegration

# This generates data for simulation of a relative value/market making strategy (i.e. Cointegration-based strategy).

# A - start with 2 assets, cointegrated without shocks or regime changes
def generateA_task(N):

    return generateB_task(N, num_assets=2)

# B - 3 or 4 assets (conditions like A) that are cointegrated together.
def generateB_task(N, num_assets=2):

    assets = []

    for _ in range(num_assets):
        # Strength of random innovations of individual asset's random walk
        noise_vol = np.random.uniform(0.001, 0.05)

        # Base price level of assets
        base_price = np.random.uniform(5., 100.)

        # Mean bid-ask spread per asset
        mean_bid_ask = np.random.uniform(0.01, 0.5)

        # Std. dev of bid-ask spread per asset (as a percentage of the bid-ask spread value)
        stdev_bid_ask = np.random.uniform(0.01, 0.2)

        # Trade frequency
        trade_freq = np.random.uniform(.2, 10.)

        # Trade skew (ratio of buys to sells)
        trade_skew = np.random.uniform(0., 1.)

        params = {
            'volatility': noise_vol,
            'base_price': base_price,
            'mean_bid_ask': mean_bid_ask,
            'stdev_bid_ask': stdev_bid_ask,
            'trade_freq': trade_freq,
            'trade_skew': trade_skew,
            'trend': 0.
        }
        assets.append(Asset(params))

    # Strength of mean reversion of assets
    theta = np.random.uniform(0.05, 0.25)

    # Strength of random innovation of the cointegration relationship
    noise_vol = np.random.uniform(0.001, 0.05)

    coint_params = {
        'theta': theta,
        'volatility': noise_vol
    }

    coint = Cointegration(assets, coint_params)

    return coint.generate(N)