import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np


def movingaverage(interval, window_size):
	window = np.ones(int(window_size))/float(window_size)
	return np.convolve(interval, window, "same")

raw_data = DataFrame.from_csv("../data/historic_wins.tsv", sep="\t",index_col=False, header=0)
y = raw_data["Distance Cycled"]
x = raw_data["Year"]
print y
plt.plot(x,y,ls='none',marker='.',color="green")
av_x = pandas.rolling_mean(y,10, min_periods=8, center=True)
print av_x
plt.plot(x,av_x,color="blue")
z = np.polyfit(x,y,1)
p = np.poly1d(z)
plt.plot(x,p(x),"r--")
plt.show()

# The first mountain stages (in the Pyrenees) appeared in 1910
# Until 1930 he demanded that riders mend their bicycles without help and that they use the same bicycle from start to end
# 1953 saw the introduction of the Green Jersey 'Points' competition. 
# in 1975, the same year the polka-dot jersey
# The mountains classification was added to the Tour de France in the 1933 edition
# yellow jersey was added to the race in the 1919 edition 