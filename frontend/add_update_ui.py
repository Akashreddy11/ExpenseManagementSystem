import datetime
import streamlit as st
import requests

API_URL = "http://localhost:8000"


def addUpdate():
    st.subheader("Manage Daily Expenses")

    with st.container(border=True):
        col_date, col_summary = st.columns([1, 2])
        with col_date:
            selected_date = st.date_input(
                "Expense Date",
                value=datetime.date(2024, 8, 1),
                max_value=datetime.date.today()
            )

        expenses = []
        try:
            response = requests.get(f"{API_URL}/expenses/{selected_date}")
            if response.status_code == 200:
                expenses = response.json()
            else:
                st.error("Could not retrieve expenses for the selected date.")
        except requests.exceptions.RequestException:
            st.error("Backend service is unavailable.")

        existing_total = sum(float(item.get("amount", 0)) for item in expenses)
        with col_summary:
            m1, m2 = st.columns(2)
            m1.metric("Logged Entries", len(expenses))
            m2.metric("Recorded Total", f"${existing_total:,.2f}")

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expenses_form", border=True):
        st.markdown("##### Expense Entries")

        header_cols = st.columns([2, 2, 3])
        header_cols[0].caption("**Amount ($)**")
        header_cols[1].caption("**Category**")
        header_cols[2].caption("**Notes**")

        expense_list = []
        max_rows = max(5, len(expenses))

        for i in range(max_rows):
            if i < len(expenses):
                raw_amount = expenses[i].get("amount", 0.0)
                category = expenses[i].get("category", "Other")
                notes = expenses[i].get("notes", "")
            else:
                raw_amount = 0.0
                category = "Food"
                notes = ""

            cat_index = categories.index(category) if category in categories else 0

            c1, c2, c3 = st.columns([2, 2, 3])
            with c1:
                amount_inp = st.number_input(
                    label=f"Amount {i + 1}",
                    min_value=0.0,
                    step=1.0,
                    value=float(raw_amount),
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with c2:
                category_inp = st.selectbox(
                    label=f"Category {i + 1}",
                    options=categories,
                    index=cat_index,
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with c3:
                notes_inp = st.text_input(
                    label=f"Notes {i + 1}",
                    value=notes,
                    placeholder="Optional details...",
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expense_list.append({
                "amount": amount_inp,
                "category": category_inp,
                "notes": notes_inp.strip()
            })

        st.write("")
        submit_button = st.form_submit_button(
            label="Save Changes",
            type="primary",
            use_container_width=True
        )

        if submit_button:
            filtered_expenses = [item for item in expense_list if item["amount"] > 0]
            try:
                save_res = requests.post(
                    f"{API_URL}/expenses/{selected_date}",
                    json=filtered_expenses
                )
                if save_res.status_code == 200:
                    st.success("Expenses updated successfully.")
                    st.rerun()
                else:
                    st.error("Failed to save expenses. Check server logs.")
            except requests.exceptions.RequestException:
                st.error("Connection error while saving.")