"""
QUTTIC Crash Course Python 

This file will contain the classes and functions
used to calculate the indicators.

Andrew Collison 07-02-18
"""
# Import the modules we need
import pandas as pd
import numpy as np

# Load the data into a pandas data frame
data = pd.read_csv("pair_data2.csv", parse_dates = True)
print()
## Create the class to hold the functions
class indicators:
	# Define the functions for the desired indicators	
	# Moving Average
	def moving_average(data, window):
		# Make the moving average calculation
		MA = data['Close'].rolling(center=False, window = window).mean()
		# Name the indicator
		name = 'MA_'+str(window)
		# Append it to the origional dataset
		data[name] = MA
		# Return the data frame
		return data
	
	# Keltner Channel
	def keltner(data):
		### Calculate ATR
		H_minus_L = data.High - data.Low
		H_minus_Cp = data.High - data.Close
		L_minus_Cp = data.Low - data.Close
		# Create a data frame of daily volatility
		ATR_calc = pd.DataFrame({'H-L': H_minus_L, 'H-CP': H_minus_Cp, 'L-CP': L_minus_Cp})
		#Calculate the moving average of the ATR
		ATR = ATR_calc.max(axis=1)
		ATR = ATR.rolling(center=False, window=10).mean()
		# Append ATR to the data frame
		data['ATR'] = ATR

		### Calculate the EXP MA	
		data['ExpMA'] = data['Close'].ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()

		### Calculate the Keltner Channel
		data['kelt_upper'] = data['ExpMA']+(1.5*data['ATR'])
		data['kelt_lower'] = data['ExpMA']-(1.5*data['ATR'])

		return data
	
	# MACD
	def MACD(data):
		ewm26 = data.Close.ewm(span=26, adjust=True, min_periods=20).mean()
		ewm12 = data.Close.ewm(span=20, adjust=True, min_periods=20).mean()
		ewm9 = data.Close.ewm(span=9, adjust=True, min_periods=20).mean()

		MACD = ewm12 - ewm26
		MACD_signal = ewm = MACD.ewm(span=20, adjust=True, min_periods=20).mean()
		MACD_hist = MACD - MACD_signal


		data['MACD'] = MACD 
		data['MACD_signal'] = MACD_signal
		data['MACD_hist'] = MACD_hist

		return data

	# RSI
	def rsi(data):
		window_length =14
		close = data['Close']
		# Get the difference in price from previous step
		delta = close.diff()
		# Get rid of the first row, which is NaN since it did not have a previous
		# row to calculate the differences
		delta = delta[1:]
		# Make the positive gains (up) and negative gains (down) Series
		up, down = delta.copy(), delta.copy()
		up[up < 0] = 0
		down[down > 0] = 0
		# Calculate the EWMA
		roll_up1 = up.ewm(min_periods=14,span=14,adjust=False).mean()
		roll_down1 = down.abs().ewm(min_periods=14,span=14,adjust=False).mean()
		# Calculate the RSI based on EWMA
		RS1 = roll_up1 / roll_down1
		RSI1 = 100.0 - (100.0 / (1.0 + RS1))
		data['RSI'] = RS1
		return data

	# Parabolic Sar
	def psar(data):
		iaf = 0.02
		maxaf = 0.2
		length = len(data)
		dates = list(data.index)
		high = list(data['High'])
		low = list(data['Low'])
		close = list(data['Close'])
		psar = close[0:len(close)]
		psarbull = [None] * length
		psarbear = [None] * length
		bull = True
		af = iaf
		ep = low[0]
		hp = high[0]
		lp = low[0]
		for i in range(2,length):
			if bull:
				psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
			else:
				psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
			reverse = False
			if bull:
				if low[i] < psar[i]:
					bull = False
					reverse = True
					psar[i] = hp
					lp = low[i]
					af = iaf
			else:
				if high[i] > psar[i]:
					bull = True
					reverse = True
					psar[i] = lp
					hp = high[i]
					af = iaf
			if not reverse:
				if bull:
					if high[i] > hp:
						hp = high[i]
						af = min(af + iaf, maxaf)
					if low[i - 1] < psar[i]:
						psar[i] = low[i - 1]
					if low[i - 2] < psar[i]:
						psar[i] = low[i - 2]
				else:
					if low[i] < lp:
						lp = low[i]
						af = min(af + iaf, maxaf)
					if high[i - 1] > psar[i]:
						psar[i] = high[i - 1]
					if high[i - 2] > psar[i]:
						psar[i] = high[i - 2]
			if bull:
				psarbull[i] = psar[i]
			else:
				psarbear[i] = psar[i]

		
		data['psar'] = psar
		data['psar_bull'] = psarbull
		data['psar_bear'] = psarbear

		return data

# data = indicators.moving_average(data, 20)
# data = indicators.moving_average(data, 200)
# data = indicators.keltner(data, 200)
# data = indicators.psar(data)
# data = indicators.MACD(data)
# data = indicators.rsi(data)
# print(data)

### We will save this file for later
# data.to_csv('indicator_data.csv')	
	