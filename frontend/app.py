

import streamlit as st
from add_update_ui import addUpdate
from analytics_ui import analytics_tab
from analytics_monthly import monthly_analytics_tab
st.title("Expense Management System")

tab1 ,tab2 ,tab3 = st.tabs(["Add / Update","Analytics-by-category","Analytics-by-months"])

with tab1:
    addUpdate()

with tab2:
    analytics_tab()
with tab3:
    monthly_analytics_tab()

