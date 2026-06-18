import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #eef3ea;
}

/* BOLD EVERYTHING */
* {
    font-weight: 800 !important;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 38px;
    color: #1b4332;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #2d6a4f;
}

/* KPI */
.kpi {
    background: #d8f3dc;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: #1b4332;
}

/* GAP */
.kpi-gap {
    margin-bottom: 25px;
}

/* CARD */
.card {
    background: #d8f3dc;
    padding: 20px;
    border-radius: 18px;
    color: #1b4332;
}

/* LABELS */
label {
    color: #1b4332 !important;
}

/* ---------------------------
   🔥 DROPDOWN FIX
--------------------------- */

/* Selected value */
.stSelectbox div[data-baseweb="select"] > div {
    color: white !important;
}

/* Dropdown options */
div[role="listbox"] {
    color: white !important;
    background-color: #2d6a4f !important;
}

/* ---------------------------
   🔥 NUMBER INPUT FIX
--------------------------- */

input[type="number"] {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

div[data-testid="stNumberInput"] input {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

input::placeholder {
    color: white !important;
}

div[data-testid="stNumberInput"] {
    background-color: #2d6a4f !important;
    border-radius: 10px;
    padding: 5px;
}

/* ---------------------------
   🔥 UPLOAD FIX
--------------------------- */

section[data-testid="stFileUploader"] label {
    color: #1b4332 !important;
}

section[data-testid="stFileUploader"] button {
    color: #1b4332 !important;
}

/* 200MB text */
section[data-testid="stFileUploader"] small,
section[data-testid="stFileUploader"] span,
section[data-testid="stFileUploader"] p {
    color: white !important;
}

/* BUTTON */
.stButton>button {
    background: #2d6a4f;
    color: white;
    border-radius: 10px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<div class='title'>🌿 NGO Operations Analytical Report 🌿</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>✨ Discover insights. Drive impact. ✨</div>", unsafe_allow_html=True)

# UPLOAD
file = st.file_uploader("📂 Upload Dataset")

if file:

    df = pd.read_csv(file)

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='kpi'>📊 Total Events<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'>📈 Avg Impact<br><h2>{round(df['Impact_Score'].mean(),2)}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'>💰 Total Cost<br><h2>{int(df['Cost'].sum())}</h2></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi'>👥 Volunteers<br><h2>{int(df['Volunteers'].sum())}</h2></div>", unsafe_allow_html=True)

    st.markdown("<div class='kpi-gap'></div>", unsafe_allow_html=True)

    left, right = st.columns([2,1])

    with left:
        st.markdown("<div class='card'>📊 Impact Trend 🌿</div>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(8,3))
        grp = df.groupby("Event_Type")["Impact_Score"].mean()
        ax.plot(grp.index, grp.values, marker='o', color="#1b4332")
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig)

    with right:
        st.markdown("<div class='card'>📉 Distribution 🌿</div>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(4,3))
        ax.hist(df["Impact_Score"], bins=5, color="#2d6a4f")
        st.pyplot(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='card'>💸 Cost vs Impact</div>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(4,3))
        ax.scatter(df["Cost"], df["Impact_Score"], color="#1b4332")
        ax.tick_params(axis='both', labelsize=8)
        st.pyplot(fig)

    with col2:
        st.markdown("<div class='card'>📍 Region Analysis</div>", unsafe_allow_html=True)

        pivot = df.pivot_table(
            values="Impact_Score",
            index="Location",
            columns="Event_Type",
            aggfunc="mean"
        )
        st.dataframe(pivot.style.background_gradient(cmap="Greens"))

    with col3:
        st.markdown("<div class='card'>🚀 Prediction Tool</div>", unsafe_allow_html=True)

        event = st.selectbox("Event Type", df["Event_Type"].unique())
        location = st.selectbox("Location", df["Location"].unique())
        cost = st.number_input("Cost")
        volunteers = st.number_input("Volunteers")
        resources = st.number_input("Resources")

        if st.button("✨ Predict Impact"):
            score = (volunteers * 1.2) + (resources * 0.8) - (cost / 2000)

            if score > 80:
                st.success(f"🌟 {round(score,2)} High Impact")
            elif score > 60:
                st.info(f"👍 {round(score,2)} Moderate")
            else:
                st.error(f"⚠ {round(score,2)} Low")

else:
    st.markdown(
        "<h3 style='text-align:center; color:#1b4332;'>🌿 Upload dataset to begin ✨</h3>",
        unsafe_allow_html=True
    )