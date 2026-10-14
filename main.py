import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import Database
from datetime import datetime
import io

# Page Configuration
st.set_page_config(page_title="SpendWise", page_icon="💰", layout="wide")

# ✨ Soft & Glam Custom CSS for Streamlit
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stApp { background-color: #FFFFFF; }
    h1 { color: #0F172A; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; }
    .stButton>button { 
        background-color: #FB7185; color: white; border-radius: 8px; border: none; 
        font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #F43F5E; color: white; }
    .stDataFrame { border-radius: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# Initialize Database
@st.cache_resource
def load_db():
    return Database()

db = load_db()

# Title
st.title("💰 SpendWise: Advanced Expense Tracker")
st.markdown("Manage your monthly budget with a clean, modern interface.")
st.markdown("---")

# Sidebar for Filters
st.sidebar.header("🔍 Filter Expenses")
filter_category = st.sidebar.selectbox("Category", ["All", "Food", "Transport", "Bills", "Entertainment", "Other"])
search_text = st.sidebar.text_input("Search Description")

# Fetch Data
expenses = db.get_filtered_expenses(filter_category, search_text)
df = pd.DataFrame(expenses, columns=["ID", "Date", "Category", "Amount", "Description"])

# --- DASHBOARD METRICS ---
budget_limit = db.get_monthly_budget()
monthly_expenses = db.get_current_month_expenses()
total_spent = sum(exp[3] for exp in monthly_expenses)
remaining = budget_limit - total_spent

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📅 Monthly Budget", f"Rs. {budget_limit:,.2f}")
with col2:
    st.metric("💸 Total Spent", f"Rs. {total_spent:,.2f}", delta=f"Rs. {total_spent - budget_limit:,.2f}" if total_spent > budget_limit else None, delta_color="inverse")
with col3:
    st.metric("✅ Remaining", f"Rs. {remaining:,.2f}", delta_color="normal" if remaining >= 0 else "inverse")

# Progress Bar
if budget_limit > 0:
    percentage = min((total_spent / budget_limit) * 100, 100)
    st.progress(percentage / 100, text=f"{percentage:.1f}% of budget used")
    if percentage >= 100:
        st.warning("⚠️ Budget Exceeded! Please review your spending.")

st.markdown("---")

# --- ADD EXPENSE FORM ---
st.subheader("➕ Add New Expense")
with st.form("expense_form"):
    col_form1, col_form2, col_form3 = st.columns([2, 2, 3])
    with col_form1:
        category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Other"])
    with col_form2:
        amount = st.number_input("Amount (Rs.)", min_value=0.0, step=10.0)
    with col_form3:
        description = st.text_input("Description (Optional)")
    
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        if amount > 0:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.add_expense(date, category, amount, description)
            st.success("Expense added successfully!")
            st.rerun()
        else:
            st.error("Amount must be greater than zero.")

st.markdown("---")

# --- DATA TABLE & CHART ---
tab1, tab2 = st.tabs(["📊 Expense List", "📈 Visual Chart"])

with tab1:
    st.subheader("Recent Expenses")
    if not df.empty:
        # Display table without index
        st.dataframe(df[["Date", "Category", "Amount", "Description"]], use_container_width=True, hide_index=True)
        
        # Delete Option
        st.markdown("##### 🗑️ Delete an Expense")
        delete_id = st.number_input("Enter Expense ID to delete", min_value=1, step=1)
        if st.button("Delete Selected"):
            db.delete_expense(delete_id)
            st.success(f"Expense ID {delete_id} deleted!")
            st.rerun()
    else:
        st.info("No expenses found. Add one above!")

with tab2:
    st.subheader("Spending Breakdown")
    if not df.empty:
        category_totals = df.groupby("Category")["Amount"].sum()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ['#FB7185', '#FBBF24', '#A78BFA', '#60A5FA', '#34D399']
        ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', colors=colors, startangle=140, textprops={'color': '#334155', 'fontweight': 'bold'})
        ax.set_title("Expense Distribution by Category", color='#0F172A', fontsize=14, pad=15)
        st.pyplot(fig)
    else:
        st.info("Add some expenses to see the chart!")

st.markdown("---")

# --- SETTINGS & EXPORT ---
col_set1, col_set2 = st.columns(2)
with col_set1:
    st.subheader("⚙️ Settings")
    new_budget = st.number_input("Set Monthly Budget Limit", min_value=0.0, value=float(budget_limit), step=100.0)
    if st.button("Update Budget"):
        db.set_monthly_budget(new_budget)
        st.success("Budget updated!")
        st.rerun()

with col_set2:
    st.subheader("📥 Export Data")
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Full Report as CSV",
            data=csv,
            file_name='spendwise_report.csv',
            mime='text/csv',
        )
    else:
        st.info("No data to export.")