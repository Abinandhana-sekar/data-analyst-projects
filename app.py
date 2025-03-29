import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Customer Acquisition Cost (CAC) Analysis")

uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Dataset Preview")
    st.write(df.head())

    st.subheader("📈 Data Summary")
    st.write(df.describe())

    if "Marketing_Spend" in df.columns and "New_Customers" in df.columns:
        df["cac"] = df["Marketing_Spend"] / df["New_Customers"]
        st.subheader("💰 CAC Calculation")
        st.write(df[["Marketing_Spend", "New_Customers", "cac"]].head())

        st.subheader("📊 Data Distributions")
        for col in ["Marketing_Spend", "New_Customers", "cac"]:
            fig, ax = plt.subplots()
            sns.histplot(df[col], bins=30, kde=True, ax=ax)
            st.pyplot(fig)

        if "Marketing_Channel" in df.columns:
            channel_comparison = df.groupby("Marketing_Channel").agg(
                total_customers=("New_Customers", "sum"),
                avg_cac=("cac", "mean")
            ).reset_index()

            st.subheader("📢 Marketing Channel Analysis")
            st.write(channel_comparison)

            for y_val, title in [("total_customers", "Customers Acquired"), ("avg_cac", "Average CAC")]:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.barplot(x="Marketing_Channel", y=y_val, data=channel_comparison, ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
    else:
        st.error("Dataset must contain 'Marketing_Spend' and 'New_Customers' columns.")
else:
    st.warning("⚠️ Please upload a CSV file.")
