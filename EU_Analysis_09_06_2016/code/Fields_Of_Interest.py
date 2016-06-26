import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

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