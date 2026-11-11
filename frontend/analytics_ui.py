import datetime
import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"


def analytics_tab():
    if "analytics_data" not in st.session_state:
        st.session_state.analytics_data = None

    st.subheader("Spending Analytics & Insights")

    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", datetime.date.today())
        with col3:
            fetch_btn = st.button("Analyze", type="primary", use_container_width=True)

    if fetch_btn:
        try:
            payload = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            }
            res = requests.post(f"{API_URL}/analytics", json=payload)
            if res.status_code == 200:
                st.session_state.analytics_data = {
                    "raw": res.json(),
                    "range": (start_date, end_date)
                }
            else:
                st.error("Failed to load analytics data from server.")
        except requests.exceptions.RequestException:
            st.error("Unable to connect to the backend service.")

    if st.session_state.analytics_data:
        response = st.session_state.analytics_data["raw"]
        s_date, e_date = st.session_state.analytics_data["range"]

        if not response:
            st.info("No expense records found for the selected time window.")
            return

        data = {
            "Category": list(response.keys()),
            "Total": [float(response[cat]["total"]) for cat in response],
            "Percentage": [float(response[cat]["percentage"]) for cat in response]
        }

        df = pd.DataFrame(data).sort_values(by="Total", ascending=False).reset_index(drop=True)
        total_spend = df["Total"].sum()
        top_row = df.iloc[0]
        top_category = top_row["Category"]
        top_pct = top_row["Percentage"]
        top_amt = top_row["Total"]

        st.write("")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Spent", f"${total_spend:,.2f}")
        m2.metric("Top Category", top_category)
        m3.metric("Top Outflow", f"${top_amt:,.2f}", f"{top_pct:.1f}%")
        m4.metric("Categories", len(df))

        st.write("")
        chart_col, table_col = st.columns([3, 2], gap="medium")

        with chart_col:
            st.markdown("##### Distribution by Category")
            chart_df = df.set_index("Category")[["Total"]]
            st.bar_chart(chart_df, color="#4F46E5", use_container_width=True)

        with table_col:
            st.markdown("##### Breakdown Details")
            st.dataframe(
                df,
                column_config={
                    "Category": st.column_config.TextColumn("Category"),
                    "Total": st.column_config.NumberColumn("Total", format="$%.2f"),
                    "Percentage": st.column_config.ProgressColumn(
                        "Share",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
                },
                hide_index=True,
                use_container_width=True
            )

        st.divider()

        with st.container(border=True):
            st.markdown("#### Smart Budget Diagnosis")

            if top_pct >= 50:
                st.warning(
                    f"**Heavy Outflow Alert**: **{top_category}** consumes **{top_pct:.1f}%** (${top_amt:,.2f}) "
                    f"of your total budget. Trimming this category by just 10% would retain approximately "
                    f"**${top_amt * 0.10:,.2f}**."
                )
            elif top_pct >= 30:
                st.info(
                    f"**Moderate Concentration**: **{top_category}** is your primary cost driver at "
                    f"**{top_pct:.1f}%** (${top_amt:,.2f}), while the remaining expenses are spread across "
                    f"{len(df) - 1} other categories."
                )
            else:
                st.success(
                    f"**Balanced Outflow**: Your highest spending area (**{top_category}**) stays under "
                    f"**{top_pct:.1f}%** (${top_amt:,.2f}). Outflows remain evenly divided across active categories."
                )

            with st.expander("Ask Financial Assistant"):
                user_query = st.text_input(
                    "Prompt",
                    placeholder="e.g., Where should I prioritize reducing costs this month?",
                    label_visibility="collapsed"
                )

                if user_query:
                    st.markdown(f"**Analysis on:** *{user_query}*")
                    if "save" in user_query.lower() or "cut" in user_query.lower() or "reduce" in user_query.lower():
                        st.write(
                            f"Focus primarily on **{top_category}**, which accounts for **${top_amt:,.2f}** "
                            f"({top_pct:.1f}% of outflows). Setting a soft spending ceiling at "
                            f"**${top_amt * 0.85:,.2f}** for the upcoming period would secure roughly "
                            f"**${top_amt * 0.15:,.2f}** in immediate surplus."
                        )
                    else:
                        st.write(
                            f"Across the recorded interval ({s_date} to {e_date}), you logged {len(df)} distinct "
                            f"spending channels totaling **${total_spend:,.2f}**. Keep an eye on secondary outflows "
                            f"to avoid cost creep outside of {top_category}."
                        )