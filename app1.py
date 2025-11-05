import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.title("COvid-19 EDA")
st.write("Simple exploratory data analysis of COVID-19 research.")
 

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\USER\Desktop\PERIS DOCUMENTS⁮\New folder (2)\coviddata_clean.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    return df

df = load_data()


# ---- App Title and Description ----

st.markdown("""
This interactive dashboard lets you explore COVID-19 research publications.
You can view publication trends over time, analyze top journals, and preview the dataset.
""")


# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filter Data")
year_list = sorted(df['publish_time'].dropna().dt.year.unique())
selected_year = st.sidebar.selectbox("Select Year", options=year_list)
min_count = st.sidebar.slider("Minimum number of publications", 10, 500, 100)


#---- Filter Data ----
filtered_df = df[df['publish_time'].dt.year == selected_year]



# Publications over time
st.subheader("Publications Over Time")
year_counts = filtered_df['publish_time'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.barh(year_counts.index, year_counts.values, color='skyblue')
st.pyplot(fig)

#Top journals
st.subheader("Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots()
ax.barh(top_journals.index, top_journals.values, color='lightgreen')
st.pyplot(fig)


# Count the number of papers per source
source_counts = df['source_x'].value_counts()

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(source_counts.index, source_counts.values, color='teal')

# Add titles and labels
ax.set_title('Distribution of Paper Counts by Source', fontsize=14)
ax.set_xlabel('Source', fontsize=12)
ax.set_ylabel('Number of Papers', fontsize=12)
ax.set_xticks(rotation=45, ha='right')

# Add exact counts on each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # x position (center of bar)
        yval + 5,                           # y position (slightly above bar)
        int(yval),                          # label text (integer count)
        ha='center', va='bottom', fontsize=10
    )

# Adjust layout
plt.tight_layout()
st.pyplot(fig)

# Word cloud
st.subheader("Word Cloud of Titles")
titles = ' '.join(filtered_df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)


# ---- Data Sample ----
st.subheader("🧾 Sample of Dataset")
st.dataframe(df.sample(10))




