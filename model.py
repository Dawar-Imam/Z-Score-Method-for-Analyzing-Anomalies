import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import re
import plotly.express as px
import plotly.io as pio
import plotly.offline as py
import plotly.graph_objs as go


############################################################### Descriptive Statistics

pio.templates.default = "plotly_white"
data = pd.read_csv("Queries.csv")

null_values = data.isnull().sum()
print("Null values in the dataset:")
print(null_values)
print("\nColumn information:")
print(data.info())
print("\nDescriptive statistics:")
print(data.describe())

############################################################### Data Cleaning

data['CTR'] = data['CTR'].str.rstrip('%').astype('float') / 100.0
print("\nUpdated dataset with CTR column converted to float:")
print(data.head(10))

############################################################### Histogram of Words

def clean_and_split(query):
    words = re.findall(r'\w+', query.lower())
    return words

all_words = data['Top queries'].apply(clean_and_split).sum()
word_freq = Counter(all_words)
word_freq_df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)
word_freq_df=word_freq_df.head(20)

fig = go.Figure([go.Bar(x=word_freq_df['Word'], y=word_freq_df['Frequency'])])
fig.update_layout(title='Word Frequencies in Search Queries', xaxis_title='Word', yaxis_title='Frequency')
py.plot(fig)
input("Press Enter to continue...")

############################################################### Clicks and Impressions Frequencies

data_sorted_by_clicks = data.sort_values(by='Clicks', ascending=False)
data_sorted_by_impressions = data.sort_values(by='Impressions', ascending=False)
data_sorted_by_clicks=data_sorted_by_clicks.head(10)
data_sorted_by_impressions=data_sorted_by_impressions.head(10)

fig_clicks = go.Figure([go.Bar(x=data_sorted_by_clicks['Top queries'], y=data_sorted_by_clicks['Clicks'])])
fig_clicks.update_layout(title='Top Queries by Clicks', xaxis_title='Top Queries', yaxis_title='Clicks')
py.plot(fig_clicks)
input("Press Enter to continue...")
fig_impressions = go.Figure([go.Bar(x=data_sorted_by_impressions['Top queries'], y=data_sorted_by_impressions['Impressions'])])
fig_impressions.update_layout(title='Top Queries by Impressions', xaxis_title='Top Queries', yaxis_title='Impressions')
py.plot(fig_impressions)
input("Press Enter to continue...")

############################################################### Highest and Lowest CTRs

data_sorted_by_ctr_desc = data.sort_values(by='CTR', ascending=False)
data_sorted_by_ctr_asc = data.sort_values(by='CTR', ascending=True)
top_ctr_queries = data_sorted_by_ctr_desc.head(10)
bottom_ctr_queries = data_sorted_by_ctr_asc.head(10)

fig_top_ctr = go.Figure([go.Bar(x=top_ctr_queries['Top queries'], y=top_ctr_queries['CTR'])])
fig_top_ctr.update_layout(title='Top Queries with Highest CTRs', xaxis_title='Top Queries', yaxis_title='CTR')
py.plot(fig_top_ctr)
input("Press Enter to continue...")
fig_bottom_ctr = go.Figure([go.Bar(x=bottom_ctr_queries['Top queries'], y=bottom_ctr_queries['CTR'])])
fig_bottom_ctr.update_layout(title='Top Queries with Lowest CTRs', xaxis_title='Top Queries', yaxis_title='CTR')
py.plot(fig_bottom_ctr)
input("Press Enter to continue...")

############################################################### Correlation Metrix

numeric_columns = ['Clicks', 'Impressions', 'CTR', 'Position']
numeric_data = data[numeric_columns]
correlation_matrix = numeric_data.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Clicks, Impressions, CTR, and Position')
plt.savefig('correlation_matrix_heatmap.png')
plt.show()

############################################################### Detecting 

data['Clicks_Zscore'] = (data['Clicks'] - data['Clicks'].mean()) / data['Clicks'].std()
data['Impressions_Zscore'] = (data['Impressions'] - data['Impressions'].mean()) / data['Impressions'].std()
data['CTR_Zscore'] = (data['CTR'] - data['CTR'].mean()) / data['CTR'].std()
data['Position_Zscore'] = (data['Position'] - data['Position'].mean()) / data['Position'].std()
z_score_threshold = 7 # Adjust this threshold as needed
anomalies = data[(abs(data['Clicks_Zscore']) > z_score_threshold) |
                 (abs(data['Impressions_Zscore']) > z_score_threshold) |
                 (abs(data['CTR_Zscore']) > z_score_threshold) |
                 (abs(data['Position_Zscore']) > z_score_threshold)]

print("\n\nAnomalies Detected:")
print(anomalies[['Top queries', 'Clicks', 'Impressions', 'CTR', 'Position']])
print()
