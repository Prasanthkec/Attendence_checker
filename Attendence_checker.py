import streamlit as st
import pandas as pd
import xlrd
from datetime import datetime,timedelta

# def process_previous_week_attendance(df):


#     def process_row(row):
#         if row['State'] == 'Submitted' and row['Total Hours'] < 40:
#             return 'Action Required Status still in Submitted and Hours less than 40'
#         elif row['State'] == 'Submitted' :
#             return 'Action Required Status still in Submitted'
        
#         return 'No Action'

#     df['Action'] = df.apply(process_row, axis=1)
#     df['Action'] = df['Action'].astype(str)
#     Action_req_df = df[df['Action'].str.contains('Action Required')]
#     return Action_req_df

def process_previous_week_attendance(df):


    def process_row(row):
        if row['State'] == 'Submitted' and row['Total Hours'] < 40:
            return 'Action Required Status still in Submitted and Hours less than 40'
        elif row['State'] == 'Submitted' :
            return 'Action Required Status still in Submitted'
        elif row['State'] == 'Pending' :
            return 'Action Required status Pending'
        return 'No Action'

    df['Action'] = df.apply(process_row, axis=1)
    df['Action'] = df['Action'].astype(str)
    Action_req_df = df[df['Action'].str.contains('Action Required')]
    return Action_req_df

def process_current_week_attendance(df):

    def process_row(row):
        
        if row['State'] == 'Pending' :
            return 'Action Required for current week status Pending'
        if row['Total Hours'] < 40 and row['State'] == 'Submitted':
           return 'Action Required for current week Hours less than 40 '
        return 'No Action'

    df['Action'] = df.apply(process_row, axis=1)
    df['Action'] = df['Action'].astype(str)
    Action_req_df = df[df['Action'].str.contains('Action Required')]
    return Action_req_df

st.title("Attendance Dashboard")

uploaded_file = st.file_uploader("Upload your attendance Excel file", type=["xls", "xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    #st.write("Original Data", df)

    df['Week starts on'] = pd.to_datetime(df['Week starts on'])
    #print('Week starts on',df['Week starts on'] )
    #need to enable
    #today = datetime.today()
    today = datetime.strptime('2024-07-25 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
    print(today)
    start_of_week = (today - timedelta(days = today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
   
    print('start_of_week',start_of_week)
    start_of_previous_week = start_of_week - timedelta(days=7)
    print('start_of_previous_week',start_of_previous_week)
    current_week_df = df[df['Week starts on']==start_of_week ]
    previous_week_df = df[df['Week starts on']==start_of_previous_week]
    previous_week_processed_df = process_previous_week_attendance(previous_week_df)
    current_week_processed_df = process_current_week_attendance(current_week_df)

    processed_df = pd.concat([current_week_processed_df,previous_week_processed_df])
    
    if processed_df is not None:
        st.write("Processed Data", processed_df)

        
        action_summary = processed_df['Action'].value_counts()
        st.write("Summary", action_summary)

        
        processed_file = 'processed_attendance.xlsx'
        processed_df.to_excel(processed_file, index=False)
        with open(processed_file, 'rb') as f:
            st.download_button('Download Processed File', f, file_name='processed_attendance.xlsx')
