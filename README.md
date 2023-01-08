# Microstructure
## A capital market microstructure data simulation/generation framework

*Work in progress...*

###### Why data simulation?

One might wonder why it would be useful to generate simulated financial data instead of using the real thing: historical data. There are two main reasons for this.

First, high-quality financial data is extremely expensive. This is especially true of level 2 data, but even high-frequency level 1 data is often unaffordable. The only free, public historical data that is available is daily or hourly bar data, which is too low-frequency and too simplistic to be useful to professional traders (in practice there are also very few, if any, inefficiencies at this level).

Second, when using algorithmic or machine learning approaches, it is only too easy to overfit historical data or incur a "model selection bias" on this data. In fact, historical data and backtesting should not be used as a research tool, methodologically speaking (see Marcos Lopez de Prado's book "Advances in Financial Machine Learning", for example). Doing so is the easiest way to ensure that you develop a strategy that only works on paper, or a strategy that only works for a particular market regime. Instead, historical data and backtesting tools should be used merely as "sanity checks" to confirm that the resulting strategy makes sense, before going live with it.

A "best practice" methodology for developing trading strategies might go something like this:
* First generate a hypothesis based on domain expertise. This includes a mechanism of "why" such a strategy would be profitable.
* Generate simulated data that reproduces the necessary underlying mechanism, while randomizing everything else (within reasonable market parameters) 
* Develop your strategy and iterate on this simulated data only, until the desired behaviour and level of success is reached.
* Backtest on historical data to confirm that the strategy is sensible. If it is, proceed (cautiously).
* If it isn't, either your hypothesis is wrong (i.e. the market doesn't behave the way you think it does) or the simulated mechanism doesn't correspond to your hypothesis.
* The worst thing you can do at this stage is to tweak a few parameters and try again on the historical data, forcefully trying to make it work. (unless the tweak is a literal bug fix -- but then why did it work well on the simulated data?)
* Note: unless you're an experienced trader, the vast majority of your hypotheses will be wrong. But it's better to know you're wrong than to think you're right (when you're not) and bet money on it...

Simulated data is also a great way to develop new algorithms (i.e. not a specific strategy per se, but an underlying machine learning approach, for example) and test whether they're able to successfully learn/optimize on this simulation data. If they're not, then it's unlikely that they will generalize to real market data.

###### For custom data generation:

**DataGeneration.Asset** generates historical quote and trade data for an individual asset. It is currently being
modelled as a lognormal random walk. To instantiate it, pass a parameter dictionary with the following values:
* 'trend': the mean trend of this asset.
* 'volatility': the standard deviation of the random walk's innovation.
* 'base_price': the starting price level for this asset.
* 'mean_bid_ask': the average bid-ask spread of the asset.
* 'stdev_bid_ask': the standard deviation of the changes in the bid-ask spread.
* 'trade_freq': the frequency at which it trades, between 0 and 1. If 0, it never trades. If 1, it trades at every single timestep.
* 'trade_skew': the ratio of buy trades vs sell trades. At 0.5, there is an equal distribution of buys and sells on the asset. At 1, trades only occur on the ask side (active buys). At 0, trades only occur on the bid side (active sells).

**DataGeneration.Cointegration** is used to build relationships between assets of the provided list. In particular, this relationship is one of cointegration (not correlation). This means that the price levels of these assets will tend to revert to a fixed mean distance between each other. This is currently modelled as an Ornstein-Uhlenbeck process.

To instantiate a Cointegration object, pass a list of Asset objects and a parameter dictionary that contains the following values:
* 'theta': the strength of mean reversion. A value of 0 means no cointegration. A strength of 1 means the assets will follow each other to perfection.
* 'volatility': the strength of the innovations that temporarily drive the prices apart. This is the strength of the "pushing" force, while theta represents the strength of the "pulling" force.

Once an Asset or a Cointegration object *(obj)* has been instantiated, you can use it to generate a number of data points as follows:
```
data_points = obj.generate(N)
```

For the case of DataGeneration.Cointegration, this will generate N data points of the following format:
```
data_points = (bid_data, ask_data, trade_data)

  bid_data shape: (D, N) where D is the number of assets, and N is the number of timesteps (bid values) per asset.

  ask_data shape: (D, N) where D is the number of assets, and N is the number of timesteps (ask values) per asset.

  trade_data shape: (D, N) where D is the number of assets, and N is the number of timesteps (trade prices) per asset.
  Each time step where a trade did not occur will instead contain a *None* value.
```

For the case of DataGeneration.Asset, the returned data does not contain a D dimension. They are only flat vectors of prices.

###### Examples:
See the file *RVtrading.py* for a few examples on generating assets and cointegration data.

Run the *main.py* file to generate data and visualize it. 

###### TODO/Desired features:

* More realistic/complex Cointegration mechanism that can simulate temporary shocks
* trade_skew and trade_freq shouldn't be static parameters? They are stochastic processes?
* Support for regime changes and temporary trends when simulating individual assets
* Trade simulation should support dark exchanges: fills that occur in-between the bid and the ask
* Return available bid/ask sizes on the book (not just prices, as is the case right now)
* Support non 1:1 cointegration levels
* Support for exogenous variables that influence the cointegration relationship and the individual assets
* Simulate Level 2 book
* Simulate different exchanges with different functionalities (ideally based on the real Canadian and U.S. exchanges)
* Model Wiggins-like mean-reverting volatility
* More generally anything that is a stochastic process (volatility, trade_skew, etc.) should be configurable by instantiating a process from a library of general stochastic processes. Allows for better customization of the dataset.
* A module that makes it easy to do curriculum learning by building increasingly complex data series
* More realistic asset models than just log-normal (support Cauchy distributions, for example?)
* **DataGeneration.Derivative** object (to simulate things such as options)
* A live market simulation mode (rather than only generating historical data) with automated participants
* Optimize & parallelize code for faster data generation

###### About the author:

Simon Ouellette is a machine learning specialist with 7 years of professional experience in applying his AI expertise
to capital markets & trading problems. He has had the opportunity of working with some of the best professional
traders, which allowed him to develop an in-depth understanding of markets and trading. As a result, this
simulation framework is built from the perspective of an expert mindset on the topic, and reflects features and functionalities that
are necessary for professional-level trading.
