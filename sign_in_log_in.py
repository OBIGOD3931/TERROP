import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

# Firebase Configuration (from your Firebase Console)
firebaseConfig = {
    'apiKey': "AIzaSyCYEZ2AWi0gtntVFhbpLytTVzWF78R00DU",
    'authDomain': "terrop-cfb71.firebaseapp.com",
    'databaseURL': "https://terrop-cfb71-default-rtdb.firebaseio.com",
    'projectId': "terrop-cfb71",
    'storageBucket': "terrop-cfb71.appspot.com",
    'messagingSenderId': "161712926661",
    'appId': "1:161712926661:web:a5f4d9c108f7413291a5ac",
    'measurementId': "G-80KS5MG0LY"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Firebase Admin SDK Initialization
cred = credentials.Certificate("terrop-cfb71-8a10226b5c48.json")
#firebase_admin.initialize_app(cred)

# Function to handle signup
def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        # st.success("You have successfully created an account.")
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
        elif "INVALID_LOGIN_CREDENTIALS" in error_message:
            st.error("The login credentials are invalid. Please check your email and password and try again.")
        else:
            st.error(f"Error: {error_message}")
        return None

# Function to handle logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = None

# Streamlit App
def app():
    # Login/Signup form
    st.title("Authentication System")

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    if st.session_state.logged_in:
        st.subheader(f"Welcome, {st.session_state.user_info['email']}!")
        
        # Sign out button
        if st.button("Sign Out"):
            logout()
            st.success("You have successfully signed out.")
            st.experimental_rerun()
    else:
        choice = st.selectbox("Login/Signup", ["Login", "Signup"])

        if choice == "Signup":
            st.subheader("Create a New Account")

            # Signup form fields
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")  # Confirm password

            if st.button("Create Account"):
                if password == confirm_password:
                    user = signup(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_info = {
                            'idToken': user.get('idToken'),
                            'localId': user.get('localId'),
                            'email': email
                        }
                        st.success(f"Account created successfully!")
                        st.experimental_rerun()
                else:
                    st.error("Passwords do not match. Please try again.")

        elif choice == "Login":
            st.subheader("Login to Your Account")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                user = login(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        'idToken': user.get('idToken'),
                        'localId': user.get('localId'),
                        'email': user.get('email')
                    }
                    st.success("Logged in successfully!")
                    st.experimental_rerun()

#if __name__ == "__main__":
 #   main()
