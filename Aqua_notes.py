import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Job Summary Generator", layout="centered")
st.title("Job Summary Generator")

# -------------------------
# Session state
# -------------------------
if "selected" not in st.session_state:
    st.session_state.selected = {}
if "summary" not in st.session_state:
    st.session_state.summary = ""

# -------------------------
# Helpers
# -------------------------
def render_group(group, options, per_row=3):
    st.subheader(group)
    current_selection = []
    for i in range(0, len(options), per_row):
        row_opts = options[i:i + per_row]
        cols = st.columns(len(row_opts))
        for col, opt in zip(cols, row_opts):
            key = f"{group}_{opt}"
            selected = col.toggle(opt, key=key)
            if selected:
                current_selection.append(opt)
    st.session_state.selected[group] = current_selection

def render_single_choice(group, options):
    st.subheader(group)
    choice = st.radio("", options, horizontal=True, key=group)
    st.session_state.selected[group] = [choice] if choice else []

def format_list_with_and(items):
    if not items:
        return ""
    if len(items) == 1:
        return f"{items[0]}."
    if len(items) == 2:
        return f"{items[0]} and {items[1]}."
    return f"{', '.join(items[:-1])} and {items[-1]}."

def section_divider():
    return "-----------------------------\n"

# -------------------------
# JOB TIME
# -------------------------
st.header("Job Time")
check_in = st.text_input("Check-in time")
check_out = st.text_input("Check-out time")

# -------------------------
# PAYMENT
# -------------------------
render_group(
    "Payment Information",
    [
        "Visa",
        "Mastercard",
        "Debit",
        "Cash",
        "Pending – please contact the customer",
        "Commercial"
    ],
    per_row=3
)

# -------------------------
# SITE LOGISTICS
# -------------------------
st.header("Site Logistics")
render_single_choice("Parking", ["Easy", "Medium", "Difficult"])
render_single_choice("Setup", ["Easy", "Medium", "Difficult"])

# -------------------------
# TECHNICAL WORK
# -------------------------
st.header("Technical Work")

render_group(
    "Equipment Used",
    ["Portable", "Truck mount", "Cimex"],
    per_row=3
)

render_group(
    "Carpet Fiber Type",
    ["Wool", "Synthetic"],
    per_row=2
)

render_group(
    "Products Applied",
    [
        "Procyon",
        "Citrus",
        "Releasit",
        "Bio Break",
        "Eco Cide",
        "Flex",
        "Groutmaster",
        "Protector",
        "Petzap IQ",
        "Triplephase",
        "Volume 40",
        "Wool Medic",
        "Pure O2",
        "Boost All",
        "Spot Stop"
    ],
    per_row=3
)

# -------------------------
# DESCRIPTION
# -------------------------
st.header("Job Description")
description = st.text_area("Describe the work performed")

# -------------------------
# GENERATE SUMMARY
# -------------------------
if st.button("Generate Summary"):

    summary = ""

    # Job Time
    summary += "JOB TIME\n"
    if check_in:
        summary += f"Check-in: {check_in}\n"
    if check_out:
        summary += f"Check-out: {check_out}\n"
    summary += section_divider()

    # Payment
    payment = st.session_state.selected.get("Payment Information", [])
    if payment:
        summary += "PAYMENT INFORMATION\n"
        summary += f"{format_list_with_and(payment)}\n"
        summary += section_divider()

    # Site Logistics
    parking = st.session_state.selected.get("Parking", [])
    setup = st.session_state.selected.get("Setup", [])
    if parking or setup:
        summary += "SITE LOGISTICS\n"
        if parking:
            summary += f"Parking: {format_list_with_and(parking)}\n"
        if setup:
            summary += f"Setup: {format_list_with_and(setup)}\n"
        summary += section_divider()

    # Equipment
    equipment = st.session_state.selected.get("Equipment Used", [])
    if equipment:
        summary += "EQUIPMENT USED\n"
        summary += f"{format_list_with_and(equipment)}\n"
        summary += section_divider()

    # Fiber Type
    fiber = st.session_state.selected.get("Carpet Fiber Type", [])
    if fiber:
        summary += "CARPET FIBER TYPE\n"
        summary += f"{format_list_with_and(fiber)}\n"
        summary += section_divider()

    # Products
    products = st.session_state.selected.get("Products Applied", [])
    if products:
        summary += "PRODUCTS APPLIED\n"
        summary += f"{format_list_with_and(products)}\n"
        summary += section_divider()

    # Description
    if description.strip():
        clean_description = description.strip()
        clean_description = clean_description[0].upper() + clean_description[1:]
        if not clean_description.endswith("."):
            clean_description += "."
        summary += "JOB DESCRIPTION\n"
        summary += f"{clean_description}\n"
        summary += section_divider()

    st.session_state.summary = summary

# -------------------------
# OUTPUT
# -------------------------
if st.session_state.summary:
    st.markdown("### Final Job Summary")
    st.text_area("Review or copy:", st.session_state.summary, height=260)

    components.html(
        f"""
        <button id="copyBtn"
                style="padding:10px 20px;font-size:16px;background:#4CAF50;color:white;
                       border:none;border-radius:5px;cursor:pointer;">
            Copy Summary
        </button>
        <script>
        const btn = document.getElementById("copyBtn");
        btn.addEventListener("click", () => {{
            navigator.clipboard.writeText(`{st.session_state.summary}`);
            btn.innerText = "Copied";
            setTimeout(() => {{
                btn.innerText = "Copy Summary";
            }}, 2000);
        }});
        </script>
        """,
        height=70
    )
