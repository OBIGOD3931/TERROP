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
from streamlit_extras.stylable_container import stylable_container



def app():    

    # Inject custom HTML and CSS
    st.markdown(
        """
        <style>
        .head {
            text-align: center; /* Center the text */
            font-weight: bold;  /* Make the text bold */
            text-transform: uppercase; /* Capitalize all letters */
            margin: 20px 0;
            color: #a5abab
        }

        .double-tick-line {
            border: 0;
            border-top: 3px double #dadcdc ;
            margin: 20px auto;
            width: 50%;
        }

         .centered-text {
            text-align: center; /* Center the text */
            margin: 0;
            color: #a5abab
        }
        .column-container {
            display: flex;
            justify-content: center; /* Center the columns */
            gap: 3px; /* Add space between columns */
        }
        </style>

        
        <hr class="double-tick-line">
        <hr class="double-tick-line">

        <div class="h1_header">
            <h1 class="head">COMBATING TERRORISM CENTRE</h1>
            <h2 class="head" style=color:"white">Predicting the likelihood of attack can help save lives</h2>
        </div>

        <hr class="double-tick-line">
        <hr class="double-tick-line">
        """,
        unsafe_allow_html=True
    )

    st.write("##")
    # Create a main container to center the content
    
    # Create a main container to center and align the content horizontally
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
            <div style="font-size: 30px; font-weight: bold; color: #a5abab; padding: 10px; margin-right: 20px;">
                Terrorism will spill over if you don’t speak up.
            </div>
            <div style="font-size: 35px; font-weight: bold; color: white; padding: 10px 15px; background-color: #3498db; border-radius: 5px; text-align: center;">
                ✔ Yes, it does
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )


    
    # Create a main container that extends to both edges of the page
    st.markdown(
        """
        <div style="width: 100%; padding: 20px; background-color: #f8f9fa; left: 0; border-radius: 15px">
            <div style="display: flex; justify-content: center; align-items: center;">
                <div style="text-align: center; font-size: 24px; font-weight: bold; color: #333; padding: 20px;">
                    <div style="font-size: 40px;">PREDICTION OF TERRORISM IN NIGERIA</div>
                    <div style="margin-top: 10px; font-size: 20px; font-weight: normal; color: #666; text-transform: uppercase;">
                        Terrorist activities are unpredictable in themselves since they are likely to be conducted by unknown <br> persons in an unknown place and at unpredicted times.
                    </div>
                    <!-- Double Horizontal Line -->
                    <div style="margin-top: 20px; position: relative; text-align: center;">
                        <hr style="border: none; border-top: 1px solid #ccc; position: relative; z-index: 1; margin-bottom: 0px">
                        <hr style="border: none; border-top: 1px solid #ccc; position: relative; z-index: 1; margin-top: 5px">
                    </div>
                </div>
            </div> 
        </div>
        """, 
        unsafe_allow_html=True
        )


    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Use markdown to add HTML and style the images and text inside divs
    with col1:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f8f9fa; margin: 0; padding: 0; width: 100%; gap: 0;">
                <div style="margin: 0; padding: 0;">
                    <img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQGKJsPjFR3zzOec7lpk3A8b41WIqRF-Y4BPdgwV3EugbXAqReE" alt="Terrorism creates fear" style="width: 200px; height: 200px; border-radius: 8px;">
                </div>
                <div style="font-size: 18px; color: #444; text-transform: uppercase; text-align: center; margin: 0; padding: 0;">
                    <span style="font-weight: bold;">Terrorist Attack</span> <br> Terrorism creates fear
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f8f9fa; margin: 0; padding: 0; width: 100%; gap: 0;">
                <div style="margin: 0; padding: 0;">
                    <img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQbUjB3-n3m5qYM4CgNY_yk46SQ5A2YvX6i8f8XI0QmpJ1BZjsa" alt="Terrorism creates fear" style="width: 200px; height: 200px; border-radius: 8px;">
                </div>
                <div style="font-size: 18px; color: #444; text-transform: uppercase; text-align: center; margin: 0; padding: 0;">
                    <span style="font-weight: bold;">Terrorism and Society</span> <br> The Cost of Fear and Division
                </div>
            </div>
            """,
            unsafe_allow_html=True   

        )

    with col3:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f8f9fa; margin: 0; padding: 0; width: 100%; gap: 0;">
                <div style="margin: 0; padding: 0;">
                    <img src="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQxBFl3hz9qTp4l-l8XETX8wx64fjl4v9TewQRH3kOdB0T_EU6y" alt="Terrorism creates fear" style="width: 200px; height: 200px; border-radius: 8px;">
                </div>
                <div style="font-size: 18px; color: #444; text-transform: uppercase; text-align: center; margin: 0; padding: 0;">
                    <span style="font-weight: bold;">Terrorist Activities</span> <br> A Nigerian Challenge We Must Confront
                </div>
            </div>
            """,
            unsafe_allow_html=True  

        )


    st.markdown(
        """
        <div style="width: 100%; padding: 20px; background-color: #f8f9fa; bottom: 0; left: 0; border-radius: 15px;">
            <div style="text-align: center; color: #333; font-size: 14px; padding-top: 100px; ">
                <p style="margin: 0; padding: 0;">This study is to develop and evaluate a machine learning model for the classification and forecasting of terrorist activities, with a focus on violent attacks.</p>
                <p style="margin: 0; padding: 0;">The project intends to enable real-time adaptation of prediction models. These findings offer significant insights for researchers, policymakers, and security organizations involved in effective counterterrorism efforts.</p>
            </div>
        </div>
        """,   
        unsafe_allow_html=True
    )
