"""
Diversity and Demographics Analytics module.
Identifies gender gaps and age distribution trends across the company.
"""

import pandas as pd

def get_gender_distribution_by_role(df):
    """
    Calculates the count of Male/Female for each Job Role.
    
    Input: DataFrame with 'JobRole' and 'Gender' columns.
    Output: DataFrame with 'JobRole', 'Gender', and 'Count'.
    """
   
    # .size() counts the rows, .reset_index() turns it back into a normal table
    gender_counts = df.groupby(['JobRole', 'Gender']).size().reset_index(name='Count')
    
    return gender_counts

def get_age_stats_by_department(df):
    """
    Calculates age statistics per department to identify aging workforces.
    
    Input: DataFrame with 'Department' and 'Age' columns.
    Output: DataFrame with mean, median, min, and max age per department.
    """

    age_stats = df.groupby('Department')['Age'].agg([
        'mean', 
        'median', 
        'min', 
        'max'
    ]).round(1)
    
    return age_stats