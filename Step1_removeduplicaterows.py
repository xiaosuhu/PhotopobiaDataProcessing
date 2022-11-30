import pandas as pd

df = pd.read_csv('/Users/frankhu/Moxytech/PhotophobiaData/PainData20221130.csv')
df.drop_duplicates(subset='geopaindata', inplace=True)
df.to_csv('/Users/frankhu/Moxytech/PhotophobiaData/PainData20221130edit.csv', index=False)
