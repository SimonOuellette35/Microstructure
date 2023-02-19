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

        def trim_process(process):
            output = []
            for p in process:
                if p <= 0:
                    p = 0.01

                if p >= 1:
                    p = 0.99

                output.append(p)

            return np.array(output)

        trade_freq_init = np.random.normal(0.5, .25)
        trade_skew_init = np.random.normal(0.5, .25)

        trade_freqs_unadjusted = self.params['trade_freq'].sample(N, trade_freq_init)
        trade_skews = self.params['trade_skew'].sample(N, trade_skew_init)

        trade_freqs_unadjusted = trim_process(trade_freqs_unadjusted)
        trade_skews = trim_process(trade_skews)

        for t in range(N):
            # trade probability is inversely proportional to bid-ask spread!
            current_bid_ask_spread = asks[t] - bids[t]

            spread_adjustment = 1.0 / 100. * current_bid_ask_spread
            if spread_adjustment < 0.25:
                spread_adjustment = 0.25

            current_trade_freq = spread_adjustment * trade_freqs_unadjusted[t]

            tmp = np.random.uniform(0., 1.)
            if tmp < current_trade_freq:
                # a trade occurred, let's determine which side of the book was filled.
                tmp = np.random.uniform(0., 1.)
                if tmp < trade_skews[t]:
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