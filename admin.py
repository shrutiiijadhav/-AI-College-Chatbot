import streamlit as st
import pandas as pd
import os

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Admin Dashboard", page_icon="📊")
st.title("📊 College Chatbot Admin Dashboard")

# -------------------------
# FILE PATH (IMPORTANT)
# -------------------------
file_path = r"C:\Users\Morya\Desktop\chatbot\FAQ_chatbot.csv"

# -------------------------
# CHECK FILE EXISTS
# -------------------------
if not os.path.exists(file_path):
    st.error("❌ CSV file not found! Check file path.")
    st.stop()

# -------------------------
# LOAD DATA (FIX FORMAT)
# -------------------------
df = pd.read_csv(file_path)

# Fix if CSV is in single column
if len(df.columns) == 1:
    df = df[df.columns[0]].str.split(",", expand=True)

# Set correct column names
df.columns = ["question", "answer", "category"]

# -------------------------
# SIDEBAR MENU
# -------------------------
menu = st.sidebar.selectbox(
    "Menu",
    ["View Data", "Add FAQ", "Delete FAQ", "Search", "Statistics"]
)

# -------------------------
# VIEW DATA
# -------------------------
if menu == "View Data":
    st.subheader("📋 All FAQ Data")
    st.dataframe(df)

# -------------------------
# ADD FAQ
# -------------------------
elif menu == "Add FAQ":
    st.subheader("➕ Add New FAQ")

    question = st.text_input("Question")
    answer = st.text_input("Answer")
    category = st.text_input("Category")

    if st.button("Add"):
        if question and answer and category:
            new_row = pd.DataFrame([[question, answer, category]],
                                   columns=["question", "answer", "category"])

            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file_path, index=False)

            st.success("✅ FAQ added successfully!")
        else:
            st.warning("⚠️ Please fill all fields")

# -------------------------
# DELETE FAQ
# -------------------------
elif menu == "Delete FAQ":
    st.subheader("❌ Delete FAQ")

    st.dataframe(df)

    index = st.number_input("Enter row index to delete", min_value=0, max_value=len(df)-1)

    if st.button("Delete"):
        df = df.drop(index)
        df.to_csv(file_path, index=False)
        st.success("✅ Deleted successfully!")

# -------------------------
# SEARCH
# -------------------------
elif menu == "Search":
    st.subheader("🔍 Search FAQ")

    search_term = st.text_input("Enter keyword")

    if search_term:
        results = df[df["question"].str.contains(search_term, case=False, na=False)]
        st.write(results)

# -------------------------
# STATISTICS
# -------------------------
elif menu == "Statistics":
    st.subheader("📊 Dashboard Stats")

    st.write("Total Questions:", len(df))

    category_counts = df["category"].value_counts()
    st.bar_chart(category_counts)

# -------------------------
# DOWNLOAD OPTION
# -------------------------
st.sidebar.subheader("⬇️ Download Data")

st.sidebar.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="FAQ_updated.csv",
    mime="text/csv"
)