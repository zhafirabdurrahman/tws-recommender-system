import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SoundScout",
    layout="wide"
)

from eda import run_eda
from predict import run_predict

menu = ["Home Page", "EDA", "Predict Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home Page":

    with open("./src/img.png", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    html = f"""
    <div style="
        background: radial-gradient(circle at top, #0f172a, #020617);
        padding: 70px 50px;
        border-radius: 28px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        max-width: 900px;
        margin: 60px auto;
        text-align: center;
        color: white;
        font-family: Inter, system-ui, -apple-system, sans-serif;
    ">

        <img src="data:image/png;base64,{img_base64}"
             style="width:150px; margin-bottom:30px;" />

        <h1 style="
            font-size:72px;
            font-weight:800;
            margin-bottom:18px;
            letter-spacing:-1px;
        ">
            SoundScout
        </h1>

        <p style="
            font-size:26px;
            color:#94a3b8;
            margin-bottom:36px;
        ">
            Semantic Audio Product Recommendation Engine
        </p>

        <p style="
            font-size:18px;
            line-height:1.8;
            color:#e5e7eb;
            max-width:700px;
            margin: 0 auto 40px;
        ">
            Stop guessing which audio gear is worth your money.<br/>
            SoundScout analyzes real user reviews using <b>semantic similarity</b>
            to surface products that actually match what you care about.
        </p>

        <p style="
            font-size:14px;
            letter-spacing:2px;
            color:#f87171;
        ">
            USE THE MENU TO START EXPLORING
        </p>

    </div>
    """

    components.html(html, height=720)

elif choice == "EDA":
    run_eda()

elif choice == "Predict Data":
    run_predict()