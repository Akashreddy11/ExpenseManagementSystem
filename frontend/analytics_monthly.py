import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"

def monthly_analytics_tab():
    st.subheader("Monthly Expense Trends")

    try:
        response = requests.get(f"{API_URL}/analytics/monthly")
        if response.status_code != 200:
            st.error("Failed to load monthly data from server.")
            return
        data = response.json()
    except requests.exceptions.RequestException:
        st.error("Unable to connect to the backend.")
        return

    if not data:
        st.info("No expense data recorded yet.")
        return

    # Prepare DataFrame
    df = pd.DataFrame(list(data.items()), columns=["MonthKey", "Total"])
    df["Total"] = df["Total"].astype(float)

    # Converts '2024-08' to 'August 2024'
    df["Month"] = pd.to_datetime(df["MonthKey"], format="%Y-%m").dt.strftime("%B %Y")

    # Key KPI cards
    total_lifetime = df["Total"].sum()
    avg_monthly = df["Total"].mean()
    highest_month = df.loc[df["Total"].idxmax()]

    m1, m2, m3 = st.columns(3)
    m1.metric("Lifetime Spend", f"${total_lifetime:,.2f}")
    m2.metric("Monthly Average", f"${avg_monthly:,.2f}")
    m3.metric("Peak Month", str(highest_month["Month"]), f"${highest_month['Total']:,.2f}")

    st.write("")

    col_chart, col_table = st.columns([3, 2], gap="medium")

    with col_chart:
        st.markdown("##### Spending by Month")
        st.bar_chart(df.set_index("Month")["Total"], color="#2563EB", use_container_width=True)

    with col_table:
        st.markdown("##### Monthly Totals")
        st.dataframe(
            df.sort_values(by="Month", ascending=False),
            column_config={
                "Month": st.column_config.TextColumn("Month"),
                "Total": st.column_config.NumberColumn("Total Spend", format="$%.2f")
            },
            hide_index=True,
            use_container_width=True
        )