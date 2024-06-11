%matplotlib inline
import pandas as pd

df = pd.read_csv('data/movie_metadata.csv')

# IQR 계산하기

q1 = df['budget'].quantile(0.25)
q3 = df['budget'].quantile(0.75)
iqr = q3 - q1

# 이상점 제거하기

condition = (df['budget'] > q3 + 5 * iqr)
df.drop(df[condition].index, inplace = True)

# 산점도 그리기
df.plot(kind = 'scatter', x = 'budget', y = 'imdb_score')