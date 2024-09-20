import streamlit as st
import joblib
import pandas as pd
from streamlit_option_menu import option_menu
import sqlite3
from PIL import Image
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
import geocoder
import time
import mysql.connector
import os
from dotenv import load_dotenv
import sklearn


def app():
    

    state_label_encoder = joblib.load('state_label_encoder1.pkl')      # For State
    full_data = pd.read_csv('Clean_terrorism_db.csv')

    # Get the user's IP-based location
    g = geocoder.ip('me')

    # Extract latitude and longitude
    latitude = g.latlng[0]
    longitude = g.latlng[1]

    # Reverse geocode to get the location name
    g = geocoder.osm([latitude, longitude], method='reverse')

    st.markdown(
    """
            <style>
                .stSpinner > div > div {
                    color: #e7951a;  
                    font-size: 40px; 
                }
            </style>
            <div class="make-report-header">
                    <h1 style='color:#a5abab;'>Make a Report</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    

    st.markdown(
    """
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>

            .make-report-header {
                background-color: none;
                
                border-radius: 5px; /*for rounded corners */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /*for a subtle shadow effect */

                
                font-size: 40px;
                font-weight: bold;
                color: white; 
            }
            .make-report-header {
                
                font-size: 24px;
                font-weight: bold;
                color: white; 
            }

            .paragraph{
                color: black; 
                background-color: #d7e4e4;
                padding: 20px;
                margin-top: 5px;
                margin-bottom: 50px;
                border-radius: 15px;
                width: 50%;
            }
            .st-emotion-cache-1jmvea6.e1nzilvr4{
                color: #dfe0d3; 
            }

            .st-emotion-cache-vdokb0.e1nzilvr4{
                color: #d0d8ec;
            }
            #submitted-reports{
                color: #c4edf4;
            }
            
        </style>

        
        <div class="paragraph">
                <p style= "font-size: 18px; text-align: justify; margin-bottom:20px;">To predict the likelihood of a terrorist attack in Nigeria, please fill in the required details below. Your input will help our system analyze and forecast potential risk areas, providing valuable insights for enhancing security measures. The information you provide, such as location, date, and other relevant factors, allows our predictive model to assess the probability of an attack based on historical data and current trends. This tool is designed to support proactive decision-making, helping communities, security agencies, and policymakers stay one step ahead in preventing crime and ensuring public safety. Please ensure all fields are accurately completed to receive the most reliable predictions.</p>
            </div>
        """,
        unsafe_allow_html=True
    )

    #<div data-testid="stMarkdownContainer" class="st-emotion-cache-1jmvea6 e1nzilvr4"><p>Date</p></div>
    #<div data-testid="stMarkdownContainer" class="st-emotion-cache-1jmvea6 e1nzilvr4"><p>Select the type of weapon used for the attack</p></div>
    
    # Function to fetch all reports from the database
    def fetch_reports():
        # Establish connection to the MySQL database
        conn = mysql.connector.connect(
            host='sql5.freesqldatabase.com',
            user='sql5729527',
            password='T2RVEewsi7',
            database='sql5729527'
        )

        # Create a cursor object using the connection
        c = conn.cursor()

        # Execute the SQL query to fetch all data from the reports table
        c.execute('SELECT * FROM reports')

        # Fetch all rows from the executed query
        rows = c.fetchall()

        # Get the column names from the cursor description
        #columns = [i[0] for i in c.description]

        # Close the connection
        conn.close()

        # Return the data as a pandas DataFrame
        return pd.DataFrame(rows, columns=c.column_names)

    # Display the data on the Make Report page
    def display_reports():
        st.subheader("Submitted Reports")

        # Fetch the data
        reports_df = fetch_reports()

        # Check if there are any reports
        if reports_df.empty:
            st.info("No reports found.")
        else:
            # Display the data in a table format
            st.dataframe(reports_df)

    
        

    # Function to connect and create MySQL table
    def create_reports_table():
        # Establish connection to the MySQL database
        connection = mysql.connector.connect(
        host='sql5.freesqldatabase.com',
        user='sql5729527',
        password='T2RVEewsi7',
        database='sql5729527'
        )

        # Create a cursor object using the connection
        cursor = connection.cursor()

        # Create the table with MySQL syntax
        cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        date DATE,
                        State VARCHAR(255),
                        city VARCHAR(255),
                        latitude FLOAT,
                        longitude FLOAT,
                        suicide VARCHAR(255),
                        attacktype1_txt VARCHAR(255),
                        target_type VARCHAR(255),
                        target_subtype VARCHAR(255),
                        target VARCHAR(255),
                        group_name VARCHAR(255),
                        weapon_type VARCHAR(255),
                        weapon_subtype VARCHAR(255),
                        no_killed INT,
                        no_wounded INT,
                        full_name VARCHAR(255),
                        mobile_contact VARCHAR(255),
                        email_contact VARCHAR(255),
                        address TEXT
                        )''')

        # Commit the transaction
        connection.commit()

        # Close the connection
        connection.close()


    # Function to add a report to the database
    def add_report(date, state, city, latitude, longitude, suicide,
                        attacktype1_txt, target_type, target_subtype, target, group_name,
                        weapon_type, weapon_subtype, no_killed, no_wounded, full_name,
                        mobile_contact, email_contact, address):
                        # Establish connection to the MySQL database
                        conn = mysql.connector.connect(
                                host='sql5.freesqldatabase.com',
                                user='sql5729527',
                                password='T2RVEewsi7',
                                database='sql5729527'
                            )
            
                        # Create a cursor object using the connection
                        c = conn.cursor()
            
                        # Execute the SQL command to insert data
                        c.execute('''INSERT INTO reports (date, State, city, latitude, longitude, suicide,
                                            attacktype1_txt, target_type, target_subtype, target, group_name,
                                            weapon_type, weapon_subtype, no_killed, no_wounded, full_name,
                                            mobile_contact, email_contact, address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (date, state, city, latitude, longitude, suicide,
                        attacktype1_txt, target_type, target_subtype, target, group_name,
                        weapon_type, weapon_subtype, no_killed, no_wounded, full_name,
                        mobile_contact, email_contact, address))
            
                        # Commit the transaction
                        conn.commit()
            
                        # Close the connection
                        conn.close()


    # Create the table when the app starts
    create_reports_table()

    

    # Initialize session state to manage form submission
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    if "show_report" not in st.session_state:
        st.session_state.show_report = False

    # Form for making a report
    if not st.session_state.form_submitted:
        placeholder = st.empty()
        col1, col2, col3, col4 = placeholder.columns([1, 1, 0.4, 3])  # Adjust column width ratio as needed

    
        with st.form("report_form", clear_on_submit=True):
            
            with col1:
                date = st.date_input("Date")
                state = st.selectbox("State", options=state_label_encoder.classes_)
                city = st.text_input("City")
                suicide = st.selectbox("Suicide", ["Yes", "No"])
                attacktype1_txt = st.selectbox('Select the type of attack', full_data['attacktype1_txt'].unique())
                target_type = st.selectbox('Select the target type of the attack', full_data['target_type'].unique())
                target_subtype = st.selectbox('Select the target subtype', full_data['target_subtype'].unique())
                target = st.text_input("Target (Enter the name of person or group attacked)")
                group_name = st.selectbox('Select the terrorist group name', full_data['group_name'].unique())
                
                

            with col2:
                weapon_type = st.selectbox('Select the type of weapon used for the attack', full_data['weapon_type'].unique())
                weapon_subtype = st.selectbox('Select the weapon subtype', full_data['weapon_subtype'].unique())
                no_killed = st.number_input("Number Killed", min_value=0)
                no_wounded = st.number_input("Number Wounded", min_value=0)
                full_name = st.text_input("Full Name (of user)")
                mobile_contact = st.text_input("Mobile Contact (of user)")
                email_contact = st.text_input("Email Contact (of user)")
                address = st.text_area("Address (of user)")

            with col4:
                show_reports = st.radio("Show submitted reports?", ("No", "Yes"))
                if show_reports == "Yes":
                    display_reports()  # Show the reports if "Yes" is selected
                    st.session_state.show_report = True
                else:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.info("Select 'Yes' to view submitted reports.")

           
   
            submitted = st.form_submit_button("Submit Report")

            if submitted:
                add_report(date, state, city, latitude, longitude, suicide,
                            attacktype1_txt, target_type, target_subtype, target, group_name,
                            weapon_type, weapon_subtype, no_killed, no_wounded, full_name,
                            mobile_contact, email_contact, address)

                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    with st.spinner('Feching the location of reporter...'):
                        time.sleep(5)  # Simulate a delay

                        st.markdown(
                            f"""
                                <style>
                                    .geo {{
                                        color: #a5abab;
                                        margin-left: 5px;
                                    }}
                                </style>

                                
                                <h3 style="color: #bdd3c0;">Geolocation of Reporter</h3>
                                <h4 class="geo">Latitude: {latitude}, Longitude: {longitude}</h4>
                                <h4 class="geo">{g.address}</h4>
                            """,
                            unsafe_allow_html=True
                        )
                

                with col2:

                    with st.spinner('Submitting report...'):
                        time.sleep(3)  # Simulate a delay

                        # Display the progress bar
                        progress_bar = st.progress(0)

                        # Simulate a delay with progress updates
                        for i in range(100):
                            time.sleep(0.02)  # Adjust the delay to control the speed of the progress bar
                            progress_bar.progress(i + 1)

                            
                        st.success(f"Report submitted successfully from the location with the Geographic Coordinates; {latitude}, {longitude}!")
                        st.session_state.form_submitted = True
                       

    # Option to submit another report
    if st.session_state.form_submitted:
        st.markdown(
            """
                <p style="color:white; margin-left:5px;">Thank you for your report.<p/>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Submit Another Report"):

            col1, col2, col3 = st.columns([1, 0.3, 3])
            with col1:
                st.session_state.form_submitted = False
                st.experimental_rerun()
            with col3:
                if st.session_state.show_report:
                    show_reports = st.radio("Show submitted reports?", ("No", "Yes"))
                    if st.session_state.show_report:

                    #if show_reports == "Yes":
                        st.session_state.show_report = True
                        if st.session_state.show_report:
                            display_reports()  # Show the reports if "Yes" is selected
                    else:
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.info("Select 'Yes' to view submitted reports.")
        
    