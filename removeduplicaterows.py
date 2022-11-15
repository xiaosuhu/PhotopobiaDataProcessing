import pandas as pd

df = pd.read_csv('PainData20221010.csv')
df.drop_duplicates(subset='metadata', inplace=True)
df.to_csv('PainData20221010edit.csv', index=False)
