## from jupyter notebook on wdcsol0000006


import pandas as pd
from pandas import DataFrame, read_csv
fileloc = r'C:\geoevent_input\spire\5570_Suez_Canal_Pers_Gulf_Merge.csv' #position_2017_09_01.csv
df = pd.read_csv(fileloc) # will import huge things quickly 
df.head() # shows the first five rows
df.columns # examine all the columns
ldf = df.iloc[1:1000,:] #takes the first thousand records and turns it into ldf
ldf.to_csv(r'C:\geoevent_input\spire\first1kboats.csv') # export to new CSV as manageable size
ldf.iloc[2] # pulls back just #2 record
ldf.rot[0:10] # gets the first 10 values in the 'rot' column
for i, row in enumerate(ldf.values): # to iterate through a df and filter
    if (pd.isnull(ldf.rot[ldf.index[i]])): # pd.isnull checks for NaN
        print(str(ldf.mmsi[ldf.index[i]]) +" has a null rot")
len(df.index)
