import pandas as pd

df = pd.read_csv('data/ab_data.csv')
duplicates = df[df.drop(columns=['timestamp']).duplicated(keep=False)]
df = df.drop_duplicates(subset='user_id', keep='first')
duplicates = df[df['user_id'].duplicated(keep=False)]
pd.crosstab(df['group'], df['landing_page'])