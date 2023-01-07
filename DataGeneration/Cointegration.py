import numpy as np

class Cointegration:

    def __init__(self, assets, params):
        self.assets = assets
        self.params = params

    def generate_midpoints(self, N):
        midpoints = []
        baseline_ts = self.assets[0].generate_midpoints(N)
        midpoints.append(baseline_ts)

        theta = self.params['theta']
        vol = self.params['volatility']
        for i in range(1, len(self.assets)):
            base_price = self.assets[i].params['base_price']
            other_ts = []
            midpoint = base_price * np.exp(np.random.normal(self.assets[i].params['trend'],
                                                            self.assets[i].params['volatility']))
            other_ts.append(midpoint)

            for t in range(N - 1):
                tmp_midpoint = other_ts[-1] + theta * (baseline_ts[t] - other_ts[-1]) * np.exp(np.random.normal(0., vol))
                other_ts.append(tmp_midpoint)

            midpoints.append(other_ts)

        return midpoints

    def generate(self, N):
        # Now generate the actual time series (ignoring the bid-ask details first, focussing only on the price
        # relationships between assets, i.e. the midpoints)
        midpoints = self.generate_midpoints(N)

        # Then, generate the micro-market details of bid-ask effects for each asset.
        bids = []
        asks = []
        for i in range(len(midpoints)):
            tmp_bids, tmp_asks = self.assets[i].generate_bidasks(midpoints[i])
            bids.append(tmp_bids)
            asks.append(tmp_asks)

        # Finally, generate the tape data (trade history) to be able to simulate fills.
        trades = []
        for i in range(len(midpoints)):
            tmp_trades = self.assets[i].generate_trades(bids[i], asks[i])
            trades.append(tmp_trades)

        return bids, asks, trades