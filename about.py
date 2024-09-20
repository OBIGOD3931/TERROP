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
                <style>
                        .about-header {
                            background-color: none;
                            
                            border-radius: 5px; /*for rounded corners */
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /*for a subtle shadow effect */

                            
                            font-size: 40px;
                            font-weight: bold;
                            color: white; 
                    }
                        .about-header{
                        
                            font-size: 24px;
                            font-weight: bold;
                            color: white; 
                            margin: 5px;
                    }

                        .paragraph{
                            color: black; 
                            background-color: #d7e4e4;
                            padding: 20px;
                            margin: 5px;
                            border-radius: 15px;
                            width: 50%;
                    }
                </style>

                <div class="about-header">
                    <h1 style='color:#a5abab;'>About</h1>
                </div>
                <div class="paragraph">
                    <p>This study focuses on addressing terrorism using machine learning and Geographic Information Systems (GIS). It highlights the significant impact of terrorism on various sectors, particularly in Nigeria, and the need for predictive models to understand and mitigate these threats. Machine learning's capability to analyze historical data and forecast aspects of terrorist attacks—such as weapon types, attack success, and location—supports more effective resource allocation and prevention strategies. The research integrates GIS to capture and analyze spatial data, enhancing the prediction of terrorist hotspots. By combining GIS with machine learning, the study aims to improve counterterrorism efforts, helping security agencies to prevent attacks and devise strategies that promote safety and national peace.</p>                
                </div>
            """,
            unsafe_allow_html=True
        )

    
