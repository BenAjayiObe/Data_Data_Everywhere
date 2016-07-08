import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

# Meta Data

# indic_bt = Production
# nace_r2 = NACE Rev.2 Code
# s_adj = statistical adjustment, look into it yourself
# unit = what the number actually means (e.g. pch_sm means percentage change over same period in the previous year)


def findRange(value,ranges,range_text):
	if pandas.isnull(value):
		return value
	range_index = 0;
	for index,threshold in enumerate(ranges):
		if value>= threshold:
			range_index = index
	return range_text[range_index]


if 0:
	# Read in data into Pandas Dataframe
	prod_Data = DataFrame.from_csv("../data/Production_In_Industry_Monthly.tsv", sep=",",index_col=False, header=None)

	#prod_Data_Food = prod_Data.loc[prod_Data['nace_r2'] == "B"]
	#print prod_Data_Food

	# Split the dataframe into two based on delimiter character used.
	data_Column = prod_Data.iloc[:,[4]]
	indic_Column = prod_Data.iloc[:,[0,1,2,3]]

	# creating dataframe from single column seperated by tabs
	foo = lambda x: pandas.Series([i for i in reversed(x.split('\t'))])
	data_Column = data_Column.iloc[:,0].apply(foo)

	# Function to clean each element in dataframe
	def cleaner(col):
		return col.map(lambda x: str(x).rstrip('pseci ').replace(":","nan"))

	# applying string cleaning function to each element
	data_Column = data_Column.iloc[:,:437].apply(cleaner, axis=1)

	# combing the two datasets
	data = pandas.concat([indic_Column,data_Column], axis=1)

	# setting the column headers as the first line
	data.columns = data.iloc[0]
	data.reindex(data.index.drop(0))
	data = data[1:]
	#test = data[data['nace_r2'] == "B"]
	#test = test[test['s_adj'] == "CA"]
	test = data
	columns_names = list(test)
	#print columns_names
	columns_names.insert(0,columns_names.pop(columns_names.index("geo\\tim")))
	test = test.ix[:,columns_names]

	# test = test.iloc[:,6:]
	# cols = list(test)
	# for name in cols:
	# 	print name
	# 	test[name] = test[name].astype(float).fillna(0.0)
	test.to_csv("../data/Clean_Production_In_Industry_Monthly.csv", sep="\t", index=False)

if 0:
	clean_Data = DataFrame.from_csv("../data/Clean_Production_In_Industry_Monthly.csv", sep="\t",index_col=False, header=0)
	#test['2016M02'].plot()
	#plt.show(block=True)
	test = clean_Data.iloc[:,6:]
	attr_data = clean_Data.iloc[:,:5]
	cols = list(test)
	for name in cols:
		test[name] = test[name].astype(float).fillna(0.0)
	data = pandas.concat([attr_data,test],axis=1)

	data = data[data["nace_r2"] == "C"]
	data = data[data["unit"] == "PCH_PRE"]
	data = data.drop(data.columns[[1,2,3,4]],axis=1)
	# Manually realocate DE to the right coloumn on the very last line.

	countries = DataFrame.from_csv("../data/Country_Code.csv", sep=",", index_col=False, header=0)
	for index, value in data.iterrows():
		for x, row in countries.iterrows():
			if value[0] == row[0]:
				data.ix[index,0] = row[1]
				break;
	data = data.transpose()
	data = data.drop("geo\\tim")
	print data
	data.plot(kind="line")
	plt.show(block=True)
	#test.iloc[49].plot(kind='line')
	#plt.show(block=True)

if 0:


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
#data = data.transpose()
#plot_data = data.groupby(['Head office country', 'Estimate of costs (as a range)'])['Head office country'].count().unstack("Estimate of costs (as a range)").fillna(0)
#print plot_data

# Break down of top five countries cost brackets

if 0:
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


#  TOP TEN COUNTRIES WITH MOST REGISTERED GROUPS
if 1:
	data = DataFrame.from_csv("../data/Transparency_Register.csv", sep=",", index_col=False, header=0)
	print data["Head office country"].value_counts()

	# Extracting top ten countries
	top_ten_countries = ["Belgium","Germany","United Kingdom","France","Italy","Spain","Netherlands","United States","Austria","Sweden"]
	data = data[data["Head office country"].isin(top_ten_countries)]
	ax = data["Head office country"].value_counts().plot(kind="bar", linewidth=0.0)
	ax.set_axis_bgcolor('white')
	ax.set_title("Top Ten Registered Countries")
	ax.set_xlabel("Country")
	ax.set_ylabel("Number of Groups Registered")
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
	for p in ax.patches:
		ax.annotate(str(p.get_height()), xy=(p.get_x()+0.02, p.get_height()+30))
	#ax.get_xaxis().set_ticks([])
	#ax.get_yaxis().set_ticks([])
	#plot_data.plot(kind="bar", stacked=True)
	#plt.savefig("../Charts/Top_Ten_Countries_absolute.png")
	plt.show(block=True)

if 0:
	if 0:
		data = DataFrame.from_csv("../data/Transparency_Register.csv", sep=",", index_col=False, header=0)
		top_ten_countries = ["Belgium","United Kingdom","Germany","France","United States","Spain","Italy","Netherlands","Austria","Sweden"]
		country_data = data["Head office country"]
		#data = data[data["Head office country"].isin(top_ten_countries)]
		data = data.loc[:,["Head office country","Fields of interest"]]
		#country_data = data["Head office country"]]

		foo = lambda x: pandas.Series([i for i in reversed(x.split('\t\t'))])
		data = data.iloc[:,1].apply(foo)
		#print len(np.unique(data[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]].values))
		columns = ['Agriculture and Rural Development','Audiovisual and Media','Budget',
		 'Climate Action','Communication','Competition','Consumer Affairs',
		 'Culture','Customs','Development','Economic and Financial Affairs',
		 'Education','Employment and Social Affairs','Energy','Enlargement',
		 'Enterprise','Environment','External Relations',
		 'Financial Services and Capital Markets Union','Financial Stability',
		 'Fisheries and Aquaculture','Food Safety',
		 'Foreign and Security Policy and Defence',
		 'General and Institutional Affairs','Home Affairs','Humanitarian Aid',
		 'Information Society','Internal Market','Justice and Fundamental Rights',
		 'Public Health','Regional Policy','Research and Technology','Sport',
		 'Taxation','Trade','Trans-European Networks','Transport','Youth']
		field_data = pandas.DataFrame(columns=columns)
		for index, row in data.iterrows():
			print index
			#field_data.loc[index] = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
			for col in row:
				if pandas.isnull(col)==0:
					#field_data.iloc[index,[str(col)]] = 1
					field_data.set_value(index,col,1)
		print field_data
		field_data = pandas.concat([country_data,field_data], axis=1)
		plot_data = field_data.groupby(['Head office country'])[['Agriculture and Rural Development','Audiovisual and Media','Budget',
		 'Climate Action','Communication','Competition','Consumer Affairs',
		 'Culture','Customs','Development','Economic and Financial Affairs',
		 'Education','Employment and Social Affairs','Energy','Enlargement',
		 'Enterprise','Environment','External Relations',
		 'Financial Services and Capital Markets Union','Financial Stability',
		 'Fisheries and Aquaculture','Food Safety',
		 'Foreign and Security Policy and Defence',
		 'General and Institutional Affairs','Home Affairs','Humanitarian Aid',
		 'Information Society','Internal Market','Justice and Fundamental Rights',
		 'Public Health','Regional Policy','Research and Technology','Sport',
		 'Taxation','Trade','Trans-European Networks','Transport','Youth']].sum().fillna(0)

		plot_data.to_csv("../data/Field_Of_Interest_Count_Per_Country.csv", sep="\t")
	columns = ['Agriculture and Rural Development','Audiovisual and Media','Budget',
	 'Climate Action','Communication','Competition','Consumer Affairs',
	 'Culture','Customs','Development','Economic and Financial Affairs',
	 'Education','Employment and Social Affairs','Energy','Enlargement',
	 'Enterprise','Environment','External Relations',
	 'Financial Services and Capital Markets Union','Financial Stability',
	 'Fisheries and Aquaculture','Food Safety',
	 'Foreign and Security Policy and Defence',
	 'General and Institutional Affairs','Home Affairs','Humanitarian Aid',
	 'Information Society','Internal Market','Justice and Fundamental Rights',
	 'Public Health','Regional Policy','Research and Technology','Sport',
	 'Taxation','Trade','Trans-European Networks','Transport','Youth']
	plot_data = DataFrame.from_csv("../data/Field_Of_Interest_Count_Per_Country.csv", sep="\t", index_col=False, header=0)
	plot_data = plot_data[plot_data['Head office country']=="Belgium"]
	plot_data = plot_data.ix[:, plot_data.columns != 'Head office country']
	plot_data = plot_data.transpose()

	ax = plot_data.plot(kind="barh", color="purple")
	#ax.tick_params(axis='y',direction='up', pad=2)
	ax.set_title("Belgium, Num of Groups Per Fields of Interest")
	ax.set_xlabel("Number of Groups")
	ax.set_ylabel("Field of Interest")
	ax.yaxis.labelpad = 20
	# Hide the right and top spines
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(True)
	#ax.yaxis.set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none')
	ax.legend().set_visible(False)
	plt.show()
# 8 Artificial ranges,
# 0 - 1,249,999 			["0-9999","10000-24999","25000-49999","50000-99999","100000-199999","200000-299999","300000-399999","400000-499999","500000-599999","600000-699999","700000-799999","800000-899999","900000-999999","1000000-1249999"]
# 1,250,000 - 2,499,999 	["1250000-1499999","1500000-1749000","1750000-1999999","2000000-2249999","2250000-2499999"]
# 2,500,000 - 3,749,999 	["2500000-2749000","2750000-2999999","3000000-3249999","3250000-3499999","3500000-3749000"]
# 3,750,000 - 4,999,999 	["3750000-3999999","4000000-4249999","4250000-4499999","4500000-4749000","4750000-4999999"]
# >=5,000,000 				["5000000-5249999","5250000-5499999","6000000-6249999","6250000-6499999","7250000-7499999","7750000-7999999","8000000-8249999","8750000-8999999","9000000-9249999","9750000-9999999",">10000000"]

# 6,250,000 - 6,499,999 	"6250000-6499999"
# 6,500,000 - 7,749,999 	"7250000-7499999"
# 7,750,000 - 9,999,999 	"7750000-7999999" "8000000-8249999" "8750000-8999999" "9000000-9249999" "9750000-9999999"
# >= 10,000,000 			">10000000"

# 0 - 799,999 				"0-9999","10000-24999","25000-49999","50000-99999","100000-199999","200000-299999","300000-399999","400000-499999","500000-599999","600000-699999","700000-799999"
# 800,000 - 1,499,999 		"800000-899999","900000-999999","1000000-1249999","1250000-1499999"
# 1,500,000 - 2,499,999 	"1500000-1749000","1750000-1999999","2000000-2249999","2250000-2499999"
# 2,500,000 - 3,499,999 	
# > 3,500,000 				

#Belgium                           1904
#Germany                           1185
#United Kingdom                    1044
#France                             943
#Italy                              671
#Spain                              562
#Netherlands                        480
#United States                      322
#Austria                            204
#Sweden                             191


["0-9999","10000-24999","25000-49999","50000-99999","100000-199999","200000-299999","300000-399999","400000-499999",
"500000-599999""600000-699999","700000-799999","800000-899999","900000-999999","1000000-1249999","1250000-1499999",
"1500000-1749000","1750000-1999999","2000000-2249999","2250000-2499999","2500000-2749000","2750000-2999999","3000000-3249999",
"3250000-3499999","3500000-3749000","3750000-3999999","4000000-4249999","4250000-4499999","4500000-4749000","4750000-4999999",
"5000000-5249999","5250000-5499999","6000000-6249999","6250000-6499999","7250000-7499999","7750000-7999999","8000000-8249999",
"8750000-8999999","9000000-9249999","9750000-9999999",">10000000"]

[0,10000,25000,50000,100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000,1250000,1500000,1750000
,2000000,2250000,2500000,2750000,3000000,3250000,3500000,3750000,4000000,4250000,4500000,4750000,5000000,5250000
,6000000,6250000,7250000,7750000,8000000,8750000,9000000,9750000,10000000]


["Belgium","United Kingdom","Germany","France","United States","Spain","Italy","Netherlands","Austria","Sweden"]

["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37"]