import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

def findRange(value,ranges,range_text):
	if pandas.isnull(value):
		return value
	range_index = 0;
	for index,threshold in enumerate(ranges):
		if value>= threshold:
			range_index = index
	return range_text[range_index]

data = DataFrame.from_csv("../data/Transparency_Register.csv", sep=",", index_col=False, header=0)
	#print data["Estimate of costs (as a range)"].value_counts()

# Extracting top ten countries
top_five_countries = ["Belgium","Germany","United Kingdom","France","Italy"]
data = data[data["Head office country"].isin(top_five_countries)]

first_bucket = ["0-9999","10000-24999","25000-49999","50000-99999","100000-199999","200000-299999","300000-399999","400000-499999","500000-599999","600000-699999","700000-799999","800000-899999","900000-999999","1000000-1249999"]
second_bucket = ["1250000-1499999","1500000-1749000","1750000-1999999","2000000-2249999","2250000-2499999"]
third_bucket = ["2500000-2749000","2750000-2999999","3000000-3249999","3250000-3499999","3500000-3749000"]
fourth_bucket = ["3750000-3999999","4000000-4249999","4250000-4499999","4500000-4749000","4750000-4999999"]
fifth_bucket = ["5000000-5249999","5250000-5499999","6000000-6249999","6250000-6499999","7250000-7499999","7750000-7999999","8000000-8249999","8750000-8999999","9000000-9249999","9750000-9999999",">10000000"]
ranges = [0, 1250000,2500000,3750000,5000000]
range_text = ["0 - 1,249,999","1,250,000 - 2,499,999","2,500,000 - 3,749,999" , "3,750,000 - 4,999,999", ">5,000,000"]
for index,row in data.iterrows():
	if pandas.isnull(row["Estimate of costs (as a range)"]):
		data.set_value(index,"Estimate of costs (as a range)",findRange(row["Estimate of costs (absolute amount)"],ranges,range_text))
	if row["Estimate of costs (as a range)"] in first_bucket:
		data.set_value(index,"Estimate of costs (as a range)","0 - 1,249,999")

	if  row["Estimate of costs (as a range)"] in second_bucket:
		data.set_value(index,"Estimate of costs (as a range)","1,250,000 - 2,499,999")

	if  row["Estimate of costs (as a range)"] in third_bucket:
		data.set_value(index,"Estimate of costs (as a range)","2,500,000 - 3,749,999")

	if  row["Estimate of costs (as a range)"] in fourth_bucket:
		data.set_value(index,"Estimate of costs (as a range)","3,750,000 - 4,999,999")

	if  row["Estimate of costs (as a range)"] in fifth_bucket:
		data.set_value(index,"Estimate of costs (as a range)",">5,000,000")

data = data.loc[:,["Head office country","Estimate of costs (as a range)"]]


temp = data[data["Head office country"]=="Germany"]
ax = temp["Estimate of costs (as a range)"].value_counts().reindex(range_text).fillna(0).plot(kind="barh", linewidth=0.0,color="green", log=True)
ax.set_axis_bgcolor('white')
ax.set_title("Germany")
ax.set_xlabel("Number of groups (log)")
ax.set_ylabel("Cost range of lobbying action (Euros)")
ax.yaxis.labelpad = 20
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none')
for index,p in enumerate(ax.patches):
	print p.get_width()+((1/(index+1))*1000)
	ax.annotate(str(p.get_width()), xy=(p.get_width()+((1.1/(index+1))*8), p.get_y() +(p.get_height()/3)))
plt.show()