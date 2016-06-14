import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt

# Meta Data

# indic_bt = Production
# nace_r2 = NACE Rev.2 Code
# s_adj = statistical adjustment, look into it yourself
# unit = what the number actually means (e.g. pch_sm means percentage change over same period in the previous year)

# Read in data into Pandas Dataframe
prod_Data = DataFrame.from_csv("../data/Production_In_Industry_Monthly.tsv", sep=",",index_col=None, header=None)

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
data.reindex(data.index.drop(0))
data = data[1:]
#test = data[data['nace_r2'] == "B"]
#test = test[test['s_adj'] == "CA"]
test = data
columns_names = list(test)
#print columns_names
columns_names.insert(0,columns_names.pop(columns_names.index("geo\\tim")))
test = test.ix[:,columns_names]

test = test.iloc[:,5:]
cols = list(test)
for name in cols:
	print name
	test[name] = test[name].astype(float).fillna(0.0)
test.to_csv("../data/Clean_Production_In_Industry_Monthly.csv", sep="\t")

#test['2016M02'].plot()
#plt.show(block=True)

test.iloc[49].plot(kind='line')
plt.show(block=True)