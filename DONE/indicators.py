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
	
	
# data = indicators.moving_average(data, 20)
# data = indicators.moving_average(data, 200)
# data = indicators.keltner(data)
# print(data)

### We will save this file for later
# data.to_csv('indicator_data.csv')	
	