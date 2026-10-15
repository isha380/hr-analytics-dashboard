
"""
Data cleaning module for HR Analytics.
Handles data validation, duplicate removal, missing value handling, and case normalization.
"""

import pandas as pd
import numpy as np

def validate_required_columns(df):
    """
    Check if the uploaded dataframe has the minimum required columns.
    Fails fast if critical data is missing.
    """
    required_columns = ['Age', 'Department', 'Attrition']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}. Please upload a valid HR dataset.")
    
    return True

def load_and_clean_data(uploaded_file):
    """
    Main function to load CSV and apply all cleaning steps.
    """
    df = pd.read_csv(uploaded_file)
    original_rows = len(df)

    validate_required_columns(df)
    
    
    df_clean = df.drop_duplicates()
    duplicates_removed = original_rows - len(df_clean)
    
    # Fix case inconsistencies and whitespace
    issues_fixed = 0
    
    
    if 'Gender' in df_clean.columns:
        original_gender = df_clean['Gender'].copy()
        df_clean['Gender'] = df_clean['Gender'].astype(str).str.strip().str.title()
        # Count rows that changed
        issues_fixed += (original_gender.astype(str).str.strip().str.title() != df_clean['Gender']).sum()
    
   
    if 'Department' in df_clean.columns:
        original_dept = df_clean['Department'].copy()
        df_clean['Department'] = df_clean['Department'].astype(str).str.strip().str.title()
        issues_fixed += (original_dept.astype(str).str.strip().str.title() != df_clean['Department']).sum()
    
   
    if 'JobRole' in df_clean.columns:
        original_role = df_clean['JobRole'].copy()
        df_clean['JobRole'] = df_clean['JobRole'].astype(str).str.strip().str.title()
        issues_fixed += (original_role.astype(str).str.strip().str.title() != df_clean['JobRole']).sum()
    
    # Handle missing values
    missing_before = df_clean.isnull().sum().sum()
    df_clean = fill_missing_values(df_clean)
    missing_after = df_clean.isnull().sum().sum()
    missing_filled = missing_before - missing_after
    
   
    total_issues_fixed = issues_fixed + missing_filled
    
   
    cleaning_summary = {
        "original_rows": original_rows,
        "final_rows": len(df_clean),
        "duplicates_removed": duplicates_removed,
        "missing_values_filled": total_issues_fixed,  # Now includes case fixes
        "columns": list(df_clean.columns)
    }
    
    return df_clean, cleaning_summary


def fill_missing_values(df):
    """
    Fill missing values based on data type.
    - Numeric columns: fill with median 
    - Categorical columns: fill with mode 
    """
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Fill numeric columns with median
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_value = df[col].median()
            df[col].fillna(median_value, inplace=True)
   
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_value = df[col].mode()
            if len(mode_value) > 0:
                df[col].fillna(mode_value[0], inplace=True)
            else:
                df[col].fillna('Unknown', inplace=True)
    
    return df