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

            .visualization-header {
                background-color: none;
                padding: 10px;
                border-radius: 5px; /*for rounded corners */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /*for a subtle shadow effect */

                
                font-size: 40px;
                font-weight: bold;
                color: white; 
            }
            .visualization-header span {
                
                font-size: 24px;
                font-weight: bold;
                color: white; 
            }

            .visualization-text{
                padding: 10px;
                width: 50%;
                
                font-size: 40px;
                font-weight: bold;
                color: white; 
            }

            .paragraph{
                color: black; 
                background-color: white;
                padding: 20px;
                margin: 20px;
                border-radius: 15px;
            }

        </style>

        <div class="visualization-header">
            <h1 style='color:#a5abab;'>Visualization</h1>
        </div>

        <div class="visualization-text">
            <span>Visualize the historical data and the model's performance</span>
            <div class="paragraph">
                <p "style= font-size: 40px; text-align: justify;">Explore interactive visualizations that highlight key areas at risk of terrorist attacks in Nigeria. Our dynamic maps and data-driven charts provide a clear view of past incidents and potential coordinates. Use these insights to better understand the distribution and frequency of attacks, helping to inform preventive measures and strategic planning. Navigate through the visuals to stay informed and proactive in enhancing security within vulnerable region.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )