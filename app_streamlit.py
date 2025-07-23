# app_streamlit.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model_backend import predict_revenue

st.set_page_config(page_title="📊 Smart Sales Dashboard", layout="wide")
st.title("📁 Upload Your Sales CSV to Predict Revenue & View Insights")

uploaded_file = st.file_uploader("Upload CSV (with Date, Product, Units Sold, Revenue, Cost, etc.)", type=["csv"])

# 👇 Future prediction data store
future_data = []

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day

        predicted = []
        for _, row in df.iterrows():
            predicted.append(round(predict_revenue(row['Year'], row['Month'], row['Day'], row['Units Sold']), 2))
        df['Predicted Revenue'] = predicted

        st.success("✅ File processed and predictions completed!")
        st.dataframe(df)

        # 📊 Graphs for Uploaded Data
        st.subheader("📈 Revenue Over Time")
        fig1, ax1 = plt.subplots()
        df.groupby('Date')['Revenue'].sum().plot(ax=ax1)
        ax1.set_title("Total Revenue Over Time")
        st.pyplot(fig1)

        st.subheader("📦 Units Sold by Product")
        fig2, ax2 = plt.subplots()
        df.groupby('Product')['Units Sold'].sum().plot(kind='bar', ax=ax2, color='teal')
        ax2.set_title("Units Sold by Product")
        st.pyplot(fig2)

        st.subheader("🌍 Revenue Distribution by Region")
        fig3, ax3 = plt.subplots()
        df.groupby('Region')['Revenue'].sum().plot.pie(autopct='%1.1f%%', ax=ax3)
        ax3.set_ylabel("")
        ax3.set_title("Revenue by Region")
        st.pyplot(fig3)

        st.subheader("🚚 Transportation Cost by Region")
        fig4, ax4 = plt.subplots()
        df.groupby('Region')['Transportation Cost'].sum().plot(kind='bar', ax=ax4, color='orange')
        ax4.set_title("Transportation Cost by Region")
        st.pyplot(fig4)

        st.subheader("💰 Cost vs Revenue by Product")
        cost_rev = df.groupby('Product')[['Cost', 'Revenue']].sum()
        fig5, ax5 = plt.subplots()
        cost_rev.plot(kind='bar', ax=ax5)
        ax5.set_title("Cost vs Revenue by Product")
        st.pyplot(fig5)

        st.subheader("🧑‍💼 Revenue by Salesperson")
        fig6, ax6 = plt.subplots()
        df.groupby('Salesperson')['Revenue'].sum().plot.pie(autopct='%1.1f%%', ax=ax6)
        ax6.set_ylabel("")
        st.pyplot(fig6)

        st.subheader("📈 Predicted Revenue Over Time")
        fig7, ax7 = plt.subplots()
        df.groupby('Date')['Predicted Revenue'].sum().plot(ax=ax7, color='green')
        ax7.set_title("Predicted Revenue Over Time")
        st.pyplot(fig7)

        # 🔮 Future Prediction Section
        st.subheader("📅 Future Revenue Prediction by Product & Part")

        unique_products = df['Product'].unique().tolist()
        selected_product = st.selectbox("Select Product", unique_products)

        parts_mapping = {
            "Aluminium Can": ["Body", "Top", "Bottom", "Valve"],
            "White Cylinder": ["Cap", "Neck", "Body", "Base"],
            "Orange Cylinder": ["Shell", "Coating", "Label"],
            "Silver Cylinder": ["Ring", "Core", "Seal"]
        }

        product_parts = parts_mapping.get(selected_product, ["General"])
        selected_part = st.selectbox("Select Part of Product", product_parts)

        future_year = st.number_input("Enter Year", value=2025)
        future_month = st.number_input("Enter Month", min_value=1, max_value=12, value=7)
        future_day = st.number_input("Enter Day", min_value=1, max_value=31, value=1)
        future_units = st.number_input("Enter Units Sold", min_value=1, value=500)

        if st.button("Predict Future Revenue"):
            future_pred = predict_revenue(future_year, future_month, future_day, future_units)
            st.success(f"🧠 Predicted Revenue for {selected_product} - {selected_part} on {future_day}-{future_month}-{future_year} is ₹{round(future_pred, 2)}")

            future_df = pd.DataFrame({
                'Date': [f"{future_year}-{future_month:02d}-{future_day:02d}"],
                'Product': [selected_product],
                'Part': [selected_part],
                'Units Sold': [future_units],
                'Predicted Revenue': [round(future_pred, 2)]
            })
            st.session_state['future_df'] = st.session_state.get('future_df', pd.DataFrame())._append(future_df, ignore_index=True)

        # 📊 Future Graphs
        if 'future_df' in st.session_state and not st.session_state['future_df'].empty:
            future_df = st.session_state['future_df']
            future_df['Date'] = pd.to_datetime(future_df['Date'])

            st.subheader("📊 Future Prediction Overview")
            st.dataframe(future_df)

            st.subheader("📅 Future Predicted Revenue Over Time")
            fig8, ax8 = plt.subplots()
            future_df.groupby('Date')['Predicted Revenue'].sum().plot(ax=ax8, marker='o', color='purple')
            ax8.set_ylabel("Predicted Revenue")
            ax8.set_xlabel("Date")
            st.pyplot(fig8)

            st.subheader("📦 Future Units Sold by Product")
            fig9, ax9 = plt.subplots()
            future_df.groupby('Product')['Units Sold'].sum().plot(kind='bar', ax=ax9, color='coral')
            ax9.set_ylabel("Units Sold")
            st.pyplot(fig9)

            st.subheader("💰 Future Predicted Revenue by Product")
            fig10, ax10 = plt.subplots()
            future_df.groupby('Product')['Predicted Revenue'].sum().plot(kind='bar', ax=ax10, color='green')
            ax10.set_title("Future Revenue by Product")
            st.pyplot(fig10)

            st.subheader("🧩 Future Revenue by Part")
            fig11, ax11 = plt.subplots()
            future_df.groupby('Part')['Predicted Revenue'].sum().plot(kind='bar', ax=ax11, color='orange')
            ax11.set_title("Future Revenue by Part")
            st.pyplot(fig11)

        # 📥 Download
        st.download_button("📥 Download Final Data with Prediction", df.to_csv(index=False), "predicted_sales.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error: {e}")
