import numpy as np
import matplotlib.pyplot as plt

# This generates data for simulation of a relative value/market making strategy.

# TODO: Curriculum learning:
# A - start with 2 assets, cointegrated without shocks or regime changes
# B - 3 or 4 assets (conditions like A)
# C - B, but add temporary shocks
# D - C, but add regular permanent regime changes
# E - D, but instead of only random walks for individual assets, add 4 distinct regimes: Random Walk, Mean reverting, Long, Short
# F - E, but add exogenous variables that allow some form of prediction of the cointegration relationship
# G - F, but make base price levels uneven, such that hedging ratios other than 1:1 have to be used.
# H - G, but simulate L2 book with bid-ask sizes
# I = H, but simulate dark positions: fills sometimes occur at prices between the bid and ask (such as midpoint, for example)
# J = I, but simulate each of the different exchanges and their particular behaviours.

def roundPrice(raw_price):
    price100 = int(raw_price * 100.0)
    return float(price100) / 100.0

def generateA_task(N):

    timeseries = []

    # TODO: Wiggins-like mean-reverting volatility

    # first randomize the parameters of the relationship

    # Strength of random innovations of individual asset's random walk
    RW_noise_vol = np.random.uniform(0.001, 0.05)

    # Base price level of assets
    base_price = np.random.uniform(5., 100.)

    # Strength of mean reversion of assets
    theta = np.random.uniform(0.05, 0.25)

    # Strength of random innovation of the cointegration relationship
    coint_noise_vol = np.random.uniform(0.001, 0.05)

    # Mean bid-ask spread per asset
    mean_bid_ask = np.random.uniform(0.01, 0.5)

    # Std. dev of bid-ask spread per asset (as a percentage of the bid-ask spread value)
    stdev_bid_ask = np.random.uniform(0.01, 0.2)

    # Trade frequency
    trade_freq = np.random.uniform(.2, 10.)

    # Trade skew (ratio of buys to sells)
    trade_skew = np.random.uniform(0., 1.)

    print("RW_noise_vol = %.2f" % RW_noise_vol)
    print("base_price = %.2f" % base_price)
    print("theta = %.2f" % theta)
    print("coint_noise_vol = %.2f" % coint_noise_vol)
    print("mean_bid_ask = %.2f" % mean_bid_ask)
    print("stdev_bid_ask = %.2f" % stdev_bid_ask)
    print("trade_freq = %.2f" % trade_freq)
    print("trade_skew = %.2f" % trade_skew)

    # Now generate the actual time series (ignoring the bid-ask details first, focussing only on the price relationships
    # between assets)
    baseline_ts = []
    midpoint = base_price + np.random.normal(0., RW_noise_vol)

    baseline_ts.append(midpoint)
    for t in range(N-1):
        tmp_midpoint = baseline_ts[-1] * np.exp(np.random.normal(0., RW_noise_vol))
        baseline_ts.append(tmp_midpoint)

    other_ts = []
    midpoint = base_price + np.random.normal(0., RW_noise_vol)

    other_ts.append(midpoint)
    for t in range(N-1):
        tmp_midpoint = other_ts[-1] + theta * (baseline_ts[t] - other_ts[-1]) + np.random.normal(0., coint_noise_vol)
        other_ts.append(tmp_midpoint)

    timeseries.append(baseline_ts)
    timeseries.append(other_ts)

    # Then, generate the micro-market details of bid-ask effects for each asset.
    bid_timeseries = []
    ask_timeseries = []
    for ts in timeseries:
        bids = []
        asks = []

        initial_bid_ask = roundPrice(np.random.normal(mean_bid_ask, stdev_bid_ask*mean_bid_ask))
        if initial_bid_ask < 0:
            initial_bid_ask = 0.01

        print("Initial bid-ask spread = ", initial_bid_ask)

        bid_ask_spread = initial_bid_ask

        for t in range(N):
            last_bid = roundPrice(ts[t] - bid_ask_spread)
            last_ask = roundPrice(ts[t] + bid_ask_spread)

            bids.append(last_bid)
            asks.append(last_ask)

            bid_ask_spread = roundPrice(np.random.normal(mean_bid_ask, stdev_bid_ask*mean_bid_ask))

        bid_timeseries.append(bids)
        ask_timeseries.append(asks)

    # Finally, generate the tape data (trade history) to be able to simulate fills.
    trade_timeseries = []
    for ts_idx in range(len(timeseries)):
        trades = []

        for t in range(N):
            # trade probability is inversely proportional to bid-ask spread!
            current_bid_ask_spread = ask_timeseries[ts_idx][t] - bid_timeseries[ts_idx][t]
            current_trade_freq = (1.0 / (100. * current_bid_ask_spread)) * trade_freq

            tmp = np.random.uniform(0., 1.)
            if tmp < current_trade_freq:
                # a trade occurred, let's determine which side of the book was filled.
                tmp = np.random.uniform(0., 1.)
                if tmp < trade_skew:
                    # the ask was filled
                    trades.append(ask_timeseries[ts_idx][t])
                else:
                    # the bid was filled
                    trades.append(bid_timeseries[ts_idx][t])
            else:
                # no trade
                trades.append(None)

        trade_timeseries.append(trades)

    return bid_timeseries, ask_timeseries, trade_timeseries