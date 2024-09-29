import streamlit as st
import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
from streamlit_extras.stylable_container import stylable_container

# Firebase Configuration (from your Firebase Console)
firebaseConfig = st.secrets["firebase"]

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Firebase Admin SDK Initialization
def init_firebase_admin():
    if not firebase_admin._apps:  # Avoid re-initialization
        cred = credentials.Certificate("terrop-cfb71-8a10226b5c48.json")
        firebase_admin.initialize_app(cred)

# Function to handle signup
def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        error_message = str(e)
        if "INVALID_EMAIL" in error_message:
            st.error("The email address is badly formatted. Please check and try again.")
        elif "EMAIL_EXISTS" in error_message:
            st.error("The email address is already in use by another account.")
        else:
            st.error(f"Error: {error_message}")
        return None

# Function to handle login
def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        error_message = str(e)
        if "INVALID_EMAIL" in error_message:
            st.error("The email address is badly formatted. Please check and try again.")
        else:
            st.error(f"Error: {error_message}")
        return None

# Function to handle logout
def logout():
    st.session_state['user'] = None
    st.session_state['logged_in'] = False
    st.success("You have logged out successfully.")

# Function to display login/signup form
def display_auth_form():
    change_singup_color = """
                <style>
                .st-emotion-cache-1jmvea6.e1nzilvr4 {
                    color: #efe1cc;
                }
                .st-emotion-cache-vdokb0.e1nzilvr4 {
                    color: #a2a9a9;
                }
                </style>
                """
    st.markdown(change_singup_color, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.session_state.get('logged_in', False):
            st.subheader("You are logged in.")
            if st.button("Logout"):
                logout()
                st.experimental_rerun()  # Optional: Rerun the app to reset the state
        else:
            choice = st.selectbox("Login/Signup", ["Login", "Signup"])
            if choice == "Signup":
                st.subheader("Create a New Account")

                username = st.text_input("Username (User ID)")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.button("Create Account"):
                    if password == confirm_password:
                        init_firebase_admin()
                        user = signup(email, password)
                        if user:
                            st.success(f"Account created successfully for {username}!")
                    else:
                        st.error("Passwords do not match. Please try again.")
                st.info("Have an account? Select Login in the dropdown to login to your account")

            elif choice == "Login":
                st.subheader("Login to Your Account")

                email = st.text_input("Email")
                password = st.text_input("Password", type="password")

                if st.button("Login"):
                    init_firebase_admin()
                    user = login(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_info = user
                        st.success("Logged in successfully!")
                st.info("Don't have an account? Select Signup in the dropdown to create an account")

# Main App Logic
def app_main():
    # Set the webpage title and layout
    st.set_page_config(page_title="TERROP", page_icon='imag3.webp', layout="wide")

    # Lazy load heavy modules
    def load_modules():
        global joblib, pd, sqlite3, Image, OrdinalEncoder, LabelEncoder
        import joblib
        import pandas as pd
        import sqlite3
        from PIL import Image
        from category_encoders import OrdinalEncoder
        from sklearn.preprocessing import LabelEncoder

    from streamlit_option_menu import option_menu
    import time
    import base64

    class MultiApp:
        def __init__(self):
            self.apps = []

        def add_app(self, title, func):
            self.apps.append({"title": title, "function": func})

        def run(self):
            # Inject custom CSS to remove background color
            remove_bg_color = """
                <style>
                .stApp {
                    background-color: transparent;
                }
                </style>
            """
            st.markdown(remove_bg_color, unsafe_allow_html=True)

            @st.cache_data
            def get_base64_of_bin_file(bin_file):
                with open(bin_file, 'rb') as f:
                    data = f.read()
                return base64.b64encode(data).decode()

            def set_image_as_page_bg(image_file):
                bin_str = get_base64_of_bin_file(image_file)
                page_bg_img = f'''
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{bin_str}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                }}
                </style>
                '''
                st.markdown(page_bg_img, unsafe_allow_html=True)

            set_image_as_page_bg('images/header.jpg')

            hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                #welcome-to-terrop{
                    color: #cfcebd;
                    text-align: center;
                    font-weight: bold;
                    font-size: 80px;
                }
                #your-number-one-terrorism-predictor{
                    color: #f4f4eb;
                    text-align: center;
                    font-weight: bold;
                }
                </style>
            """
            st.markdown(hide_menu_style, unsafe_allow_html=True)

            # Option menu with sign-in/sign-up and restricted access to features
            app = option_menu(
                menu_title='TERROP',
                options=['Home', 'Visualizations', 'Prediction', 'Make a Report', 'About', 'Login/Signup'],
                icons=['house-fill', 'bar-chart-fill', 'globe', 'x-diamond-fill', 'info-circle-fill', 'person-fill'],
                menu_icon="globe-europe-africa",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {"padding": "5!important", "background-color": 'white'},
                    "icon": {"color": "#956241", "font-size": "23px"},
                    "nav-link": {"color": "#473021", "font-size": "20px", "font-weight": "bold", "centre": "left", "--hover-color": "#d2c8c2"},
                    "nav-link-selected": {"background-color": "#b79581"},
                    "menu-title": {"font-size": "30px", "color": "#473021", "font-weight": "bold"},
                }
            )

            # Home and About are always accessible
            if app == "Home":
                home.app()
            elif app == "About":
                about.app()

            # Restricted pages require login
            elif app == "Visualizations":
                if st.session_state.get('logged_in', False):
                    load_modules()
                    visualizations.app()
                else:
                    st.title("WELCOME TO TERROP")
                    st.title("Your number one terrorism predictor")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.warning("Please log-in to view the Visualizations.")
                    display_auth_form()

            elif app == "Prediction":
                if st.session_state.get('logged_in', False):
                    load_modules()
                    prediction.app()
                else:
                    st.title("WELCOME TO TERROP")
                    st.title("Your number one terrorism predictor")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.warning("Please log-in to make predictions.")
                    display_auth_form()

            elif app == "Make a Report":
                if st.session_state.get('logged_in', False):
                    load_modules()
                    make_report.app()
                else:
                    st.title("WELCOME TO TERROP")
                    st.title("Your number one terrorism predictor")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.warning("Please log-in to submit a report.")
                    display_auth_form()

            elif app == "Login/Signup":
                display_auth_form()

    # Run the app
    MultiApp().run()

# Main Entry
if __name__ == "__main__":
    # Initialize login state if not already set
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    app_main()
