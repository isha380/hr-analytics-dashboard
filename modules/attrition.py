# """
# Machine Learning module for predicting Employee Attrition.
# Uses Random Forest to classify employees as 'Flight Risk' or 'Safe'.
# """

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
# def prepare_ml_data(df):
#     """
#     Prepares the dataframe for machine learning by encoding text into numbers.
    
#     Input: Cleaned pandas DataFrame
#     Output: Tuple (features_matrix, target_vector, label_encoder_object)
#     """
  
#     ml_data = df.copy()
    
#     # 1. Encode the Target Variable (What we want to predict: Attrition)
#     # We use LabelEncoder to turn 'No' -> 0 and 'Yes' -> 1
#     target_encoder = LabelEncoder()
#     ml_data['Attrition_Encoded'] = target_encoder.fit_transform(ml_data['Attrition'])
    
#     # 2. Encode Categorical Features (Text columns that aren't the target)
#     # We use pd.get_dummies() to create binary columns (e.g., Department_Sales = 1, Department_R&D = 0)
#     categorical_cols = ['Gender', 'Department', 'JobRole', 'OverTime']
#     ml_data = pd.get_dummies(ml_data, columns=categorical_cols, drop_first=True)
    
#     # 3. Separate Features (X) and Target (y)
#     # Drop the original text 'Attrition' and the new encoded target from features
#     features_to_drop = ['Attrition', 'Attrition_Encoded']
#     X = ml_data.drop(columns=features_to_drop)
#     y = ml_data['Attrition_Encoded']
    
#     return X, y, target_encoder

# def train_attrition_model(X, y):
#     """
#     Trains a Random Forest model to predict attrition.
    
#     Input: Features (X) and Target (y)
#     Output: Tuple (trained_model, accuracy_score)
#     """
#     # Split data: 80% for training the model, 20% for testing its accuracy
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, 
#         test_size=0.2, 
#         random_state=42 # Ensures we get the same split every time we run it
#     )
    
#     # Initialize the Random Forest model
#     # n_estimators=100 means we are building 100 decision trees and averaging them
#     model = RandomForestClassifier(n_estimators=100, random_state=42)
    
#     # Train the model on the training data
#     model.fit(X_train, y_train)
    
#     # Test the model and calculate accuracy
#     accuracy = model.score(X_test, y_test)
    
#     return model, accuracy

# def prepare_ml_data(df):
#     """
#     Prepares the dataframe for machine learning by encoding text into numbers.
#     Drops columns that are not suitable for ML (like text feedback).
#     """
#     # Create a copy so we don't accidentally modify the original dashboard data
#     ml_data = df.copy()
    
#     # REMOVE columns that ML can't use (text feedback, IDs, etc.)
#     columns_to_drop = ['Feedback', 'Sentiment_Score', 'Sentiment_Category', 'Flight_Risk_Score', 'Risk_Category']
#     for col in columns_to_drop:
#         if col in ml_data.columns:
#             ml_data = ml_data.drop(columns=[col])
    
#     # 1. Encode the Target Variable (What we want to predict: Attrition)
#     target_encoder = LabelEncoder()
#     ml_data['Attrition_Encoded'] = target_encoder.fit_transform(ml_data['Attrition'])
    
#     # 2. Encode Categorical Features (Text columns that aren't the target)
#     categorical_cols = ['Gender', 'Department', 'JobRole', 'OverTime']
#     # Only encode columns that actually exist
#     categorical_cols = [col for col in categorical_cols if col in ml_data.columns]
#     ml_data = pd.get_dummies(ml_data, columns=categorical_cols, drop_first=True)
    
#     # 3. Separate Features (X) and Target (y)
#     features_to_drop = ['Attrition', 'Attrition_Encoded']
#     X = ml_data.drop(columns=features_to_drop)
#     y = ml_data['Attrition_Encoded']
    
#     return X, y, target_encoder

def prepare_ml_data(df):
    """
    Prepares data for ML model training.
    Handles ALL categorical columns including new ones from messy dataset.
    
    Input: DataFrame with all features
    Output: Feature matrix X, target vector y, and fitted encoders
    """
    # Make a copy to avoid modifying original data
    df_processed = df.copy()
    
    # Drop non-predictive columns
    columns_to_drop = ['Feedback', 'Attrition']
    existing_cols_to_drop = [col for col in columns_to_drop if col in df_processed.columns]
    df_processed = df_processed.drop(columns=existing_cols_to_drop)
    
    # Identify categorical and numerical columns
    categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df_processed.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    print(f"📊 Categorical columns to encode: {categorical_cols}")
    print(f"📊 Numerical columns: {numerical_cols}")
    
    # Handle missing values
    # Fill numerical with median
    for col in numerical_cols:
        if df_processed[col].isnull().any():
            df_processed[col].fillna(df_processed[col].median(), inplace=True)
    
    # Fill categorical with mode
    for col in categorical_cols:
        if df_processed[col].isnull().any():
            df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
    
    # One-hot encode ALL categorical columns
    df_encoded = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True)
    
    # Prepare target variable
    y = (df['Attrition'] == 'Yes').astype(int)
    
    # Features
    X = df_encoded
    
    print(f"✅ Final feature matrix shape: {X.shape}")
    print(f"✅ Target variable shape: {y.shape}")
    
    return X, y, None  # Return None for encoder since we're using get_dummies

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
    model = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=10,min_samples_leaf=5, random_state=42)
    
    # Train the model on the training data
    model.fit(X_train, y_train)
    
    # Test the model and calculate accuracy
    accuracy = model.score(X_test, y_test)
    # Get Cross-Validation accuracy (Tests on 5 different splits)
    cv_scores = cross_val_score(model, X, y, cv=5)
    cv_accuracy = cv_scores.mean()
    print(f"Standard Accuracy: {accuracy*100:.1f}%")
    print(f"Cross-Validated Accuracy: {cv_accuracy*100:.1f}%") # This is the TRUE accuracy

    
    return model, cv_accuracy