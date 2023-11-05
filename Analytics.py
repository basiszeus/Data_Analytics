import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    layout="wide",
    page_icon=":bar_chart:",
    page_title="Social Media Analytics"
)

st.title("Social Media Analysis")

# Upload the data
with st.sidebar:
    st.subheader("Your Data")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)


with st.expander("Data Preview"):
    st.dataframe(df)

# Description of Data

st.subheader("Data Description")
st.write(df.describe())

# Analytics
st.header("Analytics")

#Impression Data
st.subheader("1. Post type and Impression : What is the max impression per post type")
st.write("#### 1.1 Max Impression")
max_impressions = df.groupby('Post type')['Impressions'].sum().reset_index()
max_impressionsv= max_impressions.sort_values(by='Impressions', ascending=False)
st.write(max_impressionsv)

#Impression Graph
impression_graph = plt.figure(figsize=(15, 5))
sns.barplot(x='Post type', y='Impressions', data=max_impressions, palette="viridis")

for index, value in enumerate(max_impressions['Impressions']):
    plt.text(index, value + 5, str(value), ha='center', va='bottom', fontsize=16)

plt.ylim(0, 1000000)
plt.title('Maximum Impressions per Post Type')
plt.ylabel('Impressions')
plt.xlabel('Post Type')
plt.tight_layout()

# Call the show_graph() function to display the graph
st.pyplot(impression_graph)

st.write("*Note* : To find the real impression per post, it's necessary to explore the number of post per post type and multiply that value with the average")
st.write("#### 1.2 Count of posts per post type")

#Real impression calculation
post_counts = df['Post type'].value_counts()
avg_impressions = df.groupby('Post type')['Impressions'].mean().astype(int)
result = post_counts * avg_impressions
st.write(result)

#Real Impressio graph
resultgraph = plt.figure(figsize=(15, 5))
result.plot(kind='bar', color='skyblue')
for index, value in enumerate(result):
    plt.text(index, value + 0.05 * max(result), str(round(value, 2)), ha='center')
plt.ylim(0, 1000000)
plt.ylabel('Value')
plt.title('Post Count multiplied by Average Impressions per Post Type')
plt.tight_layout()
plt.show()

st.pyplot(resultgraph)

st.write("### 2. Post type and Engagement : What is the max impression per post type")
df['Engagement rate'] = df['Engagement rate'].str.replace('%', '').astype(float) / 100
df['Engagement rate'] = df['Engagement rate'] * 100

st.write("#### 2.1 Average engagement rate per post type")
avg_engagement_rate = df.groupby('Post type')['Engagement rate'].mean().sort_values(ascending=False)
st.write(avg_engagement_rate)
st.write("#### 2.2 Max engagement rate per post type")
max_engagement_rate = df.groupby('Post type')['Engagement rate'].max().sort_values(ascending=False)
st.write(max_engagement_rate)

max_engagement_rate = df.groupby('Post type')['Engagement rate'].max()
avg_engagement_rate = df.groupby('Post type')['Engagement rate'].mean()

Graphavgmax = plt.figure(figsize=(15,5))

max_engagement_sorted = max_engagement_rate.sort_values()
max_engagement_sorted.plot(kind='barh', color='skyblue', label='Max Engagement Rate', alpha=0.7)

avg_engagement_sorted = avg_engagement_rate[max_engagement_sorted.index]
avg_engagement_sorted.plot(kind='barh', color='coral', label='Average Engagement Rate', alpha=0.7)

for index, (max_value, avg_value) in enumerate(zip(max_engagement_sorted, avg_engagement_sorted)):
    plt.text(max_value, index, f'{int(max_value)}', va='center', ha='right', color='black', fontsize=9)
    plt.text(avg_value, index, f'{int(avg_value)}', va='center', ha='left', color='black', fontsize=9)

plt.xlabel('Engagement Rate')
plt.title('Max and Average Engagement Rate per Post Type')
plt.legend()
plt.tight_layout()

st.pyplot(Graphavgmax)

st.write("### 3. Engagement Data")
Engall = df.groupby('Post type')['Engagement rate'].agg(['min', 'mean','max'])
st.write(Engall)

#Branded
st.subheader("3. Branded content analysis")
st.write("#### 3.2 Looking for Impression and Engagement rate for Branded content")
result_yobi = df[df['Content Area'] == 'Product/Yobi Link'].groupby('Post type').agg({'Impressions': 'mean', 'Engagement rate': 'mean'})
st.write(result_yobi.round(0))

#Impression Data
st.subheader("3. Branded content analysis")
st.write("#### 3.2 Looking for Impression and Engagement rate for Branded content")
result_yobi = df[df['Content Area'] == 'Product/Yobi Link'].groupby('Post type').agg({'Impressions': 'mean', 'Engagement rate': 'mean'})
st.write(result_yobi.round(0))

fig, ax = plt.subplots(figsize=(15, 5))

result_yobi.plot(kind='bar', ax=ax)
ax.set_title('Sum of Impressions and Engagement Rate by Post Type')
ax.set_xlabel('Post Type')
ax.set_ylabel('Sum')
ax.legend(["Impressions", "Engagement Rate"])

for bar in ax.patches:  # Use 'ax' here, not 'Branded'
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    ax.annotate(f'{int(y):,}', (x, y), ha='center', va='bottom')

plt.xticks(rotation=45)
plt.tight_layout()

# Display the Matplotlib figure in Streamlit
st.pyplot(fig)
st.write("Your best impression post type:", result_yobi.nlargest(3, 'Impressions')['Impressions'].reset_index().style.format({'Impressions': '{:.0f}'})
)

#Branded
st.subheader("4. Content Area")
st.write("#### 4.1 Best post type per Content area based on impression and Engaement rate")

resultaka = df.groupby('Content Area').agg({'Impressions': ['mean', 'min', 'max'], 'Engagement rate': ['mean', 'min', 'max']}).round(0)
resultaka.columns = ['Impressions Mean', 'Impressions Min', 'Impressions Max', 'Engagement Rate Mean', 'Engagement Rate Min', 'Engagement Rate Max']
resultaka = resultaka.reset_index()

st.write(resultaka)


fig, ax = plt.subplots(figsize=(12, 6))

bar_labels = resultaka['Content Area']
bar_labels = [label[:20] + '...' if len(label) > 20 else label for label in bar_labels]

bar_positions = range(len(bar_labels))

ax.bar(bar_positions, resultaka['Impressions Mean'], width=0.4)

ax.set_title('Impressions Mean by Content Area')
ax.set_xlabel('Content Area')
ax.set_ylabel('Impressions Mean')
ax.set_xticks(bar_positions)
ax.set_xticklabels(bar_labels)

# Adding annotations
for i, v in enumerate(resultaka['Impressions Mean']):
    ax.text(i, v, str(int(v)), ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

# Engagement Mean

ls, ax = plt.subplots(figsize=(12, 6))

bar_labels = resultaka['Content Area']
bar_labels = [label[:20] + '...' if len(label) > 20 else label for label in bar_labels]

bar_positions = range(len(bar_labels))

ax.bar(bar_positions, resultaka['Engagement Rate Mean'], width=0.4)

ax.set_title('Engagement Rate Mean by Content Area')
ax.set_xlabel('Content Area')
ax.set_ylabel('Engagement Rate Mean')
ax.set_xticks(bar_positions)
ax.set_xticklabels(bar_labels)

for i, v in enumerate(resultaka['Engagement Rate Mean']):
    ax.text(i, v, str(int(v)), ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(ls)

st.write("### 4. Correlation")

columns_of_interest = ['Engagement rate', 'Impressions']
correlation_matrix = df[columns_of_interest].corr()

corr= plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5)

plt.title('Correlation Heatmap: Engagement Rate vs Impressions')
st.pyplot(corr)