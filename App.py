import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load initial training program
program_df = pd.read_excel("برنامه بدنسازی.xlsx")

# Load or initialize weight tracking data
try:
    progress_df = pd.read_csv("data.csv")
except FileNotFoundError:
    progress_df = pd.DataFrame(columns=["تاریخ", "نام حرکت", "مقدار وزنه"])

st.title("🏋️‍♀️ برنامه تمرینی و نمودار پیشرفت بدنسازی")

st.header("📋 برنامه تمرینی امروز")
st.dataframe(program_df[["نام حرکت", "ست"]])

st.markdown("---")
st.subheader("📝 ثبت مقدار وزنه")

today = datetime.today().strftime('%Y-%m-%d')
with st.form("log_form"):
    selected_exercise = st.selectbox("انتخاب حرکت", program_df["نام حرکت"])
    weight = st.number_input("مقدار وزنه (کیلوگرم)", min_value=0.0, step=0.5)
    date_input = st.date_input("تاریخ", datetime.today())
    submitted = st.form_submit_button("ثبت")

    if submitted:
        new_row = {"تاریخ": date_input, "نام حرکت": selected_exercise, "مقدار وزنه": weight}
        progress_df = pd.concat([progress_df, pd.DataFrame([new_row])], ignore_index=True)
        progress_df.to_csv("data.csv", index=False)
        st.success("✅ مقدار وزنه ثبت شد!")

st.markdown("---")
st.subheader("📈 نمودار پیشرفت حرکت")

selected_for_chart = st.selectbox("انتخاب حرکت برای مشاهده پیشرفت", progress_df["نام حرکت"].unique())

if selected_for_chart:
    chart_data = progress_df[progress_df["نام حرکت"] == selected_for_chart]
    chart_data = chart_data.sort_values("تاریخ")

    fig, ax = plt.subplots()
    ax.plot(chart_data["تاریخ"], chart_data["مقدار وزنه"], marker='o', color='blue')
    ax.set_title(f"نمودار پیشرفت - {selected_for_chart}")
    ax.set_xlabel("تاریخ")
    ax.set_ylabel("مقدار وزنه (kg)")
    ax.grid(True)
    st.pyplot(fig)