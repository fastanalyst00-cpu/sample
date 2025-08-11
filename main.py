import streamlit as st

# ✅ FIRST command on the main page
st.set_page_config(page_title="Sales Analyst", layout="wide", initial_sidebar_state="collapsed")

# Navigation setup
pages = {
    "Rates": [
        st.Page("pages/formula_tester_app.py", title="Test Formula"),
        st.Page("pages/conn.py", title="Sample"),
    ]
}

pg = st.navigation(pages)
pg.run()
