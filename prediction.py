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

    st.markdown(
    """
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>

            .prediction-header2 {
                font-family: 'Roboto', sans-serif;
                color: #e3e5c1;
                width: 30%;
                padding: 10px;
                margin-left: 470px;
                border-radius: 5px; /* Optional: for rounded corners */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: for a subtle shadow effect */
            }
            .prediction-header span {
                'Roboto', sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: white; /* Optional: change the text color */
            }
        </style>
        <div class="prediction-header1">
            "<h1 style='color:#a5abab;'>Prediction</h1>" 
        </div>

        <div class="prediction-header2">             
            <span style="font-weight: bold;">Input Features</span>
            <p style="color: #c2d6d6;">Kindly fill the form below and click the predict button to make a prediction.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Load the trained Random Forest model
    model = joblib.load('final_model1.pkl') 

    # Load the encoders used during training
    #ordinal_encoders = joblib.load('re_ordinal_encoders.pkl')  # For year, month, and day
    state_label_encoder = joblib.load('state_label_encoder1.pkl')      # For State

    # Load the training dataset
    training_data = pd.read_csv('dataset_before_encoding.csv')  
    full_data = pd.read_csv('Clean_terrorism_db.csv')

    # Extract state-specific data
    state_data = training_data.groupby('State').agg({
        'mean_pct_read_seng15': 'mean',  
    #   'avg_houshold_size': 'mean'
    }).reset_index()


    
    st.markdown(
        """
            <style>
                /* Increase space between the two columns */
                div.css-1lcbmhc {
                    margin-right: 50px; /* Adjust this value to increase the space */
                }
            </style>
        """, unsafe_allow_html=True
    )

    st.markdown(
    """
            <style>
                /* Custom styling for labels */
            .st-emotion-cache-1jmvea6.e1nzilvr4 {
            font-size: 18px;
            color: white;
            font-weight: bold;
            margin-bottom: 5px;
    }

            div[data-testid="stSelectbox"] div[role="combobox"] {
                background-color: #e3f4f4; /* Green background for state selectbox */
                color: black;
            }
            div[data-testid="stNumberInput"] input {
                background-color: #e3f4f4; /* Pink background for number input (year, month, day) */
                color: black;
            }
        </style>
    """,

#<div data-testid="stMarkdownContainer" class="st-emotion-cache-1jmvea6 e1nzilvr4"><p>State</p></div>


    unsafe_allow_html=True
    )

    col1, col2, spacer, col3, col4 = st.columns([1, 1, 0.1, 1, 1])  # Adjust column width ratio as needed


    with col2:
        # Input fields for features
        state = st.selectbox("State", options=state_label_encoder.classes_)  # Use label encoder classes for selection

        # Automatically set mean_pct_read_seng15 and avg_unemploy_state based on selected State 
        mean_pct_read_seng15 = state_data[state_data['State'] == state]['mean_pct_read_seng15'].values[0]
        # avg_houshold_size = state_data[state_data['State'] == state]['avg_houshold_size'].values[0]

            
        # Input fields for year, month, and day
        year = st.number_input("Year", min_value=2000, max_value=2100, value=2024)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        day = st.number_input("Day", min_value=1, max_value=31, value=1)

    # Create a DataFrame for the inputs
    input_df = pd.DataFrame({
            'mean_pct_read_seng15': [mean_pct_read_seng15],
        #   'avg_houshold_size': [avg_houshold_size],
            'year': [year],
            'month': [month],
            'day': [day],
            'State': [state]
        })

        

        
    input_df['State'] = state_label_encoder.transform(input_df['State'])

    st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50; /* Green background */
        border: none; /* Remove borders */
        color: white; /* White text */
        padding: 15px 32px; /* Some padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* Remove underline */
        display: inline-block; /* Get the element to line up correctly */
        font-size: 35px; /* Increase font size */
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer/hand icon */
        border-radius: 8px; /* Rounded corners */
        margin-top: 27px;
    }
    .stButton>button:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    </style>
    """, unsafe_allow_html=True)


    with col3:
        # Add a button for making predictions
        


        if st.button('Predict'):
            # Make prediction
            probability = model.predict_proba(input_df)[0][1]  # Probability of terrorist attack 

            # Display the result
            st.markdown(f"<h2 style='color:#a5abab;'>Prediction</h2>", unsafe_allow_html=True)


            # Check if the probability exceeds 60%
            if probability > 0.6:
                # Display in red
                st.markdown(f"<span style='color:red;'>The probability of a terrorist attack in {state} is: {probability:.2%}.</span>", unsafe_allow_html=True)
                st.warning("This is a high-risk situation. It is recommended that the security agency take appropriate precautionary measures "
                    "to ensure maximum security and mitigation of a possible attack..")
            elif probability > 0.8:
                st.markdown(f"<span style='color:red;'>The probability of a terrorist attack in {state} is: {probability:.2%}.</span>", unsafe_allow_html=True)
                st.warning("This is a very high-risk situation with low uncertainty. It is strongly recommended that the security agency take appropriate precautionary measures "
                    "to ensure maximum security and mitigation of a possible attack.") 

            else:
                # Display in default color
                st.markdown(f"<span style='color:white;'>The probability of a terrorist attack in {state} is: {probability:.2%}.</span>", unsafe_allow_html=True)

                                    