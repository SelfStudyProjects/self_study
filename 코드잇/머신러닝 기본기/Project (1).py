#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 폰트 설정
plt.rc('font', family='NanumGothic')


# In[3]:


df_2017 = pd.read_csv('data/jeju_card_region_2017.csv')
df_2018 = pd.read_csv('data/jeju_card_region_2018.csv')
df_population = pd.read_csv('data/jeju_population.csv')


# In[4]:


# 2017년 데이터 확인
print(df_2017.info())
print(df_2017.describe())
print(df_2017.isnull().sum())


# In[5]:


print(df_2018.info())
print(df_2018.describe())
print(df_2018.isnull().sum())


# In[6]:


df_card = pd.concat([df_2017, df_2018], ignore_index=True)


# In[7]:


top_10_amount = df_card.groupby('업종명')['이용금액'].sum().sort_values(ascending=False).head(10)
print("이용금액이 많은 업종 Top 10:")
print(top_10_amount)


# In[8]:


# 이용자수가 많은 업종 Top 10
top_10_users = df_card.groupby('업종명')['이용자수'].sum().sort_values(ascending=False).head(10)
print("\n이용자수가 많은 업종 Top 10:")
print(top_10_users)


# In[9]:


# 인당 이용금액이 많은 지역 Top 10
df_card['인당이용금액'] = df_card['이용금액'] / df_card['이용자수']
top_10_per_capita = df_card.groupby('읍면동명')['인당이용금액'].mean().sort_values(ascending=False).head(10)
print("\n인당 이용금액이 많은 지역 Top 10:")
print(top_10_per_capita)


# In[12]:


# 인당 이용금액이 많은 지역의 업종 분석
for region in top_10_per_capita.index:
    print(f"\n{region} 지역의 상위 5개 업종:")
    print(df_card[df_card['읍면동명'] == region].groupby('업종명')['이용금액'].sum().sort_values(ascending=False).head())

# 카페 이용자수와 유동인구의 관계 분석
df_cafe = df_card[df_card['업종명'] == '카페'].groupby('읍면동명')[['이용자수', '이용금액']].sum().reset_index()

# 유동인구 데이터 전처리 (만약 필요하다면)
df_population['방문인구'] = df_population['방문인구'].astype(int)  # 데이터 타입 변환

# 카페 데이터와 유동인구 데이터 병합
df_merged = pd.merge(df_cafe, df_population, on='읍면동명', how='inner')

# 산점도 그리기
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_merged, x='방문인구', y='이용자수')
plt.title('카페 이용자수와 유동인구의 관계')
plt.xlabel('유동인구')
plt.ylabel('카페 이용자수')
plt.show()

# 상관계수 계산
correlation = df_merged['방문인구'].corr(df_merged['이용자수'])
print(f"\n카페 이용자수와 유동인구의 상관계수: {correlation:.2f}")

# 추가 분석: 유동인구와 이용금액의 관계
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_merged, x='방문인구', y='이용금액')
plt.title('유동인구와 카페 이용금액의 관계')
plt.xlabel('유동인구')
plt.ylabel('카페 이용금액')
plt.show()

correlation_amount = df_merged['방문인구'].corr(df_merged['이용금액'])
print(f"\n유동인구와 카페 이용금액의 상관계수: {correlation_amount:.2f}")


# In[13]:


print(df_population.columns)


# In[14]:


print(df_merged.head())
print(df_merged.dtypes)
print(df_merged.isnull().sum())


# In[19]:


print(df_merged['방문인구'].unique())
print(df_merged['이용자수'].unique())
print(df_merged['이용금액'].unique())


# In[17]:


df_merged['방문인구'] = pd.to_numeric(df_merged['방문인구'], errors='coerce')
df_merged['이용자수'] = pd.to_numeric(df_merged['이용자수'], errors='coerce')
df_merged['이용금액'] = pd.to_numeric(df_merged['이용금액'], errors='coerce')

df_merged = df_merged.dropna()


# In[18]:


plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_merged, x='방문인구', y='이용자수')
plt.title('카페 이용자수와 유동인구의 관계')
plt.xlabel('유동인구')
plt.ylabel('카페 이용자수')
plt.show()

correlation = df_merged['방문인구'].corr(df_merged['이용자수'])
print(f"\n카페 이용자수와 유동인구의 상관계수: {correlation:.2f}")

