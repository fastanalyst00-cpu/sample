import streamlit as st
import re
import pandas as pd

# Allowed variables and descriptions
columns_info = [
    {"Name": "[ACTUAL_WEIGHT]", "Description": "Gross weight"},
    {"Name": "[CBM]", "Description": "CBM"},
    {"Name": "[DECLARED_VALUE]", "Description": "Declared value"},
    {"Name": "[AMOUNT]", "Description": "Amount in the charge details"},
    {"Name": "[SKU_QTY]", "Description": "Total quantity"},
    {"Name": "[ODA_FEE]", "Description": "ODA fee"},
    {"Name": "[TOTAL_AMT]", "Description": "Total computed amount"},
    {"Name": "[CHARGEABLE_WEIGHT]", "Description": "Weight in kilograms"},
]

# Extract plain variable names (without brackets) for validation
variables = [col["Name"].strip("[]") for col in columns_info]

# Session state defaults
if "formula" not in st.session_state:
    st.session_state.formula = ""
if "selected_vars" not in st.session_state:
    st.session_state.selected_vars = []
if "formula_checked" not in st.session_state:
    st.session_state.formula_checked = False
if "var_inputs" not in st.session_state:
    st.session_state.var_inputs = {}

st.title("Formula Builder")

# Display available variables table
with st.expander("Columns"):
    df = pd.DataFrame(columns_info)
    st.table(df)

# Formula bar
st.subheader("Formula")
new_formula = st.text_input(
    "Enter formula here (use variables in square brackets):", 
    st.session_state.formula
)

# If formula changes, reset check status
if new_formula != st.session_state.formula:
    st.session_state.formula = new_formula
    st.session_state.formula_checked = False
    st.session_state.selected_vars = []

# Check Formula button
if not st.session_state.formula_checked:
    if st.button("✅ Check Formula"):
        formula = st.session_state.formula.strip()

        if not formula:
            st.error("❌ Formula is empty.")
        else:
            # Extract variables
            raw_vars = re.findall(r"[A-Z_]+", formula)
            bracket_vars = re.findall(r"\[([A-Z_]+)\]", formula)

            # Detect unbracketed variables
            unbracketed_vars = [
                v for v in raw_vars if v in variables and v not in bracket_vars
            ]

            if unbracketed_vars:
                st.error(f"❌ Variables must be inside square brackets: {', '.join(unbracketed_vars)}")
            else:
                invalid_vars = [v for v in bracket_vars if v not in variables]
                if invalid_vars:
                    st.error(f"❌ Unknown variables: {', '.join(invalid_vars)}")
                else:
                    st.session_state.selected_vars = list(set(bracket_vars))
                    st.session_state.formula_checked = True
                    st.rerun()

# Function to convert Excel-style IF to Python
def convert_excel_if_to_python(expr):
    # Regex to capture IF(condition, value_if_true, value_if_false)
    pattern = r"IF\s*\(([^,]+),\s*([^,]+),\s*(.+)\)"
    while re.search(pattern, expr, flags=re.IGNORECASE):
        expr = re.sub(pattern, r"(\2 if (\1) else \3)", expr, flags=re.IGNORECASE)
    return expr

# Show variable inputs after check
if st.session_state.formula_checked:
    st.subheader("Variable Inputs")
    for var in st.session_state.selected_vars:
        st.session_state.var_inputs[var] = st.number_input(
            f"Enter value for {var}:", value=0.0
        )

    # Evaluate button
    if st.button("▶ Evaluate Formula"):
        evaluated_formula = st.session_state.formula
        for var, val in st.session_state.var_inputs.items():
            evaluated_formula = evaluated_formula.replace(f"[{var}]", str(val))

        # Convert Excel IF to Python ternary
        evaluated_formula = convert_excel_if_to_python(evaluated_formula)

        try:
            result = eval(evaluated_formula)
            st.success(f"✅ Result: {result}")
        except Exception as e:
            st.error(f"❌ Error evaluating formula: {e}")
