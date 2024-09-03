#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 필요한 라이브러리 import
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False


# In[3]:


df = pd.read_csv('data/jeju_card.csv')


# In[4]:


print(df.shape)


# In[5]:


print(df.dtypes)


# In[6]:


print(df.describe())


# In[7]:


print(df.isnull().sum())


# In[8]:


for col in df.columns:
    print(f"{col}: {df[col].unique()}")


# In[9]:


df = df.copy()
df['년도'] = pd.to_datetime(df['연월']).dt.year


# In[10]:


df = df.copy()
df['년도'] = pd.to_datetime(df['연월']).dt.year


# In[16]:


monthly_usage = df.groupby('연월')['이용금액'].sum().reset_index()
monthly_usage['연월'] = monthly_usage['연월'].astype(str)
plt.figure(figsize=(12, 6))
sns.lineplot(x='연월', y='이용금액', data=monthly_usage)
plt.title('연월별 카드 이용 추이')
plt.xticks(rotation=45)
plt.show()


# In[17]:


plt.show()


# In[19]:


age_group_usage = df.groupby('연령대')[['이용금액', '이용자수']].sum().reset_index()
age_group_usage['1회당 소비금액'] = age_group_usage['이용금액'] / age_group_usage['이용자수']

plt.figure(figsize=(15, 5))
plt.subplot(131)
sns.barplot(x='연령대', y='이용자수', data=age_group_usage)
plt.title('연령대별 이용자수')

plt.subplot(132)
sns.barplot(x='연령대', y='이용금액', data=age_group_usage)
plt.title('연령대별 소비금액')

plt.subplot(133)
sns.barplot(x='연령대', y='1회당 소비금액', data=age_group_usage)
plt.title('연령대별 1회당 소비금액')

plt.tight_layout()
plt.show()


# In[23]:


age_industry_usage = df.groupby(['연령대', '업종명'])['이용금액'].sum().reset_index()
age_industry_usage = age_industry_usage.sort_values(['연령대', '이용금액'], ascending=[True, False])


# In[25]:


num_age_groups = len(age_group_usage['연령대'].unique())

# 그리드 크기 계산
rows = (num_age_groups + 1) // 2  # 올림 나눗셈
cols = 2

plt.figure(figsize=(15, 5 * rows))
for i, age in enumerate(age_group_usage['연령대'].unique()):
    plt.subplot(rows, cols, i+1)
    data = age_industry_usage[age_industry_usage['연령대'] == age].head(5)
    sns.barplot(x='업종명', y='이용금액', data=data)
    plt.title(f'{age} 연령대 Top 5 지출 업종')
    plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# In[ ]:


age_monthly_usage = df.groupby(['연령대', '연월'])['이용금액'].sum().reset_index()

age_monthly_usage['연월'] = pd.to_datetime(age_monthly_usage['연월'])

plt.figure(figsize=(12, 8))
sns.lineplot(x='연월', y='이용금액', hue='연령대', data=age_monthly_usage)
plt.title('연령대별 연월별 카드 이용 추이')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# In[ ]:




