"""
Compensation and Pay Equity Analytics module.
Analyzes salary fairness and income growth over time.
"""

import pandas as pd

def get_average_pay_by_role_and_gender(df):
    """
    Calculates the average monthly income for each gender within each job role.
    
    Input: DataFrame with 'JobRole', 'Gender', and 'MonthlyIncome'.
    Output: DataFrame with 'JobRole', 'Gender', and average 'MonthlyIncome'.
    """
    pay_stats = df.groupby(['JobRole', 'Gender'])['MonthlyIncome'].mean().round(0).reset_index()
    
    return pay_stats