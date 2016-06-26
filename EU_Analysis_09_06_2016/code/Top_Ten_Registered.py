import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

data = DataFrame.from_csv("../data/Transparency_Register.csv", sep=",", index_col=False, header=0)

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
plt.show(block=True)