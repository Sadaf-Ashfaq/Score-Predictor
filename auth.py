# auth.py - Authentication UI Module

import streamlit as st
import re
from db import Database

# Initialize database
db = Database()

def apply_auth_styling():
    """Apply dark theme styling for auth pages"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Main background */
        .main {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        .block-container {
            max-width: 550px !important;
            padding: 2rem 1rem !important;
        }
        
        .auth-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 1rem;
        }
        
        .auth-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 2px solid #00d4ff;
            border-radius: 20px;
            padding: 2.5rem 2rem;
            box-shadow: 0 0 40px rgba(0, 212, 255, 0.3);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .auth-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(0, 212, 255, 0.1), transparent);
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: 1.5rem;
            position: relative;
            z-index: 1;
        }
        
        .auth-title {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        }
        
        .auth-subtitle {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
        }
        
        .auth-logo {
            font-size: 3rem;
            text-align: center;
            margin-bottom: 0.8rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }
        
        /* Input fields - compact */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 2px solid rgba(0, 212, 255, 0.3) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            padding: 0.7rem 1rem !important;
            height: 45px !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #00d4ff !important;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
            background: rgba(255, 255, 255, 0.15) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
        }
        
        .stTextInput > label {
            color: #00d4ff !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.4rem !important;
        }
        
        .stTextInput {
            margin-bottom: 0.8rem !important;
        }
        
        /* Buttons - compact */
        .stButton > button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            border-radius: 50px !important;
            width: 100% !important;
            height: 50px !important;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
            margin-top: 0.5rem !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 35px rgba(255, 107, 107, 0.6) !important;
            background: linear-gradient(135deg, #ee5a24 0%, #ff6b6b 100%) !important;
        }
        
        .auth-divider {
            text-align: center;
            margin: 1.2rem 0;
            color: rgba(255, 255, 255, 0.5);
            position: relative;
            font-size: 0.85rem;
        }
        
        .auth-divider::before,
        .auth-divider::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 42%;
            height: 1px;
            background: rgba(255, 255, 255, 0.2);
        }
        
        .auth-divider::before {
            left: 0;
        }
        
        .auth-divider::after {
            right: 0;
        }
        
        .success-message {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            padding: 0.8rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.8rem 0;
            font-weight: 500;
            font-size: 0.9rem;
            animation: slideIn 0.5s ease;
        }
        
        .error-message {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 0.8rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.8rem 0;
            font-weight: 500;
            font-size: 0.9rem;
            animation: shake 0.5s ease;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .stCheckbox {
            margin: 0.8rem 0 !important;
        }
        
        .stCheckbox > label {
            color: rgba(255, 255, 255, 0.8) !important;
            font-size: 0.85rem !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        header {visibility: hidden;}
        
        /* Responsive */
        @media (max-width: 768px) {
            .auth-card {
                padding: 2rem 1.5rem;
            }
            .auth-title {
                font-size: 1.8rem;
            }
            .auth-logo {
                font-size: 2.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not any(char.isdigit() for char in password):
        return True, "Password is valid (consider adding numbers for extra security)"
    return True, "Password is valid"

def login_page():
    """Display login page"""
    apply_auth_styling()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    # Header without container
    st.markdown('<div class="auth-logo">🎓</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">Student Score Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Login to access your account</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember me")
        
        submit_button = st.form_submit_button("🚀 Login")
        
        if submit_button:
            if not username or not password:
                st.markdown('<div class="error-message">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                # Verify credentials
                result = db.verify_user(username, password)
                
                if result['success']:
                    # Store user info in session state
                    st.session_state.authenticated = True
                    st.session_state.user = result['user']
                    st.session_state.show_results = False
                    
                    st.markdown('<div class="success-message">✅ Login Successful! Redirecting...</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-message">❌ {result["message"]}</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="auth-divider">OR</div>', unsafe_allow_html=True)
    
    # Switch to signup
    if st.button("📝 Create New Account", key="switch_to_signup", use_container_width=True):
        st.session_state.auth_page = "signup"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    """Display signup page"""
    apply_auth_styling()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="auth-logo">📝</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">Create Account</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Join the Student Score Predictor community</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Signup form
    with st.form("signup_form", clear_on_submit=False):
        full_name = st.text_input("👤 Full Name", placeholder="Enter your full name", key="signup_fullname")
        username = st.text_input("🆔 Username", placeholder="Choose a username", key="signup_username")
        email = st.text_input("📧 Email", placeholder="Enter your email", key="signup_email")
        password = st.text_input("🔒 Password", type="password", placeholder="Create a password (min 6 characters)", key="signup_password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
        
        terms_agreed = st.checkbox("I agree to the Terms and Conditions")
        
        submit_button = st.form_submit_button("🚀 Sign Up")
        
        if submit_button:
            # Validation
            if not all([full_name, username, email, password, confirm_password]):
                st.markdown('<div class="error-message">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
            elif not validate_email(email):
                st.markdown('<div class="error-message">⚠️ Invalid email format</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="error-message">⚠️ Passwords do not match</div>', unsafe_allow_html=True)
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    st.markdown(f'<div class="error-message">⚠️ {message}</div>', unsafe_allow_html=True)
                elif not terms_agreed:
                    st.markdown('<div class="error-message">⚠️ Please agree to the Terms and Conditions</div>', unsafe_allow_html=True)
                else:
                    # Create user
                    result = db.create_user(username, email, password, full_name)
                    
                    if result['success']:
                        st.markdown('<div class="success-message">✅ Account created successfully! Please login.</div>', unsafe_allow_html=True)
                        st.balloons()
                        st.session_state.auth_page = "login"
                        # Auto redirect after 2 seconds
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">❌ {result["message"]}</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="auth-divider">OR</div>', unsafe_allow_html=True)
    
    # Switch to login
    if st.button("🔙 Back to Login", key="switch_to_login", use_container_width=True):
        st.session_state.auth_page = "login"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = "login"
    
    return st.session_state.authenticated

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    if 'user' in st.session_state:
        del st.session_state.user
    if 'show_results' in st.session_state:
        del st.session_state.show_results
    if 'prediction_data' in st.session_state:
        del st.session_state.prediction_data
    st.session_state.auth_page = "login"
    st.rerun()

def get_current_user():
    """Get current logged in user"""
    if 'user' in st.session_state:
        return st.session_state.user
    return None

    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not any(char.isdigit() for char in password):
        return True, "Password is valid (consider adding numbers for extra security)"
    return True, "Password is valid"

def login_page():
    """Display login page"""
    apply_auth_styling()
    
    
    st.markdown('<h1 class="auth-title">Welcome Back!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Login to access your Student Score Predictor</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember me")
        
        submit_button = st.form_submit_button("🚀 Login")
        
        if submit_button:
            if not username or not password:
                st.markdown('<div class="error-message">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                # Verify credentials
                result = db.verify_user(username, password)
                
                if result['success']:
                    # Store user info in session state
                    st.session_state.authenticated = True
                    st.session_state.user = result['user']
                    st.session_state.show_results = False
                    
                    st.markdown('<div class="success-message">✅ Login Successful! Redirecting...</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-message">❌ {result["message"]}</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="auth-divider">OR</div>', unsafe_allow_html=True)
    
    # Switch to signup
    if st.button("📝 Create New Account", key="switch_to_signup", use_container_width=True):
        st.session_state.auth_page = "signup"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    """Display signup page"""
    apply_auth_styling()
    
   
    st.markdown('<h1 class="auth-title">Create Account</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Join the Student Score Predictor community</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Signup form
    with st.form("signup_form", clear_on_submit=False):
        full_name = st.text_input("👤 Full Name", placeholder="Enter your full name", key="signup_fullname")
        username = st.text_input("🆔 Username", placeholder="Choose a username", key="signup_username")
        email = st.text_input("📧 Email", placeholder="Enter your email", key="signup_email")
        password = st.text_input("🔒 Password", type="password", placeholder="Create a password (min 6 characters)", key="signup_password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
        
        terms_agreed = st.checkbox("I agree to the Terms and Conditions")
        
        submit_button = st.form_submit_button("🚀 Sign Up")
        
        if submit_button:
            # Validation
            if not all([full_name, username, email, password, confirm_password]):
                st.markdown('<div class="error-message">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
            elif not validate_email(email):
                st.markdown('<div class="error-message">⚠️ Invalid email format</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="error-message">⚠️ Passwords do not match</div>', unsafe_allow_html=True)
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    st.markdown(f'<div class="error-message">⚠️ {message}</div>', unsafe_allow_html=True)
                elif not terms_agreed:
                    st.markdown('<div class="error-message">⚠️ Please agree to the Terms and Conditions</div>', unsafe_allow_html=True)
                else:
                    # Create user
                    result = db.create_user(username, email, password, full_name)
                    
                    if result['success']:
                        st.markdown('<div class="success-message">✅ Account created successfully! Please login.</div>', unsafe_allow_html=True)
                        st.balloons()
                        st.session_state.auth_page = "login"
                        # Auto redirect after 2 seconds
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">❌ {result["message"]}</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="auth-divider">OR</div>', unsafe_allow_html=True)
    
    # Switch to login
    if st.button("🔙 Back to Login", key="switch_to_login", use_container_width=True):
        st.session_state.auth_page = "login"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = "login"
    
    return st.session_state.authenticated

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    if 'user' in st.session_state:
        del st.session_state.user
    if 'show_results' in st.session_state:
        del st.session_state.show_results
    if 'prediction_data' in st.session_state:
        del st.session_state.prediction_data
    st.session_state.auth_page = "login"
    st.rerun()

def get_current_user():
    """Get current logged in user"""
    if 'user' in st.session_state:
        return st.session_state.user
    return None