"""
Leave and Absenteeism Analytics module.
Calculates department trends and identifies at-risk employees.
"""

import pandas as pd

def calculate_department_leave_stats(df):
    """
    Groups data by department to find average leave and absenteeism.
    
    Input: DataFrame with 'Department', 'AnnualLeaveTaken', 'SickLeaveTaken', 'AbsenteeismRate'
    Output: DataFrame containing aggregated statistics per department
    """
   
    stats = df.groupby('Department').agg({
        'AnnualLeaveTaken': 'mean',
        'SickLeaveTaken': 'mean',
        'AbsenteeismRate': 'mean'
    }).round(2)
    
    # Sort by absenteeism rate to see the worst departments first
    stats = stats.sort_values(by='AbsenteeismRate', ascending=False)
    
    return stats

def get_top_absentees(df, top_n=5):
    """
    Identifies the specific employees with the highest absenteeism rates.
    Useful for HR to schedule wellness check-ins.
    
    Input: DataFrame with employee details and 'AbsenteeismRate'
    Output: DataFrame of the top N absentees
    """
    # Sort the entire dataframe by absenteeism rate, highest first
    top_absentees = df.sort_values(by='AbsenteeismRate', ascending=False)
    
    # Select only the columns HR needs to see for a check-in
    columns_to_show = ['JobRole', 'Department', 'OverTime', 'SickLeaveTaken', 'AnnualLeaveTaken', 'AbsenteeismRate', 'Attrition']
    
    # Return the top N rows
    return top_absentees[columns_to_show].head(top_n)