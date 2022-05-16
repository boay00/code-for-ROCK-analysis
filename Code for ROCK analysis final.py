from numpy import mean, median, take, std, var, percentile, quantile

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import re

# dataframe (df)

# enter file pathname
df = pd.read_excel('')

# print(df)

stage_array = df["stage"].to_numpy()

# set width to > 1
frame_blip_width = 0

def has_blip_occurred(window):
    for i in range(1, frame_blip_width+1):
        window_string = ''.join(map(str, window[0:i+2]))

        regex = re.compile(fr'(?P<number>[\d])(\d)\2{{{i-1}}}?(?P=number)')

        if re.match(regex, window_string):
            return True
    return False

def is_valid_stage_change(window):
    first_value = window[0]
    current_value = window[1]

    # potential stage change
    if current_value != first_value:
        if has_blip_occurred(window):
            return 'change_value'

        return 'valid'

output = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
}

count = 0
current_stage = 0

for i in range(0,len(stage_array)-1):
    prev_value = stage_array[i-1]
    current_value = stage_array[i]
    next_value = stage_array[i+1]

    indices = range(i-1, i+frame_blip_width+1)
    window = stage_array.take(indices, mode='wrap')

    if i == 0:
        prev_value = current_value

    if i == len(stage_array) - 1:
        output[current_stage] = [*output[current_stage], count + 1]

    # switching stages
    if is_valid_stage_change(window) == 'change_value':
        df.at[i, 'stage'] = prev_value
    elif is_valid_stage_change(window) == 'valid':
        output[current_stage] = [*output[current_stage], count]
        count = 1
        current_stage = current_value
        continue
    
    # start setup
    if count == 0:
        current_stage = current_value
        count += 1
    # normal increment of count
    else:
        count += 1

# print(output)

averages = {}
# st_dev = {}
# variance = {}
# quants = {}

for stage in output:
    averages[stage] = mean(output[stage])
    
    #st_dev[stage] = std(output[stage])
    
    #variance[stage] = var(output[stage])
    
    #quants[stage] = quantile(output[stage], 0.75)
    
print(averages)
# print(st_dev)
# print(variance)
# print(quants)

# all violin plot code below

#sns.set_theme(style="whitegrid")
#tips = sns.load_dataset("tips")
#ax = sns.violinplot(y=output[5], palette = ['green'])
#plt.ylim(-1, 40)
#ax.yaxis.set_major_locator(plt.MaxNLocator(10))
#ax.set_xlabel('M', fontsize = 15)
#ax.set_ylabel('Duration / Frames', fontsize = 15)
#ax.set_title('CM', fontsize = 20)

# plt.violin(range(len(output)), len([]), tick_label=stage)
#plt.show()



# mutated excel file with specified filename
df.to_excel('')
