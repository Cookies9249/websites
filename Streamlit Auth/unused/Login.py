### NOT IN USE ###

# Imports
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

import yaml
from yaml.loader import SafeLoader

def load_view(authenticator):
    # Initialize authenticator
    with open('data/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Not Logged In
    if not st.session_state["authentication_status"]:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Log In", "Register", "Forgot Username", "Forgot Password"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"  # remove for vertical
        )
        
        _, middle_column, _ = st.columns((1,2,1))
        with middle_column:
            # Log In
            if selected == "Log In" or selected == None:
                name, authentication_status, username = authenticator.login('Login', 'main')
                if st.session_state["authentication_status"] is False:
                    st.error('Invalid Username or Password')
                if st.session_state["authentication_status"] is None:
                    st.warning('Please enter your username and password')

            # Register User
            elif selected == "Register":
                try:
                    if authenticator.register_user('Register user', preauthorization=False):
                        st.success('User registered successfully')
                except Exception as e:
                    st.error(e)

            # Reset Username
            elif selected == "Forgot Username":
                try:
                    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                    if username_forgot_username:
                        st.success('Username sent securely')
                        # Username to be transferred to user securely
                    else:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)

            # Reset Password
            elif selected == "Forgot Password":
                try:
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                    if username_forgot_pw:
                        st.success('New password sent securely')
                        # Random password to be transferred to user securely
                    else:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)

    # Logged In
    if st.session_state["authentication_status"]:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Main Menu", "Update User Details"],
            icons=["house", "gear"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )   

        # Main Menu
        if selected == "Main Menu":
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.title('Some content')

        # Update Email, Username, Password
        elif selected == "Update User Details":
            try:
                if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)
            try:
                if authenticator.reset_password(st.session_state["username"], 'Reset password'):
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)
        
        # Log Out
        st.markdown("###")
        authenticator.logout('Logout', 'main', key='unique_key')
    
    # Update Configs (auth)
    with open('data/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
