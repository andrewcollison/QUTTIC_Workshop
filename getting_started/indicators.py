"""
QUTIC Crash Course Python 

This file will contain the classes and functions
used to calculate the indicators.

Andrew Collison 14-09-18
"""
# Import the modules we need
import pandas as pd
import numpy as np

# Load the data into a pandas data frame
data = pd.read_csv("pair_data2.csv", parse_dates = True)
print(data)

## Create the class to hold the functions
class indicators():
	# Define the functions for the desired indicators	
	# Moving Average
	def moving_average(data, window):
		MA = data['Close'].rolling(center = False, window = window).mean()
		name = 'MA_' + str(window)
		data[name] = MA
		return data
	
	# Keltner Channel
	def keltner(data):
		# Calculate ATR
		H_minus_L = data.High - data.Low
		H_minus_Cp = data.High - data.Close
		L_minus_Cp = data.Low - data.Close

		ATR_calc = pd.DataFrame({'H-L': H_minus_L, "H-CP": H_minus_Cp, 'L-CP': L_minus_Cp})
		ATR = ATR_calc.max(axis=1)
		ATR = ATR.rolling(center=False, window = 10).mean()

		data['ATR'] = ATR
		
		# EXP moving average
		data['ExpMA'] = data['Close'].ewm(span = 20, min_periods = 0, adjust = False, ignore_na = False).mean()

		# Calculate kelt bands
		data['kelt_upper'] = data['ExpMA'] + (1.5*(data['ATR']))
		data['kelt_lower'] = data['ExpMA'] - (1.5*(data['ATR']))

		return data

	def MACD(data):
		ewm26 = data['Close'].ewm(span = 26, min_periods = 0, adjust = True, ignore_na = False).mean()
		ewm12 = data['Close'].ewm(span = 12, min_periods = 0, adjust = True, ignore_na = False).mean()
		ewm9 = data['Close'].ewm(span = 9, min_periods = 0, adjust = True, ignore_na = False).mean()

		data['MACD'] = ewm12 - ewm26
		data['MACD_signal'] = data['MACD'].ewm(span = 20, adjust = True, min_periods = 20).mean()
		data['MACD_hist'] = data['MACD'] - data['MACD_signal']

		return data 

	def RSI(data):
		window_length = 14
		close = data['Close']
		delta = close.diff()
		delta = delta[1:]

		up, down = delta.copy(), delta.copy()
		up[up<0] = 0
		down[down > 0] = 0

		roll_up1 = up.ewm(span = 14, min_periods = 14, adjust = False).mean()
		roll_down1 = down.abs().ewm(span = 14, min_periods = 14, adjust = False).mean()

		RS1 = roll_up1 / roll_down1

		RSI = 100 - (100/(1 + RS1))

		data['RSI'] = RSI

		return data 
	
	
# data = indicators.moving_average(data, 20)
# data = indicators.moving_average(data, 200)
# data = indicators.keltner(data)
# data = indicators.MACD(data)
data = indicators.RSI(data)
print(data)

### We will save this file for later
# data.to_csv('indicator_data.csv')	

# data = indicators.moving_average(data, 20)
# data = indicators.moving_average(data, 200)
# print(data)

