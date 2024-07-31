import streamlit as st
import pandas as pd

# Function to process the attendance data
def process_attendance(df):
    # required_columns = ['Email ID', 'EmpID', 'Status', 'Hours']
    # if not all(column in df.columns for column in required_columns):
    #     st.error("The input file does not contain all required columns")
    #     return None

    def process_row(row):
        if row['status'] == 'Pending' or row['Hours_worked'] < 40:
            return 'Action Required'
        return 'No Action'

    df['Action'] = df.apply(process_row, axis=1)
    return df

# Streamlit app
st.title("Attendance Dashboard")

uploaded_file = st.file_uploader("Upload your attendance Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Original Data", df)

    processed_df = process_attendance(df)

    if processed_df is not None:
        st.write("Processed Data", processed_df)

        # Generate summary
        action_summary = processed_df['Action'].value_counts()
        st.write("Summary", action_summary)

        # Download processed data
        processed_file = 'processed_attendance.xlsx'
        processed_df.to_excel(processed_file, index=False)
        with open(processed_file, 'rb') as f:
            st.download_button('Download Processed File', f, file_name='processed_attendance.xlsx')
