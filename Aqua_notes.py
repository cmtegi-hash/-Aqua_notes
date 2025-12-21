import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Job Summary Generator", layout="centered")
st.title("Job Summary Generator (Mobile Friendly)")

if "selected" not in st.session_state:
    st.session_state.selected = {}
if "summary" not in st.session_state:
    st.session_state.summary = ""

def render_group(group, options, per_row=3):
    st.subheader(group)
    current_selection = []
    for i in range(0, len(options), per_row):
        row_opts = options[i:i+per_row]
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

check_in = st.text_input("Check in:")
check_out = st.text_input("Check out:")

# Payment
render_group("Payment", [
    "Visa",
    "Mastercard",
    "Debit",
    "Cash",
    "Pending, please call the customer",
    "Commercial"
], per_row=3)

render_group("Equipment", ["Portable", "Truck mount", "Cimex"], per_row=3)

# Parking y Setup (selección única)
render_single_choice("Parking", ["Easy", "Medium", "Difficult"])
render_single_choice("Setup", ["Easy", "Medium", "Difficult"])

# Product used
render_group("Product used", [
    "Procyon",
    "Citrus",
    "Releasit",
    "Bio Break",
    "Eco cide",
    "Flex",
    "Groutmaster",
    "Protector",
    "Petzap IQ",
    "Triplephase",
    "Volume 40",
    "Wool Medic"
], per_row=3)

description = st.text_area("Description of the job:")

if st.button("Generate Summary"):
    summary = f"Check in: {check_in}.\nCheck out: {check_out}.\n"

    if st.session_state.selected.get("Payment"):
        summary += f"Payment: {format_list_with_and(st.session_state.selected['Payment'])}\n"
        summary += "-----------------------------\n"

    for group in ["Equipment", "Parking", "Setup"]:
        options = st.session_state.selected.get(group, [])
        if options:
            summary += f"{group}: {format_list_with_and(options)}\n"

    if st.session_state.selected.get("Product used"):
        summary += f"Product used: {format_list_with_and(st.session_state.selected['Product used'])}\n"
        summary += "-----------------------------\n"

    if description:
        clean_description = description.lstrip()
        if clean_description:
            clean_description = clean_description[0].upper() + clean_description[1:]
            if not clean_description.endswith("."):
                clean_description += "."

        summary += "Description of the job:\n"
        summary += f"{clean_description}\n"
        summary += "-----------------------------\n"

    st.session_state.summary = summary

if st.session_state.summary:
    st.markdown("### 📋 Final Summary")
    st.text_area("You can copy or review:", st.session_state.summary, height=220)
    components.html(f"""
        <button id="copyBtn" 
                style="padding:10px 20px;font-size:16px;background:#4CAF50;color:white;
                       border:none;border-radius:5px;cursor:pointer;">
            📎 Copy Summary
        </button>
        <script>
        const btn = document.getElementById("copyBtn");
        btn.addEventListener("click", () => {{
            navigator.clipboard.writeText(`{st.session_state.summary}`);
            btn.style.background = "#2E7D32";
            btn.innerText = "✅ Copied!";
            setTimeout(() => {{
                btn.style.background = "#4CAF50";
                btn.innerText = "📎 Copy Summary";
            }}, 2000);
        }});
        </script>
    """, height=70)
