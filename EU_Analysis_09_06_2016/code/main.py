import pandas
from pandas import DataFrame


# Read in data into Pandas Dataframe
prod_Data = DataFrame.from_csv("../data/Production_In_Industry_Monthly.tsv", sep=",")
