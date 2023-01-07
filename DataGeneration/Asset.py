import numpy as np

class Asset:

    def __init__(self, params):
        self.params = params

    def roundPrice(self, raw_price):
        price100 = int(raw_price * 100.0)
        return float(price100) / 100.0

    def generate_trades(self, bids, asks):
        trades = []
        N = len(bids)

        for t in range(N):
            # trade probability is inversely proportional to bid-ask spread!
            current_bid_ask_spread = asks[t] - bids[t]
            current_trade_freq = (1.0 / (100. * current_bid_ask_spread)) * self.params['trade_freq']

            tmp = np.random.uniform(0., 1.)
            if tmp < current_trade_freq:
                # a trade occurred, let's determine which side of the book was filled.
                tmp = np.random.uniform(0., 1.)
                if tmp < self.params['trade_skew']:
                    # the ask was filled
                    trades.append(asks[t])
                else:
                    # the bid was filled
                    trades.append(bids[t])
            else:
                # no trade
                trades.append(None)

        return np.array(trades)

    def generate_bidasks(self, midpoints):
        bids = []
        asks = []
        N = len(midpoints)

        mean_bid_ask = self.params['mean_bid_ask']
        stdev_bid_ask = self.params['stdev_bid_ask']
        initial_bid_ask = self.roundPrice(np.random.normal(mean_bid_ask, stdev_bid_ask * mean_bid_ask))
        if initial_bid_ask < 0:
            initial_bid_ask = 0.01

        bid_ask_spread = initial_bid_ask

        for t in range(N):
            last_bid = self.roundPrice(midpoints[t] - bid_ask_spread)
            last_ask = self.roundPrice(midpoints[t] + bid_ask_spread)

            bids.append(last_bid)
            asks.append(last_ask)

            bid_ask_spread = self.roundPrice(np.random.normal(mean_bid_ask, stdev_bid_ask * mean_bid_ask))

        return np.array(bids), np.array(asks)

    def generate_midpoints(self, N):
        ts = []
        midpoint = self.params['base_price'] * np.exp(np.random.normal(self.params['trend'], self.params['volatility']))
        ts.append(midpoint)

        for t in range(N - 1):
            tmp_midpoint = ts[-1] * np.exp(np.random.normal(self.params['trend'], self.params['volatility']))
            ts.append(tmp_midpoint)

        return np.array(ts)

    def generate(self, N):
        midpoints = self.generate_midpoints(N)
        bids, asks = self.generate_bidasks(midpoints)
        trades = self.generate_trades(bids, asks)

        return bids, asks, trades