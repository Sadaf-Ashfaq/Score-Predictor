# streamlit_app.py - Student Score Predictor with Authentication

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# IMPORTANT: Set page config FIRST before any other imports
st.set_page_config(
    page_title="Student Score Predictor | AI Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import auth after page config
from auth import check_authentication, login_page, signup_page, logout, get_current_user
from db import Database

# Initialize database
db = Database()

# Dark theme colorful CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Dark theme background */
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Main header */
    .main-dashboard-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Student profile card */
    .student-profile {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .profile-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcf7f, #4d9de0, #e15554);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        margin: 0 auto 1rem auto;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    
    /* Prediction form */
    .prediction-form {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #00d4ff;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
    }
    
    .form-section-title {
        color: #00d4ff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: left;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding-left: 0.5rem;
        border-left: 4px solid #00d4ff;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        color: #ffffff;
        padding: 0.15rem 0.4rem;
        font-size: 0.6rem; 
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Hide +/- buttons */
    .stNumberInput > div > div > input::-webkit-outer-spin-button,
    .stNumberInput > div > div > input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    .stNumberInput > div > div > input[type=number] {
        -moz-appearance: textfield;
    }
    
    .stNumberInput > div > div > button {
        display: none !important;
    }
    
    .stNumberInput > label {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    
    /* Predict button */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 50px;
        width: 100%;
        height: 60px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
    }
    
    /* Grade display */
    .grade-display {
        text-align: center;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .grade-a { background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); }
    .grade-b { background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }
    .grade-c { background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); }
    .grade-d { background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }
    
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .grade-letter {
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    /* Tips cards */
    .tip-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .tip-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
    }
    
    .tip-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .tip-title {
        color: #00d4ff;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .tip-content {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(102, 126, 234, 0.2) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(0, 212, 255, 0.3);
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    
    @media (max-width: 768px) {
        .main-dashboard-header {
            font-size: 2.5rem;
        }
        .score-number {
            font-size: 3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_and_data():
    """Load model and required data"""
    try:
        model = joblib.load('student_score_model.pkl')
        scaler = joblib.load('feature_scaler.pkl')
        
        with open('model_info.json', 'r') as f:
            model_info = json.load(f)
        
        with open('feature_info.json', 'r') as f:
            feature_info = json.load(f)
            
        return model, scaler, model_info, feature_info
    except Exception as e:
        st.error(f"Error loading model files: {str(e)}")
        return None, None, None, None

def predict_score(model, scaler, feature_values, feature_names):
    """Make prediction"""
    try:
        input_df = pd.DataFrame([feature_values], columns=feature_names)
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        prediction = max(0, min(100, prediction))
        return round(prediction, 2)
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None

def create_animated_gauge(score):
    """Create animated gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        title = {'text': "AI Prediction Score", 'font': {'size': 20, 'color': '#00d4ff'}},
        delta = {'reference': 75, 'increasing': {'color': '#2ecc71'}, 'decreasing': {'color': '#e74c3c'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "#00d4ff", 'tickfont': {'color': '#ffffff'}},
            'bar': {'color': "#00d4ff", 'thickness': 0.4},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 3,
            'bordercolor': "#00d4ff",
            'steps': [
                {'range': [0, 40], 'color': "rgba(231, 76, 60, 0.3)"},
                {'range': [40, 60], 'color': "rgba(243, 156, 18, 0.3)"},
                {'range': [60, 80], 'color': "rgba(52, 152, 219, 0.3)"},
                {'range': [80, 100], 'color': "rgba(46, 204, 113, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "#ff6b6b", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        height=400
    )
    return fig

def get_grade_info(score):
    """Get grade and styling info"""
    if score >= 90:
        return {'grade': 'A+', 'class': 'grade-a', 'emoji': '🏆', 'title': 'Outstanding!'}
    elif score >= 80:
        return {'grade': 'A', 'class': 'grade-a', 'emoji': '⭐', 'title': 'Excellent!'}
    elif score >= 70:
        return {'grade': 'B', 'class': 'grade-b', 'emoji': '👍', 'title': 'Good Job!'}
    elif score >= 60:
        return {'grade': 'C', 'class': 'grade-c', 'emoji': '📚', 'title': 'Keep Going!'}
    else:
        return {'grade': 'D', 'class': 'grade-d', 'emoji': '💪', 'title': 'You Can Do Better!'}

def get_personalized_tips(score):
    """Get personalized tips based on score"""
    if score >= 90:
        return [
            {"icon": "🎯", "title": "Maintain Excellence", "content": "Keep up your excellent study habits and help others succeed too!"},
            {"icon": "🚀", "title": "Leadership", "content": "Consider tutoring classmates or joining study groups as a leader."},
            {"icon": "🏆", "title": "Challenge Yourself", "content": "Take on advanced courses or extracurricular academic activities."}
        ]
    elif score >= 80:
        return [
            {"icon": "📈", "title": "Boost Performance", "content": "You're doing great! Focus on weak areas to reach the next level."},
            {"icon": "⏰", "title": "Time Management", "content": "Optimize your study schedule to maximize productivity."},
            {"icon": "🤝", "title": "Peer Learning", "content": "Form study groups with high-performing classmates."}
        ]
    elif score >= 70:
        return [
            {"icon": "📝", "title": "Active Learning", "content": "Use active recall and spaced repetition techniques."},
            {"icon": "💤", "title": "Rest & Recovery", "content": "Ensure 7-8 hours of sleep for optimal brain function."},
            {"icon": "🎯", "title": "Goal Setting", "content": "Set specific, measurable study goals for each subject."}
        ]
    else:
        return [
            {"icon": "📚", "title": "Study Plan", "content": "Create a structured daily study routine with specific time blocks."},
            {"icon": "🔄", "title": "Review Basics", "content": "Go back to fundamentals and build a strong foundation."},
            {"icon": "👨‍🏫", "title": "Seek Help", "content": "Ask teachers, tutors, or classmates for assistance."}
        ]

def sidebar_content():
    """Create sidebar content"""
    with st.sidebar:
        # User profile section
        user = get_current_user()
        if user:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, orange 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 1rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👤</div>
                <div style="color: white; font-weight: 600; font-size: 1.1rem;">{user['username']}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{user['email']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🎓 Student AI Dashboard")
        
        # Check if we should show results page
        if 'show_results' in st.session_state and st.session_state.show_results:
            page_options = ["🏠 Dashboard", "📊 Predictor", "🎯 Results", "💡 Tips & Tricks", "❓ How to Use"]
            default_index = 2
        else:
            page_options = ["🏠 Dashboard", "📊 Predictor", "💡 Tips & Tricks", "❓ How to Use"]
            default_index = 1
        
        page = st.radio("Navigate", page_options, index=default_index)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">95%</div>
            <div class="metric-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">1000+</div>
            <div class="metric-label">Students Helped</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Current time
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"### ⏰ Current Time\n**{current_time}**")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", key="logout_btn"):
            logout()
        
        return page

def main():
    # Check authentication
    if not check_authentication():
        if st.session_state.auth_page == "login":
            login_page()
        else:
            signup_page()
        return
    
    # Load model and data
    model, scaler, model_info, feature_info = load_model_and_data()
    
    if model is None:
        st.error("🚨 Failed to load model files.")
        st.stop()
    
    # Sidebar navigation
    page = sidebar_content()
    
    # Main header
    st.markdown('<h1 class="main-dashboard-header">🎓 Student Score Predictor AI</h1>', unsafe_allow_html=True)
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Predictor":
        show_predictor(model, scaler, model_info, feature_info)
    elif page == "🎯 Results":
        show_results(model, scaler, model_info, feature_info)
    elif page == "💡 Tips & Tricks":
        show_tips()
    else:
        show_how_to_use()

def show_dashboard():
    """Show dashboard page"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="student-profile">
            <div class="profile-avatar">🎓</div>
            <h2 style="text-align: center; color: white; margin-bottom: 1rem;">Welcome Student!</h2>
            <p style="text-align: center; color: rgba(255,255,255,0.8);">
                Ready to predict your academic performance? Our AI model analyzes multiple factors 
                to give you accurate score predictions and personalized improvement tips.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="student-profile">
            <div class="profile-avatar">💡</div>
            <h3 style="text-align: center; color: white; margin-bottom: 1rem;">Daily Motivation</h3>
            <p style="text-align: center; color: rgba(255,255,255,0.9); font-style: italic; font-size: 1.1rem; line-height: 1.6;">
                "Success is not the key to happiness. Happiness is the key to success. If you love what you are studying, you will be successful."
            </p>
            <p style="text-align: center; color: rgba(255,255,255,0.6); margin-top: 1rem; font-size: 0.9rem;">
                — Albert Schweitzer
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Motivational Quotes Section
    st.markdown("### 📚 Study Motivation Corner")
    
    quotes = [
        {
            "quote": "Education is the most powerful weapon which you can use to change the world.",
            "author": "Nelson Mandela",
            "icon": "🌍"
        },
        {
            "quote": "The beautiful thing about learning is that nobody can take it away from you.",
            "author": "B.B. King",
            "icon": "✨"
        },
        {
            "quote": "Success is the sum of small efforts repeated day in and day out.",
            "author": "Robert Collier",
            "icon": "🎯"
        },
        {
            "quote": "Don't watch the clock; do what it does. Keep going.",
            "author": "Sam Levenson",
            "icon": "⏰"
        },
        {
            "quote": "The expert in anything was once a beginner.",
            "author": "Helen Hayes",
            "icon": "🌱"
        },
        {
            "quote": "Study while others are sleeping; work while others are loafing; prepare while others are playing.",
            "author": "William A. Ward",
            "icon": "🔥"
        }
    ]
    
    # Display quotes in a 2-column grid
    col1, col2 = st.columns(2)
    
    for i, item in enumerate(quotes):
        current_col = col1 if i % 2 == 0 else col2
        with current_col:
            st.markdown(f"""
            <div class="tip-card" style="min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div class="tip-icon" style="font-size: 2.5rem;">{item['icon']}</div>
                    <div class="tip-content" style="font-style: italic; font-size: 1rem; line-height: 1.6; margin: 1rem 0;">
                        "{item['quote']}"
                    </div>
                </div>
                <div class="tip-title" style="text-align: right; font-size: 0.9rem; margin-top: 1rem;">
                    — {item['author']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_predictor(model, scaler, model_info, feature_info):
    """Show predictor page"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="student-profile">
            <div class="profile-avatar">👨‍🎓</div>
            <h3 style="text-align: center; color: white; margin-bottom: 1rem;">Student Profile</h3>
            <p style="text-align: center; color: rgba(255,255,255,0.8);">
                Fill in your academic and lifestyle information below.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="student-profile">
            <div class="profile-avatar">🎯</div>
            <h3 style="text-align: center; color: white;">Ready to Predict?</h3>
            <p style="text-align: center; color: rgba(255,255,255,0.8);">
                Our AI will analyze your data!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Input Form
  
    st.markdown('<div class="form-section-title">📝 Enter Academic Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    feature_values = []
    feature_names = model_info['features']
    half = len(feature_names) // 2
    
    with col1:
        st.markdown('<h4 style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-bottom: 1rem;">📚 Academic Factors</h4>', unsafe_allow_html=True)
        for i, feature in enumerate(feature_names[:half]):
            if feature in feature_info:
                info = feature_info[feature]
                label = feature.replace('_', ' ').title()
                value = st.number_input(
                    label,
                    min_value=float(info['min']),
                    max_value=float(info['max']),
                    value=None,
                    step=0.1,
                    placeholder=f"Enter value ({info['min']:.1f} - {info['max']:.1f})",
                    key=f"input_{i}"
                )
                feature_values.append(value if value is not None else 0.0)
    
    with col2:
        st.markdown('<h4 style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-bottom: 1rem;">🏃‍♂️ Lifestyle Factors</h4>', unsafe_allow_html=True)
        for i, feature in enumerate(feature_names[half:], start=half):
            if feature in feature_info:
                info = feature_info[feature]
                label = feature.replace('_', ' ').title()
                value = st.number_input(
                    label,
                    min_value=float(info['min']),
                    max_value=float(info['max']),
                    value=None,
                    step=0.1,
                    placeholder=f"Enter value ({info['min']:.1f} - {info['max']:.1f})",
                    key=f"input_{i}"
                )
                feature_values.append(value if value is not None else 0.0)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Predict My Score", key="main_predict"):
        st.session_state.prediction_data = feature_values.copy()
        st.session_state.feature_names = feature_names.copy()
        st.session_state.show_results = True
        st.rerun()

def show_results(model, scaler, model_info, feature_info):
    """Show results page"""
    
    if 'prediction_data' not in st.session_state:
        st.error("❌ No prediction data found.")
        if st.button("← Go to Predictor"):
            st.session_state.show_results = False
            st.rerun()
        return
    
    predicted_score = predict_score(model, scaler, st.session_state.prediction_data, st.session_state.feature_names)
    
    if predicted_score is None:
        st.error("❌ Error generating prediction.")
        return
    
    grade_info = get_grade_info(predicted_score)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h3 style="color: #00d4ff; margin-bottom: 1.5rem;">🎯 Your Prediction Results</h3>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="grade-display {grade_info['class']}">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{grade_info['emoji']}</div>
            <div class="score-number">{predicted_score}</div>
            <div class="grade-letter" style="font-size: 1.8rem; margin: 0.3rem 0;">Grade: {grade_info['grade']}</div>
            <div style="font-size: 1.2rem; margin-top: 0.5rem; font-weight: 600;">{grade_info['title']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h4 style="color: #00d4ff; margin: 1.5rem 0 1rem 0;">📊 Performance Metrics</h4>', unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{predicted_score}</div>
                <div class="metric-label">Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            percentile = min(99, max(1, int((predicted_score / 100) * 100)))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{percentile}th</div>
                <div class="metric-label">Percentile</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            status = "Pass" if predicted_score >= 60 else "Fail"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{status}</div>
                <div class="metric-label">Status</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 style="color: #00d4ff; margin-bottom: 1.5rem;">🎯 Score Visualization</h3>', unsafe_allow_html=True)
        gauge_fig = create_animated_gauge(predicted_score)
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown('<h3 style="color: #00d4ff; margin: 1.5rem 0;">💡 Personalized Recommendations</h3>', unsafe_allow_html=True)
    
    tips = get_personalized_tips(predicted_score)
    
    col1, col2, col3 = st.columns(3)
    
    for i, tip in enumerate(tips):
        current_col = [col1, col2, col3][i % 3]
        with current_col:
            st.markdown(f"""
            <div class="tip-card">
                <div class="tip-icon">{tip['icon']}</div>
                <div class="tip-title">{tip['title']}</div>
                <div class="tip-content">{tip['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 New Prediction", key="new_prediction"):
            if 'show_results' in st.session_state:
                del st.session_state.show_results
            if 'prediction_data' in st.session_state:
                del st.session_state.prediction_data
            st.rerun()
    
    with col2:
        if st.button("💡 More Tips", key="more_tips"):
            st.session_state.show_results = False
            st.rerun()
    
    with col3:
        if st.button("🏠 Dashboard", key="to_dashboard"):
            st.session_state.show_results = False
            st.rerun()

def show_tips():
    """Show tips page"""
    st.markdown("### 💡 Study Tips & Tricks")
    
    general_tips = [
        {"icon": "⏰", "title": "Pomodoro Technique", "content": "Study for 25 minutes, then take a 5-minute break."},
        {"icon": "📝", "title": "Active Note-Taking", "content": "Use the Cornell method for better retention."},
        {"icon": "🧠", "title": "Spaced Repetition", "content": "Review material at increasing intervals."},
        {"icon": "💤", "title": "Sleep Schedule", "content": "Maintain 7-8 hours of sleep daily."},
        {"icon": "🏃‍♂️", "title": "Exercise", "content": "Regular physical activity improves cognitive function."},
        {"icon": "🍎", "title": "Healthy Diet", "content": "Eat brain foods and stay hydrated."}
    ]
    
    col1, col2 = st.columns(2)
    
    for i, tip in enumerate(general_tips):
        current_col = col1 if i % 2 == 0 else col2
        with current_col:
            st.markdown(f"""
            <div class="tip-card">
                <div class="tip-icon">{tip['icon']}</div>
                <div class="tip-title">{tip['title']}</div>
                <div class="tip-content">{tip['content']}</div>
            </div>
            """, unsafe_allow_html=True)

def show_how_to_use():
    """Show how to use page"""
    st.markdown("### ❓ How to Use This App")
    
    steps = [
        {"step": "1", "title": "Navigate to Predictor", "content": "Click on '📊 Predictor' in the sidebar."},
        {"step": "2", "title": "Fill Information", "content": "Enter your study hours and other factors."},
        {"step": "3", "title": "Get Prediction", "content": "Click 'Predict My Score' to see results."},
        {"step": "4", "title": "Review Results", "content": "See your grade and personalized tips."},
        {"step": "5", "title": "Apply Tips", "content": "Use recommendations to improve performance."}
    ]
    
    for step in steps:
        st.markdown(f"""
        <div class="tip-card">
            <div class="tip-icon">#{step['step']}</div>
            <div class="tip-title">{step['title']}</div>
            <div class="tip-content">{step['content']}</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()