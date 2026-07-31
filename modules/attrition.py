"""
Machine Learning module for predicting Employee Attrition.
Uses Random Forest to classify employees as 'Flight Risk' or 'Safe'.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def prepare_ml_data(df):
    """
    Prepares the dataframe for machine learning by encoding text into numbers.
    
    Input: Cleaned pandas DataFrame
    Output: Tuple (features_matrix, target_vector, label_encoder_object)
    """
  
    ml_data = df.copy()
    
    # 1. Encode the Target Variable (What we want to predict: Attrition)
    # We use LabelEncoder to turn 'No' -> 0 and 'Yes' -> 1
    target_encoder = LabelEncoder()
    ml_data['Attrition_Encoded'] = target_encoder.fit_transform(ml_data['Attrition'])
    
    # 2. Encode Categorical Features (Text columns that aren't the target)
    # We use pd.get_dummies() to create binary columns (e.g., Department_Sales = 1, Department_R&D = 0)
    categorical_cols = ['Gender', 'Department', 'JobRole', 'OverTime']
    ml_data = pd.get_dummies(ml_data, columns=categorical_cols, drop_first=True)
    
    # 3. Separate Features (X) and Target (y)
    # Drop the original text 'Attrition' and the new encoded target from features
    features_to_drop = ['Attrition', 'Attrition_Encoded']
    X = ml_data.drop(columns=features_to_drop)
    y = ml_data['Attrition_Encoded']
    
    return X, y, target_encoder

def train_attrition_model(X, y):
    """
    Trains a Random Forest model to predict attrition.
    
    Input: Features (X) and Target (y)
    Output: Tuple (trained_model, accuracy_score)
    """
    # Split data: 80% for training the model, 20% for testing its accuracy
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42 # Ensures we get the same split every time we run it
    )
    
    # Initialize the Random Forest model
    # n_estimators=100 means we are building 100 decision trees and averaging them
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model on the training data
    model.fit(X_train, y_train)
    
    # Test the model and calculate accuracy
    accuracy = model.score(X_test, y_test)
    
    return model, accuracy