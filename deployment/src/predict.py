# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import numpy as np
import pandas as pd
import re
import ast

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download("stopwords")
nltk.download("punkt_tab")

# =========================
# LOAD MODEL & DATA
# =========================
@st.cache_resource
def load_model():
    return Word2Vec.load("./src/w2v_headset_model.model")

@st.cache_data
def load_data():
    return pd.read_csv("./src/df_final.csv")

w2v_model = load_model()
df = load_data()

stop_words = set(stopwords.words("english"))

# =========================
# PARSE TOKEN (CSV SAFE)
# =========================
def parse_token(token_str):
    try:
        if isinstance(token_str, str):
            return ast.literal_eval(token_str)
    except Exception:
        return []
    return []

df["token"] = df["token"].apply(parse_token)

# =========================
# SENTENCE VECTOR
# =========================
def get_sentence_vector(tokens, model):
    vectors = [model.wv[t] for t in tokens if t in model.wv]
    if not vectors:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)

# Hitung ulang review_vector (WAJIB)
df["review_vector"] = df["token"].apply(
    lambda x: get_sentence_vector(x, w2v_model)
)

# =========================
# TOP 10 BRANDS
# =========================
top_brands = (
    df.groupby("brand")["product"]
      .nunique()
      .sort_values(ascending=False)
      .head(10)
      .index
      .tolist()
)

# =========================
# QUERY PREPROCESSING
# =========================
def preprocess_query(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = word_tokenize(text)
    return [t for t in tokens if t not in stop_words and len(t) > 2]

def vectorize_query(query, model):
    tokens = preprocess_query(query)
    return get_sentence_vector(tokens, model)

# =========================
# RECOMMENDATION LOGIC
# =========================
def recommend_products(query, brand, max_price, top_n=3):
    query_vector = vectorize_query(query, w2v_model)

    df_sim = df.copy()
    df_sim["similarity"] = df_sim["review_vector"].apply(
        lambda x: cosine_similarity([query_vector], [x])[0][0]
    )

    # Filter brand
    df_sim = df_sim[df_sim["brand"].str.lower() == brand.lower()]

    # Filter price
    df_sim = df_sim[df_sim["price"] <= max_price]

    # HARD FILTER: buang smartwatch
    df_sim = df_sim[
        ~df_sim["product"].str.contains("watch|smartwatch", case=False, na=False)
    ]

    top_products = (
        df_sim
        .sort_values("similarity", ascending=False)
        .drop_duplicates("product")
        .head(top_n)
    )

    return top_products, df_sim

def is_corrupted_review(text: str) -> bool:
    if not isinstance(text, str):
        return True

    # 1. Kata super panjang tanpa spasi (camelCase / lowercase / mixed)
    if re.search(r"[A-Za-z]{25,}", text):
        return True

    # 2. Angka langsung nyambung huruf
    if re.search(r"\d+[A-Za-z]{3,}", text):
        return True

    # 3. Rasio spasi terlalu kecil (indikasi kata nempel)
    space_ratio = text.count(" ") / max(len(text), 1)
    if space_ratio < 0.08:
        return True

    return False

def get_top_reviews(product_name, df_sim, n=3):
    reviews = df_sim[
        (df_sim["product"] == product_name) &
        (df_sim["label"] == "Positive")
    ].copy()

    reviews = reviews[~reviews["review_text"].apply(is_corrupted_review)]

    return (
        reviews
        .drop_duplicates("review_text")
        .sort_values("similarity", ascending=False)
        .head(n)
    )

# =========================
# STREAMLIT UI
# =========================
def run_predict():
    st.title("🎧 Headset Recommendation System")
    st.write(
        "Rekomendasi headset berbasis **semantic similarity** "
        "dari review pengguna."
    )

    col1, col2 = st.columns(2)

    with col1:
        selected_brand = st.selectbox(
            "Brand (Top 10)",
            top_brands
        )

    with col2:
        max_price = st.slider(
            "Maximum Price ($)",
            int(df["price"].min()),
            int(df["price"].max()),
            int(df["price"].max())
        )

    query = st.text_input(
        "Keyword",
        placeholder="contoh: gaming headset low latency microphone"
    )

    if st.button("🔍 Search"):
        if not query.strip():
            st.warning("Masukkan keyword terlebih dahulu.")
            return

        top_products, df_sim = recommend_products(
            query=query,
            brand=selected_brand,
            max_price=max_price,
            top_n=3
        )

        if top_products.empty:
            st.warning("Tidak ditemukan produk yang sesuai.")
            return

        st.subheader("🏆 Top 3 Recommended Headsets")

        for idx, row in enumerate(top_products.itertuples(), start=1):
            st.markdown(f"### {idx}. {row.product}")

            col_img, col_info = st.columns([1, 2])

            with col_img:
                if isinstance(row.image_url, str):
                    st.image(row.image_url, width=180)

            with col_info:
                st.markdown(f"**Brand:** {row.brand}")
                st.markdown(f"**Price:** ${row.price}")
                st.markdown(f"**Rating:** {row.rating}")
                st.markdown(f"**Relevance:** {row.similarity:.4f}")

            st.markdown("**Top Reviews:**")

            top_reviews = get_top_reviews(row.product, df_sim)

            for i, r in enumerate(top_reviews.itertuples(), start=1):
                with st.expander(f"🟢 Review {i}"):
                    st.text(r.review_text)

            st.markdown("---")

if __name__ == "__main__":
    run_predict()