import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="🏆 Personal Performance Tracker", layout="wide")

# --- Logo ---
st.image("https://upload.wikimedia.org/wikipedia/commons/8/8c/Goal_icon.svg", width=100)

st.title("🏆 Personal Performance Tracker")
st.write("Ein interaktives Dashboard zur Verfolgung persönlicher Ziele, Aufgaben und Fortschritte – erstellt von **Vitalii Shevchuk**.")

# --- Load data ---
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("🔎 Filteroptionen")
selected_category = st.sidebar.multiselect("Kategorie auswählen:", df["Kategorie"].unique())
selected_month = st.sidebar.selectbox("Monat auswählen:", sorted(df["Monat"].unique()), index=None, placeholder="Bitte auswählen...")

filtered_df = df.copy()
if selected_category:
    filtered_df = filtered_df[df["Kategorie"].isin(selected_category)]
if selected_month:
    filtered_df = filtered_df[filtered_df["Monat"] == selected_month]

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Gesamtaufgaben", len(filtered_df))
col2.metric("Erledigte Aufgaben", len(filtered_df[filtered_df["Status"] == "Erledigt"]))
if len(filtered_df) > 0:
    col3.metric("Erfolgsquote", f"{round(len(filtered_df[filtered_df['Status']=='Erledigt'])/len(filtered_df)*100,1)}%")
else:
    col3.metric("Erfolgsquote", "0%")

# --- Charts ---
if not filtered_df.empty:
    fig1 = px.bar(filtered_df, x="Kategorie", color="Status", title="📊 Aufgaben nach Kategorie")
    fig2 = px.line(filtered_df, x="Monat", y="Punkte", markers=True, title="📈 Fortschritt über Monate")
    col4, col5 = st.columns(2)
    col4.plotly_chart(fig1, use_container_width=True)
    col5.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Bitte Filter auswählen, um Ergebnisse anzuzeigen.")

# --- Table view ---
st.subheader("📋 Aufgabenliste")
st.dataframe(filtered_df)
