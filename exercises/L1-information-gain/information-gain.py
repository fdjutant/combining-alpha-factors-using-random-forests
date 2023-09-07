import numpy as np
import pandas as pd

def entropy_fn(event):
    
    entropy = 0
    total_event = sum(event)
    for i in range(len(event)):
        p = event[i] / total_event
        entropy += -p * np.log2(p)

    return entropy

df = pd.read_csv('ml-bugs.csv')
print(df)

def parent_entropy(df):

    freq_Mobug = 0
    for index, row in df.iterrows():
        if row['Species'] == 'Mobug':
            freq_Mobug += 1

    total_data = len(df)
    entropy =  -1 * (freq_Mobug/total_data * np.log2(freq_Mobug/total_data) +\
                    (total_data-freq_Mobug)/total_data *\
                    np.log2((total_data-freq_Mobug)/total_data) )
    
    return entropy

def child_entropy(df, input):

    # Loop through the DataFrame using iterrows()
    freq_Mobug_ch1 = 0
    freq_Mobug_ch2 = 0
    total_ch1 = 0
    total_ch2 = 0
    if type(input) == str:
        
        for index, row in df.iterrows():
            if row['Color'] == input:
                total_ch1 += 1
                if row['Species'] == 'Mobug':
                    freq_Mobug_ch1 += 1
            else:
                total_ch2 += 1
                if row['Species'] == 'Mobug':
                    freq_Mobug_ch2 += 1
                    
    elif type(input) == float:
        
        for index, row in df.iterrows():
            if row['Length (mm)'] < input:
                total_ch1 += 1
                if row['Species'] == 'Mobug':
                    freq_Mobug_ch1 += 1
            else:
                total_ch2 += 1
                if row['Species'] == 'Mobug':
                    freq_Mobug_ch2 += 1

    total_data = len(df)
    ch1_entropy = -1 * (freq_Mobug_ch1/total_ch1 * np.log2(freq_Mobug_ch1/total_ch1) +\
                       (total_ch1-freq_Mobug_ch1)/total_ch1 *\
                       np.log2((total_ch1-freq_Mobug_ch1)/total_ch1) )
    
    ch2_entropy = -1 * (freq_Mobug_ch2/total_ch2 * np.log2(freq_Mobug_ch2/total_ch2) +\
                       (total_ch2-freq_Mobug_ch2)/total_ch2 *\
                       np.log2((total_ch2-freq_Mobug_ch2)/total_ch2) )
    
    ch_entropy = (total_ch1/total_data) * ch1_entropy +\
                 (total_ch2/total_data) * ch2_entropy
    
    return ch_entropy

parent_entropy = parent_entropy(df)
green_entropy = child_entropy(df, 'Green')
blue_entropy = child_entropy(df, 'Blue')
brown_entropy = child_entropy(df, 'Brown')
lessthan_17_entropy = child_entropy(df, 17.0)
lessthan_20_entropy = child_entropy(df, 20.0)

print('parent entropy\t: {:.4f}'.format(parent_entropy))
print('green entropy\t: {:.4f}'.format(parent_entropy-green_entropy))
print('blue entropy\t: {:.4f}'.format(parent_entropy-blue_entropy))
print('brown entropy\t: {:.4f}'.format(parent_entropy-brown_entropy))
print('<17 entropy\t: {:.4f}'.format(parent_entropy-lessthan_17_entropy))
print('<20 entropy\t: {:.4f}'.format(parent_entropy-lessthan_20_entropy))