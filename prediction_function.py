
import pandas as pd
import joblib
import numpy as np

def predict_student_score(model, scaler, feature_values, feature_names):
    """
    Predict student score based on input features

    Parameters:
    - model: Trained ML model
    - scaler: Fitted StandardScaler
    - feature_values: List of feature values in the same order as feature_names
    - feature_names: List of feature names

    Returns:
    - Predicted score (float)
    """
    # Create DataFrame with feature values
    input_df = pd.DataFrame([feature_values], columns=feature_names)

    # Scale the features
    input_scaled = scaler.transform(input_df)

    # Make prediction
    prediction = model.predict(input_scaled)[0]

    # Ensure prediction is within reasonable bounds (0-100)
    prediction = max(0, min(100, prediction))

    return round(prediction, 2)

def load_model_and_scaler():
    """Load the saved model and scaler"""
    model = joblib.load('student_score_model.pkl')
    scaler = joblib.load('feature_scaler.pkl')
    return model, scaler
