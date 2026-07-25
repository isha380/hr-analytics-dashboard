"""
Data cleaning module for HR Analytics.
Handles data validation, duplicate removal, and missing value handling.
"""

import pandas as pd
import numpy as np


def load_and_clean_data(uploaded_file):
    """
    Main function to load CSV and apply all cleaning steps.
    
    Input: uploaded_file (Streamlit UploadedFile object)
    Output: tuple (cleaned_dataframe, cleaning_summary_dict)
    """
    # Load the raw data
    df = pd.read_csv(uploaded_file)
    original_rows = len(df)
    
    # Step 1: Remove duplicates
    df_clean = df.drop_duplicates()
    duplicates_removed = original_rows - len(df_clean)
    
    # Step 2: Handle missing values
    missing_before = df_clean.isnull().sum().sum()
    df_clean = fill_missing_values(df_clean)
    missing_after = df_clean.isnull().sum().sum()
    missing_filled = missing_before - missing_after
    
    # Create summary report
    cleaning_summary = {
        "original_rows": original_rows,
        "final_rows": len(df_clean),
        "duplicates_removed": duplicates_removed,
        "missing_values_filled": missing_filled,
        "columns": list(df_clean.columns)
    }
    
    return df_clean, cleaning_summary


def fill_missing_values(df):
    """
    Fill missing values based on data type.
    - Numeric columns: fill with median (middle value)
    - Text columns: fill with 'Unknown'
    
    Why median instead of mean?
    Median is resistant to outliers. Example:
    Ages: [25, 30, 35, 40, 80] 
    Mean = 42 (skewed by 80)
    Median = 35 (more representative)
    """
    # Get numeric and text columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    # Fill numeric columns with median
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_value = df[col].median()
            df[col].fillna(median_value, inplace=True)
    
    # Fill text columns with 'Unknown'
    for col in text_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna('Unknown', inplace=True)
    
    return df


def validate_required_columns(df, required_columns):
    """
    Check if all required columns exist in the dataframe.
    Raises an error if any are missing.
    
    Why use assertions?
    Fail fast! Better to crash early with a clear message
    than produce wrong results silently.
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    return True