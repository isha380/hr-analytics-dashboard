"""
Visualization module for HR Analytics.
Creates Plotly charts for dashboard display.
"""

import plotly.express as px
import config  # Import our configuration


def create_department_chart(df):
    """
    Create a bar chart showing employee count by department.
    
    Input: DataFrame with 'Department' column
    Output: Plotly Figure object
    """
    # Count employees in each department
    dept_counts = df['Department'].value_counts()
    
    # Create bar chart
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


def create_all_charts(df):
    """
    Master function that creates all charts at once.
    Returns a dictionary of chart names -> figure objects.
    
    Why this function?
    Makes it easy to generate all charts with one call.
    Useful for batch processing or PDF reports.
    """
    charts = {
        "department": create_department_chart(df),
        "age": create_age_histogram(df),
        "attrition": create_attrition_pie_chart(df)
    }
    
    return charts