import numpy as np
from DataGeneration.Asset import Asset
from DataGeneration.Cointegration import Cointegration
from stochastic.processes.diffusion.diffusion import DiffusionProcess

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

        # Trade frequency process
        trade_freq_speed = np.random.uniform(0.01, .5)
        trade_freq_mean = np.random.uniform(0.05, 75.)
        trade_freq_vol = np.random.uniform(1., 10.)
        trade_freq_process = DiffusionProcess(speed=trade_freq_speed/float(N), vol=trade_freq_vol/float(N), mean=trade_freq_mean, t=N)

        # Trade skew process
        trade_skew_speed = np.random.uniform(0.01, .5)
        trade_skew_mean = np.random.uniform(0.01, 1.)
        trade_skew_vol = np.random.uniform(1., 10.)
        trade_skew_process = DiffusionProcess(speed=trade_skew_speed/float(N), vol=trade_skew_vol/float(N), mean=trade_skew_mean, t=N)

        params = {
            'volatility': noise_vol,
            'base_price': base_price,
            'mean_bid_ask': mean_bid_ask,
            'stdev_bid_ask': stdev_bid_ask,
            'trade_freq': trade_freq_process,
            'trade_skew': trade_skew_process,
            'trend': 0.
        }
        assets.append(Asset(params))

    # Strength of mean reversion of assets
    theta = np.random.uniform(0.1, 0.45)

    # Strength of random innovation of the cointegration relationship
    noise_vol = np.random.uniform(0.001, 0.025)

    # Premium around which each asset cointegrates w.r.t. the first asset
    premia = [0.]
    shock_freq = [0.]
    shock_duration = [0.]
    shock_mean = [0.]
    shock_stdev = [0.]
    for _ in range(1, num_assets):
        premia.append(np.random.normal(0., 2.5))

        # Generate occasional temporary shocks in the cointegration relationship
        # shock_freq: how frequent are the shocks, a value between 0 and 1. At 0, shocks are disabled. At 1, shocks happen
        # at every timestep (not recommended).
        shock_freq.append(np.random.uniform(0, 0.1))
        print("shock_freq = ", shock_freq[-1])

        # shock_duration: strength of persistence of shocks, a value between 0 and 1. At 0, shocks immediately revert to
        # the original premium value (i.e. they disappear). At 1, the shocks are permanent. This value is similar in
        # functionality to the theta in the cointegration relationship.
        shock_duration.append(np.random.uniform())
        print("shock_duration = ", shock_duration[-1])

        # shock_mean: the average jump in premium when a shock occurs.
        shock_mean.append(np.random.normal(0, 1.))
        print("shock_mean = ", shock_mean[-1])

        # shock_stdev: the standard deviation to use when selecting the random jump value for a shock.
        shock_stdev.append(np.random.uniform(0.01, 0.5))
        print("shock_stdev = ", shock_stdev[-1])

    coint_params = {
        'theta': theta,
        'volatility': noise_vol,
        'premia': premia,
        'shock_freq': shock_freq,
        'shock_duration': shock_duration,
        'shock_mean': shock_mean,
        'shock_stdev': shock_stdev,
    }

    coint = Cointegration(assets, coint_params)

    return coint.generate(N)