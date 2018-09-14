"""
QUTTIC Crash Course Python 

This file will be the main document
	- Here we will call our indicator functions
	- Load data and build our data frame
	- Graph the data

Andrew Collison 14-09-18
"""

# Import the modules we need
from indicators import indicators # we just wrote this module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## Load the data into a dataframe object named "df" using pd.read_csv()
df = pd.read_csv('pair_data2.csv')
print(df)

## Call our indicator functions
# Calculate 50 day moving average
df = indicators.moving_average(df, 50)
df = indicators.moving_average(df, 200)

print(df)

## Display the data
df.plot(x = 0, y =['Close', 'MA_50', 'MA_200'])
plt.title('Currency Pair')
plt.xlabel('Time (Days)')
plt.ylabel('Price (Cents)')
plt.show()



