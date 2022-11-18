import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Load the data
photophobiadata=pd.read_csv('/Users/frankhu/Moxytech/PhotophobiaData/data_test_V2_labeled.csv')
print(photophobiadata.shape)
# print(photophobiadata['Visits'])

# Sort data to pre & post

pretdcs = pd.DataFrame()
posttdcs = pd.DataFrame()

for i in range(0,photophobiadata.shape[0]):
    if '30 day' in str(photophobiadata['Visits'][i]):
       pretdcs=pd.concat([pretdcs,photophobiadata.loc[i:i]],axis =0)
       #print(i)
    if 'pre' in str(photophobiadata['Visits'][i]):
       pretdcs=pd.concat([pretdcs,photophobiadata.loc[i:i]],axis =0)
       #print(i)

    else:
       posttdcs=pd.concat([posttdcs,photophobiadata.loc[i:i]],axis =0)


#print(pretdcs.shape)
#print(posttdcs.shape)

# Plot the data for pre and post
plt.subplot(2,1,1)
ax1=plt.gca()
pretdcs.plot(y=['Average_intensity','Average_intensity.1'],ax=ax1,kind='line',grid=True,marker = 'o',use_index=True)
ax1.legend(["Left Cranium","Right Cranium"])
#plt.xticks(rotation=15)
plt.xlabel('Time')
plt.ylabel('Average Intensity')
plt.tight_layout()
plt.minorticks_on()

plt.subplot(2,1,2)
ax2=plt.gca()
pretdcs.plot(y=['Average_intensity.2','Average_intensity.3'],ax=ax2,kind='line',grid=True,marker = 'o',use_index=True)
ax2.legend(["Left Eye","Right Eye"])
#plt.xticks(rotation=15)
plt.xlabel('Time')
plt.ylabel('Average Intensity')
plt.tight_layout()
plt.minorticks_on()
plt.show()


# Fit a ploy to the data 
