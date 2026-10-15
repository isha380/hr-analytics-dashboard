


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score  # ← FIXED: was merged with function def

def prepare_ml_data(df):
    """
    Prepares data for ML model training.
    Handles ALL categorical columns including new ones from messy dataset.
    
    Input: DataFrame with all features
    Output: Feature matrix X, target vector y, and fitted encoders
    """
  
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
  
    for col in numerical_cols:
        if df_processed[col].isnull().any():
            df_processed[col].fillna(df_processed[col].median(), inplace=True)
    
 
    for col in categorical_cols:
        if df_processed[col].isnull().any():
            df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
    
    # One-hot encode ALL categorical columns
    df_encoded = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True)
    
    # Prepare target variable
    y = (df['Attrition'] == 'Yes').astype(int)
    
   
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
        random_state=42,  
        stratify=y  
    )
    
    # Initialize the Random Forest model
    # Adjusted parameters for better sensitivity
    model = RandomForestClassifier(
        n_estimators=100, 
        max_depth=10,  
        min_samples_split=5,  
        min_samples_leaf=2,  
        class_weight='balanced',  
        random_state=42
    )
    
   
    model.fit(X_train, y_train)
    
    
    accuracy = model.score(X_test, y_test)
    
    # Get Cross-Validation accuracy (Tests on 5 different splits)
    cv_scores = cross_val_score(model, X, y, cv=5)
    cv_accuracy = cv_scores.mean()
    
    print(f"Standard Accuracy: {accuracy*100:.1f}%")
    print(f"Cross-Validated Accuracy: {cv_accuracy*100:.1f}%")
    print(f"Attrition distribution in data: {y.value_counts().to_dict()}")
    
    return model, cv_accuracy  