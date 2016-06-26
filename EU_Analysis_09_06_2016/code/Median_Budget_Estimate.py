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
top_ten_countries = ["Belgium","Germany","United Kingdom","France","Italy","Spain","Netherlands","United States","Austria","Sweden"]
data = data[data["Head office country"].isin(top_ten_countries)]
#countries = data["Head office country"].unique()
#print data["Estimate of costs (as a range)"].unique()
#print len(budget_ranges)

#for country in countries:
#	print country + " " + str(len(data[data["Head office country"] == country]))

first_bucket = ["0-9999","10000-24999","25000-49999","50000-99999","100000-199999","200000-299999","300000-399999","400000-499999","500000-599999","600000-699999","700000-799999","800000-899999","900000-999999","1000000-1249999"]
second_bucket = ["1250000-1499999","1500000-1749000","1750000-1999999","2000000-2249999","2250000-2499999"]
third_bucket = ["2500000-2749000","2750000-2999999","3000000-3249999","3250000-3499999","3500000-3749000"]
fourth_bucket = ["3750000-3999999","4000000-4249999","4250000-4499999","4500000-4749000","4750000-4999999"]
fifth_bucket = ["5000000-5249999","5250000-5499999","6000000-6249999","6250000-6499999","7250000-7499999","7750000-7999999","8000000-8249999","8750000-8999999","9000000-9249999","9750000-9999999",">10000000"]
ranges = [0,10000,25000,50000,100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000,1250000,1500000,1750000
			,2000000,2250000,2500000,2750000,3000000,3250000,3500000,3750000,4000000,4250000,4500000,4750000,5000000,5250000
			,6000000,6250000,7250000,7750000,8000000,8750000,9000000,9750000,10000000]
range_text = ["0-9999","10000-24999","25000-49999","50000-99999","100000-199999","200000-299999","300000-399999","400000-499999",
			"500000-599999","600000-699999","700000-799999","800000-899999","900000-999999","1000000-1249999","1250000-1499999",
			"1500000-1749000","1750000-1999999","2000000-2249999","2250000-2499999","2500000-2749000","2750000-2999999","3000000-3249999",
			"3250000-3499999","3500000-3749000","3750000-3999999","4000000-4249999","4250000-4499999","4500000-4749000","4750000-4999999",
			"5000000-5249999","5250000-5499999","6000000-6249999","6250000-6499999","7250000-7499999","7750000-7999999","8000000-8249999",
			"8750000-8999999","9000000-9249999","9750000-9999999",">10000000"]

for index,row in data.iterrows():
	if pandas.isnull(row["Estimate of costs (as a range)"]):
		data.set_value(index,"Estimate of costs (as a range)",findRange(row["Estimate of costs (absolute amount)"],ranges, range_text))

data = data.loc[:,["Head office country","Estimate of costs (as a range)"]]
range_median = {"0-9999":500,"10000-24999":15000,"25000-49999":25000,"50000-99999":75000,"100000-199999":150000,
"200000-299999":250000,"300000-399999":350000,"400000-499999":450000,"500000-599999":550000,"600000-699999":650000,
"700000-799999":750000,"800000-899999":850000,"900000-999999":950000,"1000000-1249999":1125000,"1250000-1499999":1375000,
"1500000-1749000":1625000,"1750000-1999999":1875000,"2000000-2249999":2125000,"2250000-2499999":2375000,"2500000-2749000":2625000,
"2750000-2999999":2875000,"3000000-3249999":3125000,"3250000-3499999":3375000,"3500000-3749000":3625000,"3750000-3999999":3875000,
"4000000-4249999":4125000,"4250000-4499999":4375000,"4500000-4749000":4625000,"4750000-4999999":4875000,"5000000-5249999":5125000,
"5250000-5499999":5375000,"6000000-6249999":6125000,"6250000-6499999":6375000,"7250000-7499999":7375000,"7750000-7999999":7875000,
"8000000-8249999":8125000,"8750000-8999999":8875000,"9000000-9249999":9125000,"9750000-9999999":9875000,">10000000":10000000}
data['Estimate of costs (as a range)'] = data['Estimate of costs (as a range)'].replace(range_median, inplace=False)
plot_data = data.groupby(['Head office country'])[['Estimate of costs (as a range)']].sum().sort('Estimate of costs (as a range)', ascending=False).fillna(0) #.sort_values('Estimate of costs (as a range)').index]
print plot_data
ax = plot_data.plot(kind="bar", linewidth=0.0, color='green')
top_ten_countries = ["Belgium","Germany","United Kingdom","France","Italy","Spain","Netherlands","United States","Austria","Sweden"]
ax.set_axis_bgcolor('white')
ax.set_title("Total spent on Lobbying (Top Ten Registered Countries)")
ax.set_xlabel("Country")
ax.set_ylabel("Total spent on Lobbying (Approximation)")
ax.set_xticklabels(top_ten_countries)
ax.set_yticklabels([])
# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
#ax.yaxis.set_visible(False)
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none')
ax.legend().set_visible(False)
for p in ax.patches:
	ax.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()),va='bottom', rotation=45)
plt.show(block=True)