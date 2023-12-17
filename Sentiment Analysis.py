#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pd.set_option('display.max_rows', None)


# # NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) tool 

# In[2]:


get_ipython().system('pip install textblob nltk')
import nltk
nltk.download('vader_lexicon')


# In[3]:


sample_df = pd.read_csv('cleaned_sample_dataset.csv')


# In[4]:


from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

sample_df['review_sentiment'] = sample_df['text'].apply(lambda x: sia.polarity_scores(x)['compound'])

# The 'sentiment' column will now have compound sentiment scores
sample_df['review_sentiment'].head()


# # Aggregate to Calculate Average Sentiment Scores for each business

# In[5]:


# Calculate the average sentiment
average_sentiment = sample_df.groupby('business_id')['review_sentiment'].mean().reset_index()

# Rename the aggregated sentiment score column
average_sentiment = average_sentiment.rename(columns={'review_sentiment': 'average_sentiment'})



# # Merge with Business Attributes

# In[6]:


sample_df = sample_df.merge(average_sentiment, on='business_id', how='left')


# In[7]:


sample_df.info()


# # Exploratory Data Analysis (EDA)

# In[8]:


sample_df = sample_df.drop(['review_id','user_id','business_id','text','latitude', 'longitude'], axis=1)


# In[9]:


# Filtering to keep rows where the 'categories' column contains 'restaurant'
sample_df = sample_df[sample_df['categories'].str.contains('restaurant', case=False, na=False)]


# In[10]:


#drop the filter categories
sample_df = sample_df.drop(['categories'], axis=1)


# In[11]:


for column in sample_df.columns:
    if sample_df[column].dtype == 'bool':
        sample_df[column] = sample_df[column].astype(int)


# In[12]:


sample_df.info()


# In[14]:


sample_df.to_csv('sample_df.csv', index=False)


# In[20]:


import seaborn as sns
import matplotlib.pyplot as plt

correlation_matrix = heatmap_df.corr()

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Draw the heatmap
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')

# Show the plot
plt.show()




# In[21]:


correlation_matrix


# In[4]:


correlation_matrix = heatmap_df.corr()


# In[5]:


# Get the 'average_sentiment' column to find its correlation with other columns
average_sentiment_correlation = correlation_matrix['average_sentiment'].sort_values()

# Top 10 negative correlations with 'average_sentiment'
top_negative_correlations = average_sentiment_correlation.head(10)

# Top 10 positive correlations with 'average_sentiment' (excluding the 'average_sentiment' column itself)
top_positive_correlations = average_sentiment_correlation.drop(labels=['average_sentiment']).tail(10)

top_negative_correlations, top_positive_correlations


# In[ ]:




