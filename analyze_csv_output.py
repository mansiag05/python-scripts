##############################################################################################
#
# Description of csv File:  
# Column 0: Actual Label of the image
# Column 1-10:  Output of FC Layer
# Column 11-20: Calculating probability of a particular output. column[11] = (column[1]*100)
# Column 21-23: Top 3 Probabilities
# Column 24-26: Top 3 Probabilities Index
# Column 27   : Value=1 if the predicted label is equal to the actual label; else 0
#
##############################################################################################

##############################################################################################
#
#
# Here what we've seen is if two probablities have same the same value, then see if the 
# label of any of the equal probability is the correct label or not.
#
##############################################################################################

import pandas as pd
import numpy as np
import argparse
import os

def analyzing_fc_layer_output(input_file,output_file):
 
     df = pd.read_csv(input_file,header=None)
 
     # Firstly calculating percentage
     for i in range(1,11):
         df[i+10] = df[i]*100

     # Make dtype of column storing index as int64
     # for i in range(24,27):
     # df[i] = np.int64 

     # Find top 3 percentage values and their position
     for n, col in enumerate(df.T):
        top3 = df.iloc[:,11:21].T[col].nlargest(3)
        top3_val = top3.tolist()
        top3_val_pos = top3.index.tolist()
        for i in range(0,len(top3_val)):
           df.at[n,21+i] = top3_val[i]
        for i in range(0,len(top3_val_pos)):
           df.at[n,24+i] = top3_val_pos[i]-11

     # Calculate the percentage of correct observation 
     for index,row in df.iterrows():
        if df.at[index,0] == df.at[index,24]:
           df.at[index,27] = 1
        elif df.at[index,21]==df.at[index,22] and df.at[index,0]==df.at[index,25]:
           df.at[index,27] = 1
        elif df.at[index,21]==df.at[index,23] and df.at[index,0]==df.at[index,26]: 
           df.at[index,27] = 1
        else:
           df.at[index,27] = 0

     print("Fixed Point Top1 accuracy: ",(df[27].sum())/100)

     # Write the Top1 accuracy in csv file
     df.at[4,29] = "Top-1 Accuracy"
     df.at[5,29] = (df[27].sum())/100
       
     # Write dataframe to a file
     df.to_csv(output_file)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--i", help="input csv File")
  parser.add_argument("--o", help="output csv File")
  args = parser.parse_args()
  analyzing_fc_layer_output(args.i, args.o)
