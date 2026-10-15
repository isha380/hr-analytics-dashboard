"""
Visualization module for HR Analytics.
Creates Plotly charts for dashboard display.
"""

import plotly.express as px
import config 


def create_department_chart(df):
    """
    Create a bar chart showing employee count by department.
    
    Input: DataFrame with 'Department' column
    Output: Plotly Figure object
    """
   
    dept_counts = df['Department'].value_counts()
    
   
    fig = px.bar(
        x=dept_counts.index,
        y=dept_counts.values,
        title="Employees by Department",
        labels={'x': 'Department', 'y': 'Number of Employees'},
        color=dept_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Remove legend for cleaner look
    fig.update_layout(showlegend=False)
    
    return fig


def create_age_histogram(df):
    """
    Create a histogram showing age distribution of employees.
    
    Why histogram?
    Shows the frequency distribution of a continuous variable (age).
    Helps identify if workforce is young, old, or balanced.
    """
    fig = px.histogram(
        df,
        x='Age',
        nbins=20,  # Number of bars
        title="Employee Age Distribution",
        color_discrete_sequence=[config.COLOR_PALETTE['primary']]
    )
    
    return fig


def create_attrition_pie_chart(df):
    """
    Create a pie chart showing attrition rate.
    
    Why pie chart?
    Shows proportion of a whole (Yes vs No attrition).
    Good for binary categories.
    """
    attrition_counts = df['Attrition'].value_counts()
    
    # Use red for "Yes" (bad), green for "No" (good)
    color_map = {'Yes': config.COLOR_PALETTE['danger'], 
                 'No': config.COLOR_PALETTE['success']}
    
    fig = px.pie(
        values=attrition_counts.values,
        names=attrition_counts.index,
        title="Attrition Rate (Yes vs No)",
        color=attrition_counts.index,
        color_discrete_map=color_map
    )
    
    return fig



def create_correlation_heatmap(df):
    """
    
    Why a heatmap?
    It visually highlights strong positive (blue) or negative (red) relationships
    between variables, helping HR identify hidden patterns (e.g., Age vs Income).
    """
    # 1. Select only numeric columns
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    # 2. Calculate the correlation matrix
    # A value of 1.0 means perfect positive correlation, -1.0 is perfect negative
    corr_matrix = numeric_df.corr()
    
    # 3. Create the Plotly heatmap
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",  # Shows the correlation number inside each box
        title="Feature Correlation Heatmap",
        color_continuous_scale='RdBu_r', 
        aspect="auto"
    )
    
 
    fig.update_layout(height=600)
    
    return fig

def create_all_charts(df):
    
    charts = {
        "department": create_department_chart(df),
        "age": create_age_histogram(df),
        "attrition": create_attrition_pie_chart(df)
    }
    
    return charts