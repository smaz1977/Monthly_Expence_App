import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import time
import base64

# --- MUST BE FIRST COMMAND ---
st.set_page_config(page_title="Sandip's Income & Monthly expences", page_icon="💸", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["ID", "Date", "Amount", "Category", "Notes"])
if 'expense_id_counter' not in st.session_state:
    st.session_state.expense_id_counter = 1
if 'incomes' not in st.session_state:
    st.session_state.incomes = pd.DataFrame(columns=["ID", "Date", "Amount", "Source", "Notes"])
if 'income_id_counter' not in st.session_state:
    st.session_state.income_id_counter = 1
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
    <style>
    /* Light mode optimized styles */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #111827 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* General text */
    p, span, label, div {
        color: #1f2937;
    }
    
    /* Metrics box */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #2563eb;
        font-weight: bold;
    }
    
    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 210, 255, 0.4);
        color: white;
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Success/Info Alerts */
    .stAlert {
        border-radius: 8px;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CATEGORIES ---
CATEGORIES = ["Food & Dining", "Transportation", "Housing", "Utilities", "Shopping", "Entertainment", "Health", "Education", "Other"]

# --- AUTHENTICATION ---
def login_page():
    st.title("🔐 Welcome to Sandip's Income & Monthly expences")
    st.markdown("### Please login to continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("**(Demo Mode: Any username/password works)**")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if username and password:
                    with st.spinner("Authenticating..."):
                        time.sleep(0.5) # Simulate delay
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Please enter both username and password.")

# --- MAIN APP ---
def main_app():
    # --- SIDEBAR NAV ---
    with st.sidebar:
        st.title("💸 Menu")
        page = st.radio("Navigation", ["Dashboard", "Add Income", "Add Expense", "View Expenses", "Reports & Export"])
        
        st.markdown("---")
        
        # Calculate sidebar stats
        total_in = st.session_state.incomes['Amount'].sum() if not st.session_state.incomes.empty else 0.0
        total_ex = st.session_state.expenses['Amount'].sum() if not st.session_state.expenses.empty else 0.0
        
        st.markdown(f"**Total Entries:** {len(st.session_state.expenses) + len(st.session_state.incomes)}")
        st.markdown(f"**Current Balance:** ${(total_in - total_ex):,.2f}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # --- ADD INCOME PAGE ---
    if page == "Add Income":
        st.header("💰 Add New Income")
        
        with st.form("add_income_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Date", datetime.date.today())
                amount = st.number_input("Amount ($)", min_value=0.01, step=1.0, format="%.2f")
            
            with col2:
                source = st.selectbox("Source", ["Salary", "Business", "Investments", "Gifts", "Other"])
                notes = st.text_area("Notes", height=110)
                
            submitted = st.form_submit_button("Add Income", use_container_width=True)
            
            if submitted:
                new_income = pd.DataFrame([{
                    "ID": st.session_state.income_id_counter,
                    "Date": date,
                    "Amount": amount,
                    "Source": source,
                    "Notes": notes
                }])
                
                if st.session_state.incomes.empty:
                    st.session_state.incomes = new_income
                else:
                    st.session_state.incomes = pd.concat([st.session_state.incomes, new_income], ignore_index=True)
                st.session_state.income_id_counter += 1
                
                st.success(f"Income of ${amount:.2f} from '{source}' added successfully!")
                time.sleep(1)
                st.rerun()

    # --- ADD EXPENSE PAGE ---
    elif page == "Add Expense":
        st.header("📝 Add New Expense")
        
        with st.form("add_expense_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Date", datetime.date.today())
                amount = st.number_input("Amount ($)", min_value=0.01, step=1.0, format="%.2f")
            
            with col2:
                category = st.selectbox("Category", CATEGORIES)
                notes = st.text_area("Notes", height=110)
                
            submitted = st.form_submit_button("Add Expense", use_container_width=True)
            
            if submitted:
                new_expense = pd.DataFrame([{
                    "ID": st.session_state.expense_id_counter,
                    "Date": date,
                    "Amount": amount,
                    "Category": category,
                    "Notes": notes
                }])
                
                if st.session_state.expenses.empty:
                    st.session_state.expenses = new_expense
                else:
                    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
                st.session_state.expense_id_counter += 1
                
                st.success(f"Expense of ${amount:.2f} for '{category}' added successfully!")
                time.sleep(1)
                st.rerun()

    # --- DASHBOARD PAGE ---
    elif page == "Dashboard":
        st.header("📊 Analytics Dashboard")
        
        df = st.session_state.expenses
        inc_df = st.session_state.incomes
        
        if df.empty and inc_df.empty:
            st.info("No data found. Go to 'Add Income' or 'Add Expense' to get started!")
            return
            
        # Total Metrics
        total_income = inc_df['Amount'].sum() if not inc_df.empty else 0.0
        total_spent = df['Amount'].sum() if not df.empty else 0.0
        balance = total_income - total_spent
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")
        with col2:
            st.metric("Total Spending", f"${total_spent:,.2f}")
        with col3:
            st.metric("Balance", f"${balance:,.2f}")
        with col4:
            if not df.empty:
                highest_cat = df.groupby('Category')['Amount'].sum().idxmax()
                st.metric("Highest Category", highest_cat)
            else:
                st.metric("Highest Category", "N/A")
            
        st.markdown("---")
        
        # Charts
        if not df.empty:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("Spending by Category")
                cat_summary = df.groupby('Category', as_index=False)['Amount'].sum()
                fig = px.pie(cat_summary, values='Amount', names='Category', hole=0.4, 
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                  font=dict(color='#111827'))
                st.plotly_chart(fig, use_container_width=True)
                
            with col_chart2:
                st.subheader("Spending Over Time")
                date_summary = df.groupby('Date', as_index=False)['Amount'].sum().sort_values('Date')
                fig2 = px.area(date_summary, x='Date', y='Amount', markers=True,
                               color_discrete_sequence=['#00d2ff'])
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                   font=dict(color='#111827'), xaxis_title="", yaxis_title="Amount ($)")
                st.plotly_chart(fig2, use_container_width=True)
            
        # Smart Insights
        st.markdown("### 💡 Smart Insights")
        with st.container(border=True):
            st.write(f"🔹 Your net balance is **${balance:.2f}**.")
            
            if not df.empty:
                highest_cat_amt = df.groupby('Category')['Amount'].sum().max()
                avg_expense = df['Amount'].mean()
                st.write(f"🔹 Your average expense amount is **${avg_expense:.2f}**.")
                st.write(f"🔹 **{highest_cat}** accounts for **{(highest_cat_amt/total_spent)*100:.1f}%** of your total spending.")
                
                if total_spent > total_income and total_income > 0:
                    st.warning("⚠️ Alert: Your expenses exceed your income!")
                elif total_spent > 1000 and total_income == 0:
                    st.warning("⚠️ Alert: Your total spending has exceeded $1,000!")
            
            if not inc_df.empty:
                highest_inc_source = inc_df.groupby('Source')['Amount'].sum().idxmax()
                st.write(f"🔹 Your top income source is **{highest_inc_source}**.")

    # --- VIEW EXPENSES PAGE ---
    elif page == "View Expenses":
        st.header("📂 View & Filter Expenses")
        
        df = st.session_state.expenses
        
        if df.empty:
            st.info("No expenses to display.")
            return

        # Filtering
        with st.expander("🔍 Filter Options", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                sel_categories = st.multiselect("Filter by Category", CATEGORIES, default=[])
            with col2:
                # Need to convert date column to standard format to use date_input properly
                min_date = df['Date'].min()
                max_date = df['Date'].max()
                
                # If there's only 1 day of data, date_input range might be tricky
                if min_date == max_date:
                    date_range = st.date_input("Date Range", value=min_date)
                    if isinstance(date_range, datetime.date):
                        start_date = end_date = date_range
                    else:
                        start_date, end_date = date_range[0], date_range[-1]
                else:
                    date_range = st.date_input("Date Range", value=(min_date, max_date))
                    if isinstance(date_range, tuple) and len(date_range) == 2:
                        start_date, end_date = date_range[0], date_range[1]
                    else:
                        start_date = end_date = date_range[0] if isinstance(date_range, tuple) else date_range

        filtered_df = df.copy()
        
        if sel_categories:
            filtered_df = filtered_df[filtered_df['Category'].isin(sel_categories)]
            
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
        
        # Display
        st.dataframe(
            filtered_df.sort_values(by="Date", ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn(
                    "Amount ($)",
                    format="$%.2f"
                ),
                "Category": st.column_config.TextColumn(
                    "Category",
                    width="medium"
                ),
                "Notes": st.column_config.TextColumn(
                    "Notes",
                    width="large"
                ),
            }
        )

    # --- REPORTS PAGE ---
    elif page == "Reports & Export":
        st.header("📥 Export Reports")
        
        df = st.session_state.expenses
        
        if df.empty:
            st.info("No data available to export.")
            return
            
        st.markdown("You can export your current expense data to a CSV file.")
        
        # Convert df to CSV string
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="expense_report.csv",
            mime="text/csv",
        )
        
        st.markdown("---")
        st.write("Current data snapshot:")
        st.dataframe(df.head(5), hide_index=True)


if __name__ == "__main__":
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()
