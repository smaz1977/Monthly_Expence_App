# 📊 Smart Expense Tracker Application

## 🧩 Project Overview

This is a **user-friendly web application** built using:

-   **Frontend:** Streamlit
-   **Backend:** Python

The application allows users to **track daily expenses**, visualize
spending patterns, and gain useful insights.

------------------------------------------------------------------------

## 🎯 Objectives

-   Provide a simple and clean interface
-   Allow easy expense entry
-   Generate meaningful insights
-   Ensure smooth user experience

------------------------------------------------------------------------

## 🖥️ Frontend (Streamlit)

### Features:

-   Clean and intuitive UI
-   Sidebar navigation
-   Input forms for expense entry
-   Interactive charts and tables

### UI Components:

-   Date Picker
-   Number Input (Amount)
-   Dropdown (Category)
-   Text Input (Notes)
-   Buttons (Add, Filter)

------------------------------------------------------------------------

## ⚙️ Backend (Python)

### Responsibilities:

-   Handle user inputs
-   Store and retrieve data
-   Perform calculations
-   Generate insights

### Data Storage Options:

-   CSV (Basic)
-   MySQL (Advanced)

------------------------------------------------------------------------

## 🏗️ Application Features

### 1. Add Expense

-   Input date, amount, category, notes
-   Store data persistently

### 2. View Expenses

-   Display data in table format
-   Sort and filter options

### 3. Analytics Dashboard

-   Total spending
-   Category-wise analysis
-   Monthly trends

### 4. Smart Insights

-   Detect highest spending category
-   Weekly/monthly comparisons
-   Alerts on increased spending

------------------------------------------------------------------------

## 💻 Sample Code (Basic Implementation)

``` python
import streamlit as st
import pandas as pd
import datetime

st.title("💰 Smart Expense Tracker")

date = st.date_input("Date", datetime.date.today())
amount = st.number_input("Amount", min_value=0.0)
category = st.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Other"])
notes = st.text_input("Notes")

if st.button("Add Expense"):
    new_data = pd.DataFrame({
        "Date": [date],
        "Amount": [amount],
        "Category": [category],
        "Notes": [notes]
    })

    try:
        old_data = pd.read_csv("expenses.csv")
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
    except:
        updated_data = new_data

    updated_data.to_csv("expenses.csv", index=False)
    st.success("Expense Added Successfully!")

try:
    df = pd.read_csv("expenses.csv")
    st.subheader("All Expenses")
    st.dataframe(df)

    st.subheader("Insights")
    st.write("Total Spending:", df["Amount"].sum())
    st.bar_chart(df.groupby("Category")["Amount"].sum())

except:
    st.warning("No data available")
```

------------------------------------------------------------------------

## 🚀 Advanced Enhancements

-   User Authentication (Login/Register)
-   Database Integration (MySQL)
-   Export Reports (CSV/PDF)
-   Dark Mode UI
-   API Integration

------------------------------------------------------------------------

## 🌐 Deployment Options

-   Streamlit Cloud
-   Render
-   Railway

------------------------------------------------------------------------

## 🧠 Key Highlights

-   Beginner-friendly
-   Scalable architecture
-   Clean UI/UX
-   Real-world application

------------------------------------------------------------------------

## 📌 Antigravity Prompt

Build a user-friendly Streamlit application named "Smart Expense
Tracker".

Requirements: - Frontend: Streamlit - Backend: Python - Input fields:
date, amount, category, notes - Store data in CSV - Display data in
table - Show analytics (total, category-wise) - Provide insights

Advanced: - Add authentication - Add filters - Enable report download -
Improve UI design

------------------------------------------------------------------------

## 📎 Conclusion

This project is ideal for: - Students - Beginners in Python - Portfolio
building

It demonstrates both frontend and backend integration using Python.
