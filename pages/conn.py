import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandasql as psql

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

if st.button("Update worksheet"):
        df = conn.update(
            worksheet="masterlist",
            data=df,
        )
        st.cache_data.clear()
        st.rerun()

    # Display our Spreadsheet as st.dataframe
st.dataframe(df)
