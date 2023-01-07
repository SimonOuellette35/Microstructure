from RVtrading import generateA_task
import matplotlib.pyplot as plt
import numpy as np

bids, asks, trades = generateA_task(250)

# visualize individual assets, trades and pair spreads
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

ax1.set_title('Symbol 1')
ax1.plot(bids[0], color='green')
ax1.plot(asks[0], color='red')
ax1.plot(trades[0], 'bo')

ax2.set_title('Symbol 2')
ax2.plot(bids[1], color='green')
ax2.plot(asks[1], color='red')
ax2.plot(trades[1], 'bo')

# visualize the spread
bid_spreads = np.array(bids[0]) - np.array(bids[1])
ask_spreads = np.array(asks[0]) - np.array(asks[1])

ax3.set_title('Spread')
ax3.plot(bid_spreads, color='green')
ax3.plot(ask_spreads, color='red')

plt.show()
