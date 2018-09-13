"""
This will demonstrate a simple back testing
algo that can be used for evaluation of possible
trading stratergies.

Andrew Collison: 13/09/18

"""

### Import the packages we need
import pandas as pd
import numpy as np
from indicators import indicators
import matplotlib.pyplot as plt
plt.style.use('ggplot')

### Import our pair data 
data = pd.read_csv("pair_data2.csv")

### Set the index to the time vector
data = data.set_index(data['time'])

### Calculate the indicators
# 50 and 200 day moving average
data = indicators.moving_average(data, 50) 
data = indicators.moving_average(data, 200)
# Drop any NAN values
data = data.dropna(axis=0, how='any')
print(data)


### Starting portfolio param
data["Regime"] = 0
data["Profit"] = 0
### Define our stratergy
class stratergy(object):
	"""return 1 for long position
	   return -1 for short position
	"""
	def Regime(data):
		for index, row in data.iterrows():
			if row["MA_50"] > row["MA_200"]:
				row["Regime"] = 1
				data.loc[index, "Regime"] = 1
				# print("Buy", index, row["Close"], row["Regime"])
			elif row["MA_50"] < row["MA_200"]:
				# row["Regime"] = -1
				data.loc[index, "Regime"] = -1
				# print("Sell", index, row["Close"], row["Regime"])
		print("These are the stratergy results: \n", data["Regime"].value_counts())				
		return data


### Calculate Profits for trades
class test_strat(object):
	"""docstring for test_strat
	Take the data generated above in the regime
	and place by and sell positions.
	"""
	def long_trades(data):
		# Convert into lists
		date = list(data["time"])
		close = list(data["Close"])
		regime = list(data["Regime"])
		profit = list(data["Profit"])
		# Strating param
		open_idx = 0
		close_idx = 0
		p_open = []
		p_close = []

		# If final data point is open trade
		# force close
		if regime[-1] == 1:
			regime[-1] = -1

		# Strart evaluating positions
		for i in range(len(date)):
			if regime[i] == 1 and regime[i-1] == -1:
				open_idx = i

			if regime[i] == -1 and regime[i-1] == 1:
				profit[i] = close[i]-close[open_idx]

		cp = np.cumsum(profit)
		print("Long Profit:", cp[-1])


	def short_trades(data):
		date = list(data["time"])
		close = list(data["Close"])
		regime = list(data["Regime"])
		profit = list(data["Profit"])
		open_idx = 0
		close_idx = 0
		p_open = []
		p_close = []
	
		# If final data point results in open trade
		# force the trade to close at the closing price
		if regime[-1] == -1:
			regime[-1] = -1
			# print(regime)

		for i in range(len(date)):
			if regime[i] == -1 and regime[i-1] == 1:
				open_idx = i
				# print("Short: Price Open:", close[i]  , "Date:", date[i]  )

			if regime[i] == 1 and regime[i-1] == -1:
				profit[i] = close[open_idx] - close[i]
				# print("Short: Price Close:",close[i], "Profit:", profit[i], "Date:", date[i]  )

		cp = np.cumsum(profit)
		# print(cum_p[-1])
		print("Short Profit:", cp[-1])
		

### Function to show data
def vis_results(data):
	fig, axes = plt.subplots(nrows = 2, ncols = 1, sharex = True)
	data[['Close', 'MA_200', 'MA_50']].plot(ax = axes[0])
	data["Regime"].plot(ax = axes[1])
	plt.show()


# stratergy.Regime(data)
data = stratergy.Regime(data)
# print(data)
test_strat.long_trades(data)
test_strat.short_trades(data)

vis_results(data)







