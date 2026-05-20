import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Hacker News",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("hacker_news_clean.csv")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Filter Data")

type_filter = st.sidebar.multiselect(
    "Pilih Jenis Postingan",
    options=df['type'].unique(),
    default=df['type'].unique()
)

min_score = st.sidebar.slider(
    "Minimum Score",
    int(df['score'].min()),
    int(df['score'].max()),
    1
)

# FILTER DATA
df = df[
    (df['type'].isin(type_filter)) &
    (df['score'] >= min_score)
]

# =========================
# HEADER
# =========================
st.title("📊 Dashboard Analisis Hacker News")

st.markdown("""
Dashboard ini menampilkan hasil analisis data Hacker News menggunakan Google BigQuery dan Streamlit.
""")

# =========================
# KPI CARD
# =========================
st.subheader("Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Data", len(df))
col2.metric("Rata-rata Score", round(df['score'].mean(), 2))
col3.metric("Jumlah Penulis", df['by'].nunique())
col4.metric("Jenis Postingan", df['type'].nunique())

# =========================
# DATASET
# =========================
st.subheader("Preview Dataset")

st.dataframe(df.head())

# =========================
# STATISTIK DESKRIPTIF
# =========================
st.subheader("Statistik Deskriptif")

st.dataframe(df[['score', 'title_length']].describe())

# =========================
# VISUALISASI
# =========================

# Histogram dan Countplot
col5, col6 = st.columns(2)

with col5:
    st.subheader("Distribusi Score")

    fig1, ax1 = plt.subplots(figsize=(6,4))
    sns.histplot(df['score'], bins=30, ax=ax1)

    st.pyplot(fig1)

    st.info("""
    Mayoritas postingan memiliki score rendah dan hanya sedikit postingan dengan score tinggi.
    """)

with col6:
    st.subheader("Distribusi Jenis Postingan")

    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.countplot(x='type', data=df, ax=ax2)

    st.pyplot(fig2)

    st.info("""
    Jenis postingan story mendominasi dataset Hacker News.
    """)

# Scatterplot dan Boxplot
col7, col8 = st.columns(2)

with col7:
    st.subheader("Hubungan Panjang Judul dan Score")

    fig3, ax3 = plt.subplots(figsize=(6,4))
    sns.scatterplot(
        x='title_length',
        y='score',
        data=df,
        ax=ax3
    )

    st.pyplot(fig3)

    st.info("""
    Panjang judul tidak menunjukkan hubungan yang signifikan terhadap score postingan.
    """)

with col8:
    st.subheader("Score Berdasarkan Jenis Postingan")

    fig4, ax4 = plt.subplots(figsize=(6,4))
    sns.boxplot(
        x='type',
        y='score',
        data=df,
        ax=ax4
    )

    st.pyplot(fig4)

    st.info("""
    Postingan bertipe story cenderung memiliki score lebih tinggi dibandingkan tipe lainnya.
    """)

# =========================
# TOP AUTHOR
# =========================
st.subheader("Top 10 Penulis Paling Aktif")

top_authors = df['by'].value_counts().head(10)

fig5, ax5 = plt.subplots(figsize=(10,5))
top_authors.plot(kind='bar', ax=ax5)

plt.xticks(rotation=45)

st.pyplot(fig5)

# =========================
# KESIMPULAN
# =========================
st.subheader("Kesimpulan")

st.success("""
Berdasarkan hasil analisis, mayoritas postingan Hacker News memiliki score rendah dan didominasi oleh postingan bertipe story. Selain itu, panjang judul tidak memiliki hubungan signifikan terhadap popularitas postingan. Aktivitas pengguna juga tidak merata karena hanya beberapa penulis yang aktif membuat postingan.
""")