import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import numpy.polynomial.polynomial as poly
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import scipy as sy
import math
import re
from sklearn import datasets, linear_model
import hashlib


def movingaverage(interval, window_size):
	window = np.ones(int(window_size))/float(window_size)
	return np.convolve(interval, window, "same")


def formatTimeTaken(time_field):
	if pandas.isnull(time_field):
		time_field="0h 0'"
	m = re.search('(.+?)h',time_field)
	start = time_field.find('h ') + 2 
	end = time_field.find("'", start)
	minutes = float(time_field[start:end])
	minutes = minutes/60
	if m:
		day = m.group(1)
		return float(day) + minutes

def crosscorr(datax, datay, lag=0):
    """ Lag-N cross correlation. 
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """
    return datax.corr(datay.shift(lag))

def plotVariable(field_name):
	y = raw_data[field_name].fillna(np.mean(raw_data[field_name]))
	x = raw_data["Year"]

	fig = plt.figure()

	ax = fig.add_subplot(111)
	ax.yaxis.labelpad = 20
	ax.plot(x,y,ls='none',marker='o',color="#4d4dff", markeredgewidth=0.0)
	ax.set_axis_bgcolor('#ffffff')
	ax.yaxis.grid(True)
	ax.set_title(field_name + " of Winner Over Time")
	ax.set_xlabel("Year")
	ax.set_ylabel(field_name + " of Winner")
	ax.yaxis.labelpad = 20
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	#av_x = pandas.rolling_mean(y,10, min_periods=8, center=True)
	#plt.plot(x,av_x,color="blue")

	z = np.polyfit(x,y,2)
	p = np.poly1d(z)
	#ax.plot(x,p(x),"r--", linewidth=3)

	#f = interp1d(x,y, kind="cubic")
	#xnew = np.linspace(min(x), max(x),len(x))

	#plt.plot(xnew,f(xnew),"r--")
	plt.show()

def func(x, a, b, c):
		return a*x**b + c

if 0:
	raw_data = DataFrame.from_csv("../data/historic_wins.tsv", sep="\t",index_col=False, header=0)
	raw_data["Winning Time"] = [formatTimeTaken(time) for time in raw_data["Winning Time"]]
	raw_data = raw_data.dropna()
	plotVariable("Age")

# Shows the general winners and by country
if 1:
	raw_data = DataFrame.from_csv("../data/historic_wins.tsv", sep="\t",index_col=False, header=0)
	raw_data["Winning Time"] = [formatTimeTaken(time) for time in raw_data["Winning Time"]]
	raw_data = raw_data.dropna()
	#plotVariable("Number of Stages")
	raw_data["Drop Out"] = (raw_data["Classified Riders"] / raw_data["The Starters"])*100
	raw_data = raw_data.fillna(np.nan)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title("Number of Cyclists entered VS Number of Cyclists that Finish")
	ax.set_xlabel("Year")
	ax.set_ylabel("Number of Cyclists")

	Classified1 = raw_data[raw_data["Year"]<1915].loc[:,["Classified Riders"]]
	year1 = raw_data[raw_data["Year"]<1915].loc[:,["Year"]]

	Classified2 = raw_data[(raw_data["Year"]>1918) & (raw_data["Year"]<1940)].loc[:,["Classified Riders"]]
	year2 = raw_data[(raw_data["Year"]>1918) & (raw_data["Year"]<1940)].loc[:,["Year"]]

	Classified3 = raw_data[(raw_data["Year"]>1946) & (raw_data["Year"]<1999)].loc[:,["Classified Riders"]]
	year3 = raw_data[(raw_data["Year"]>1946) & (raw_data["Year"]<1999)].loc[:,["Year"]]

	Classified4 = raw_data[(raw_data["Year"]>2005)].loc[:,["Classified Riders"]]
	year4 = raw_data[raw_data["Year"]>2005].loc[:,["Year"]]

	Starters1 = raw_data[raw_data["Year"]<1915].loc[:,["The Starters"]]
	Starters2 = raw_data[(raw_data["Year"]>1918) & (raw_data["Year"]<1940)].loc[:,["The Starters"]]
	Starters3 = raw_data[(raw_data["Year"]>1946) & (raw_data["Year"]<1999)].loc[:,["The Starters"]]
	Starters4 = raw_data[(raw_data["Year"]>2005)].loc[:,["The Starters"]]

	ax.plot(year1,Classified1, color="blue")
	ax.plot(year2,Classified2, color="blue")
	ax.plot(year3,Classified3, color="blue")
	ax.plot(year4,Classified4, color="blue")
	ax.plot(year1,Starters1, color="green")
	ax.plot(year2,Starters2, color="green")
	ax.plot(year3,Starters3, color="green")
	ax.plot(year4,Starters4, color="green")
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title("Survival Rate Over Time (Percentage)")
	ax.set_ylabel("Survival Rate (%)")
	ax.set_xlabel("Year")
	axes = plt.gca()
	axes.set_xlim([1903,2020])
	ax.scatter(raw_data["Year"],raw_data["Drop Out"],marker="o")
	x = raw_data["Year"]
	y = raw_data["Drop Out"]
	coefs = poly.polyfit(x, y, deg=1)
	ffit = poly.Polynomial(coefs)
	y_hat = ffit(x)
	ax.plot(x,y_hat,"r--", linewidth=3)
	plt.show()

	ax = raw_data["Winner"].value_counts().plot(kind="bar")
	ax.set_title("Winners")
	ax.set_xlabel("Cyclist")
	ax.set_ylabel("Number of Wins")
	plt.show()

	winners = ["J. ANQUETIL","B. HINAULT","E. MERCKX","M. INDURAIN"]
	color_map = ["#ff6666","#ff9966","#0099ff","#adebad"]
	data = raw_data[raw_data["Winner"].isin(winners)]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter_plots = range(13)
	for index in range(len(winners)):
		X = data[data["Winner"] == winners[index]].loc[:,["Year"]]
		Y = data[data["Winner"] == winners[index]].loc[:,["Drop Out"]]
		scatter_plots[index] = ax.scatter(x=X, y=Y,s=50,color=color_map[index],edgecolor='None')
	plt.legend(scatter_plots,winners,scatterpoints=1,loc='lower right',ncol=2)
	ax.set_axis_bgcolor('white')
	ax.set_title("Winners comapred to the Survival Rate(%) over Time")
	ax.set_xlabel("Year")
	ax.set_ylabel("Survival Rate %")
	ax.yaxis.labelpad = 20
	ax.set_axis_bgcolor('#262626')
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	plt.show()

if 0:
	raw_data = DataFrame.from_csv("../data/historic_wins.tsv", sep="\t",index_col=False, header=0)
	raw_data["Winning Time"] = [formatTimeTaken(time) for time in raw_data["Winning Time"]]

	ax = raw_data["Country"].value_counts(ascending=True).plot(kind="barh",linewidth=0.0)
	ax.set_title("Frquency of Winning Country")
	ax.set_xlabel("Number of Wins")
	ax.set_ylabel("Country")
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	ax.yaxis.labelpad = 20
	for index,p in enumerate(ax.patches):
		ax.annotate(str(p.get_width()), xy=(p.get_width()+0.4, p.get_y() + p.get_height()-0.3))
	plt.show()
	data = raw_data.loc[:,["Distance Cycled","Year","Country"]]
	cmap = cm.get_cmap('Spectral')
	country_hash = [hash(value) for value in data["Country"]]
	gen_winners = ["France","Belgium","Spain","Italy","Luxembourg","United States","Switzerland","United Kingdom","Netherlands","Ireland","Germany","Denmark","Australia"]
	color_map = ["#ff6666","#ff9966","#ffff80","#adebad","#85e0e0","#0099ff","#aa80ff","#ff99ff"
	,"#b3b300","#ffb84d","#996633", "#558000", "#ccccff"]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title("Distance Cycled over Time and Winning Country")
	ax.set_xlabel("Year")
	ax.set_ylabel("Distance Cycled (km)")
	scatter_plots = range(13)
	for index in range(len(gen_winners)):
		X = data[data["Country"] == gen_winners[index]].loc[:,["Year"]]
		Y = data[data["Country"] == gen_winners[index]].loc[:,["Distance Cycled"]]
		scatter_plots[index] = ax.scatter(x=X, y=Y,s=50,color=color_map[index],edgecolor='None')
	ax.set_axis_bgcolor('#262626')
	plt.legend(scatter_plots,gen_winners,scatterpoints=1,loc='lower right',ncol=4)
	#ax.plot([1985,1985],[2000,6000],"w--")
	axes = plt.gca()
	axes.set_ylim([2000,6000])
	ax.tick_params(axis='y', pad=20)
	ax.tick_params(axis='x', pad=10)
	ax.yaxis.labelpad = 10
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	plt.show()

# Show relationship between distance and winning time
if 0:
	raw_data = DataFrame.from_csv("../data/historic_wins.tsv", sep="\t",index_col=False, header=0)
	raw_data["Winning Time"] = [formatTimeTaken(time) for time in raw_data["Winning Time"]]
	raw_data = raw_data.dropna()
	raw_data = raw_data[raw_data["Year"]>=1913]
	data = raw_data.loc[:,["Distance Cycled","Winning Time","Year"]]
	data = data.sort(["Winning Time","Distance Cycled"],ascending=True)

	y = np.array(data["Distance Cycled"].fillna(np.mean(data["Distance Cycled"])))
	x = np.array(data["Winning Time"].fillna(np.mean(data["Winning Time"])))
	year = np.array(data["Year"])

	fig = plt.figure()
	ax = fig.add_subplot(111)

	coefs = poly.polyfit(x, y, deg=3)
	ffit = poly.Polynomial(coefs)
	ax.plot(x,y,ls='none',marker='o',color="#99ccff", markeredgewidth=0.0)
	y_hat = ffit(x)
	ax.plot(x,y_hat,"r--", linewidth=3)

	ax.set_title("Distance Cycled by Winning Time")
	ax.set_xlabel("Winning Time (hours)")
	ax.set_ylabel("Distance Cycled (km)")
	ax.yaxis.labelpad = 20
	ax.set_axis_bgcolor('#ffffff')
	ax.yaxis.grid(True)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(111)

	difference = y - y_hat
	ax.scatter(year,difference,marker='o',color="green")
	ax.plot([1903,2020],[0,0],"r--", linewidth=3)

	ax.set_title("Residual Plot (Distance/Time model errors over time)")
	ax.set_xlabel("Year")
	ax.set_ylabel("Residual")
	axes = plt.gca()
	axes.set_xlim([1903,2020])
	ax.set_axis_bgcolor('#ffffff')
	ax.yaxis.grid(True)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	plt.show()

# The first mountain stages (in the Pyrenees) appeared in 1910
# Until 1930 he demanded that riders mend their bicycles without help and that they use the same bicycle from start to end
# 1953 saw the introduction of the Green Jersey 'Points' competition. 
# in 1975, the same year the polka-dot jersey
# The mountains classification was added to the Tour de France in the 1933 edition
# yellow jersey was added to the race in the 1919 edition