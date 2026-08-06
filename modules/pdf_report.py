"""
Professional PDF Report Generation module for HR Analytics.
Uses ReportLab to create executive-ready reports with embedded charts.
"""

import os
import tempfile
from datetime import datetime
import pandas as pd
import plotly.io as pio

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate


# ==========================================
# COLOR CONSTANTS
# ==========================================
PRIMARY_COLOR = HexColor('#1e3a8a')
SECONDARY_COLOR = HexColor('#3b82f6')
ACCENT_COLOR = HexColor('#10b981')
WARNING_COLOR = HexColor('#ef4444')
NEUTRAL_COLOR = HexColor('#6b7280')
BG_LIGHT = HexColor('#f8f9fa')

PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT_MARGIN = 1.5 * inch
RIGHT_MARGIN = 1.5 * inch
TOP_MARGIN = 1.2 * inch
BOTTOM_MARGIN = 1.2 * inch


# ==========================================
# STYLES - Simple Dictionary Approach
# ==========================================
def get_styles():
    """Return a simple dictionary of styles."""
    base = getSampleStyleSheet()
    
    return {
        'Title': base['Title'],
        'Heading1': base['Heading1'],
        'Heading2': base['Heading2'],
        'Normal': base['Normal'],
        'BodyText': base['BodyText'],
    }
# ==========================================
# CHART EXPORT UTILITY
# ==========================================
def export_plotly_chart(fig, filename, width=800, height=500):
    """
    Export a Plotly figure as a high-resolution PNG image.
    Returns the file path of the saved image.
    """
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, filename)
    
    fig.write_image(
        filepath, 
        width=width, 
        height=height, 
        scale=2,  # 2x resolution for crisp printing
        engine='kaleido'
    )
    return filepath


# ==========================================
# PAGE TEMPLATE (Header & Footer)
# ==========================================
def header_footer(canvas, doc):
    """Add header and footer to every page."""
    canvas.saveState()
    
    # Header line
    canvas.setStrokeColor(PRIMARY_COLOR)
    canvas.setLineWidth(1)
    canvas.line(LEFT_MARGIN, PAGE_HEIGHT - 0.8*inch, PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 0.8*inch)
    
    # Footer line
    canvas.line(LEFT_MARGIN, 0.7*inch, PAGE_WIDTH - RIGHT_MARGIN, 0.7*inch)
    
    # Footer text
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(NEUTRAL_COLOR)
    canvas.drawString(LEFT_MARGIN, 0.5*inch, "HR Analytics Dashboard - Confidential")
    canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 0.5*inch, f"Page {doc.page}")
    canvas.drawCentredString(PAGE_WIDTH / 2, 0.5*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    canvas.restoreState()


# ==========================================
# SECTION 1: COVER PAGE
# ==========================================
def build_cover_page(df, filename, styles):
    """Build the cover page elements."""
    elements = []
    
    # Add spacers to center content vertically
    elements.append(Spacer(1, 2.5 * inch))
    
    elements.append(Paragraph("HR Analytics Report", styles['CoverTitle']))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("Executive Summary & AI Insights", styles['CoverSubtitle']))
    elements.append(Spacer(1, 1 * inch))
    
    # Cover info table
    cover_data = [
        ['Report Generated:', datetime.now().strftime('%B %d, %Y at %H:%M')],
        ['Source File:', os.path.basename(filename) if filename else 'Uploaded Dataset'],
        ['Total Employees:', str(len(df))],
        ['Dashboard Version:', '1.0.0'],
    ]
    
    cover_table = Table(cover_data, colWidths=[2.5*inch, 3.5*inch])
    cover_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 11),
        ('TEXTCOLOR', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (1, 0), (1, -1), black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(cover_table)
    elements.append(PageBreak())
    return elements


# ==========================================
# SECTION 2: EXECUTIVE SUMMARY
# ==========================================
def build_executive_summary(df, styles, model_accuracy=None):
    """Build KPI cards for executive summary."""
    elements = []
    elements.append(Paragraph("1. Executive Summary", styles['SectionHeader']))
    elements.append(Paragraph(
        "This report provides a comprehensive analysis of your workforce data, "
        "including attrition predictions, sentiment analysis, and compensation insights.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Calculate KPIs
    total_employees = len(df)
    avg_age = df['Age'].mean() if 'Age' in df.columns else 0
    num_departments = df['Department'].nunique() if 'Department' in df.columns else 0
    
    high_risk = len(df[df.get('Risk_Category', pd.Series()) == 'High Risk']) if 'Risk_Category' in df.columns else 0
    avg_sentiment = df['Sentiment_Score'].mean() if 'Sentiment_Score' in df.columns else 0
    
    # KPI Grid (3 columns)
    kpi_data = [
        ['Total Employees', 'Avg Age', 'Departments'],
        [str(total_employees), f"{avg_age:.1f}", str(num_departments)],
        ['High Risk Employees', 'Model Accuracy', 'Avg Sentiment'],
        [str(high_risk), f"{model_accuracy*100:.1f}%" if model_accuracy else 'N/A', f"{avg_sentiment:.2f}"],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
    kpi_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica', 9),
        ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 16),
        ('FONT', (0, 2), (-1, 2), 'Helvetica', 9),
        ('FONT', (0, 3), (-1, 3), 'Helvetica-Bold', 16),
        ('TEXTCOLOR', (0, 0), (-1, 0), NEUTRAL_COLOR),
        ('TEXTCOLOR', (0, 1), (-1, 1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 2), (-1, 2), NEUTRAL_COLOR),
        ('TEXTCOLOR', (0, 3), (-1, 3), PRIMARY_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb')),
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(kpi_table)
    return elements


# ==========================================
# SECTION 3: DATA CLEANING SUMMARY
# ==========================================
def build_data_cleaning_summary(df, styles, cleaning_summary=None):
    """Build data cleaning summary table."""
    elements = []
    elements.append(Paragraph("2. Data Cleaning Summary", styles['SectionHeader']))
    
    if cleaning_summary:
        data = [
            ['Metric', 'Value'],
            ['Original Rows', str(cleaning_summary.get('original_rows', len(df)))],
            ['Final Rows', str(cleaning_summary.get('final_rows', len(df)))],
            ['Duplicates Removed', str(cleaning_summary.get('duplicates_removed', 0))],
            ['Missing Values Filled', str(cleaning_summary.get('missing_values_filled', 0))],
            ['Columns Processed', str(len(cleaning_summary.get('columns', df.columns)))],
        ]
    else:
        data = [
            ['Metric', 'Value'],
            ['Total Rows', str(len(df))],
            ['Columns', str(len(df.columns))],
        ]
    
    table = Table(data, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, -1), black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(table)
    return elements


# ==========================================
# SECTION 4: ATTRITION PREDICTION
# ==========================================
def build_attrition_report(df, styles, model_accuracy=None, temp_dir=None):
    """Build attrition prediction section with chart."""
    elements = []
    elements.append(Paragraph("3. Attrition Prediction Report", styles['Heading2']))
    
    if 'Risk_Category' not in df.columns:
        elements.append(Paragraph("ML prediction data not available.", styles['BodyText2']))
        return elements
    
    # Risk category counts
    risk_counts = df['Risk_Category'].value_counts()
    high = risk_counts.get('High Risk', 0)
    medium = risk_counts.get('Medium Risk', 0)
    low = risk_counts.get('Low Risk', 0)
    
    elements.append(Paragraph(f"<b>Model Accuracy:</b> {model_accuracy*100:.1f}%" if model_accuracy else "<b>Model Accuracy:</b> N/A", styles['BodyText2']))
    elements.append(Spacer(1, 0.15 * inch))
    
    # Risk distribution table
    risk_data = [
        ['Risk Category', 'Employee Count', 'Percentage'],
        ['High Risk', str(high), f"{(high/len(df)*100):.1f}%"],
        ['Medium Risk', str(medium), f"{(medium/len(df)*100):.1f}%"],
        ['Low Risk', str(low), f"{(low/len(df)*100):.1f}%"],
    ]
    
    risk_table = Table(risk_data, colWidths=[2.5*inch, 2*inch, 2*inch])
    risk_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (0, 1), WARNING_COLOR),
        ('TEXTCOLOR', (0, 2), (0, 2), HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 3), (0, 3), ACCENT_COLOR),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#d1d5db')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(risk_table)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("<b>Figure 1:</b> Attrition Distribution", styles['Heading1']))
    
    # Embed attrition chart if available
    if temp_dir and 'Attrition' in df.columns:
        import plotly.express as px
        attrition_counts = df['Attrition'].value_counts()
        fig = px.pie(
            values=attrition_counts.values,
            names=attrition_counts.index,
            title="Attrition Distribution",
            color_discrete_map={'No': '#10b981', 'Yes': '#ef4444'}
        )
        chart_path = export_plotly_chart(fig, 'attrition_chart.png', width=700, height=400)
        elements.append(Image(chart_path, width=6*inch, height=3.5*inch))
    
    return elements


# ==========================================
# SECTION 5: SENTIMENT ANALYSIS
# ==========================================
def build_sentiment_report(df, styles, temp_dir=None):
    """Build sentiment analysis section."""
    elements = []
    elements.append(Paragraph("4. Employee Sentiment Analysis", styles['SectionHeader']))
    
    if 'Sentiment_Category' not in df.columns:
        elements.append(Paragraph("Sentiment analysis data not available.", styles['BodyText2']))
        return elements
    
    avg_sentiment = df['Sentiment_Score'].mean()
    positive = len(df[df['Sentiment_Category'] == 'Positive'])
    neutral = len(df[df['Sentiment_Category'] == 'Neutral'])
    negative = len(df[df['Sentiment_Category'] == 'Negative'])
    
    elements.append(Paragraph(f"<b>Average Sentiment Score:</b> {avg_sentiment:.2f}", styles['BodyText2']))
    elements.append(Spacer(1, 0.15 * inch))
    
    sentiment_data = [
        ['Category', 'Count', 'Percentage'],
        ['Positive', str(positive), f"{(positive/len(df)*100):.1f}%"],
        ['Neutral', str(neutral), f"{(neutral/len(df)*100):.1f}%"],
        ['Negative', str(negative), f"{(negative/len(df)*100):.1f}%"],
    ]
    
    sent_table = Table(sentiment_data, colWidths=[2.5*inch, 2*inch, 2*inch])
    sent_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (0, 1), ACCENT_COLOR),
        ('TEXTCOLOR', (0, 2), (0, 2), HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 3), (0, 3), WARNING_COLOR),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#d1d5db')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(sent_table)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("<b>Figure 2:</b> Sentiment Distribution", styles['SubHeader']))
    
    if temp_dir:
        import plotly.express as px
        sent_counts = df['Sentiment_Category'].value_counts()
        fig = px.pie(
            values=sent_counts.values,
            names=sent_counts.index,
            title="Sentiment Distribution",
            color_discrete_map={'Positive': '#10b981', 'Neutral': '#f59e0b', 'Negative': '#ef4444'}
        )
        chart_path = export_plotly_chart(fig, 'sentiment_chart.png', width=700, height=400)
        elements.append(Image(chart_path, width=6*inch, height=3.5*inch))
    
    return elements


# ==========================================
# SECTION 6: LEAVE & ABSENTEEISM
# ==========================================
def build_leave_report(df, styles, temp_dir=None):
    """Build leave and absenteeism section."""
    elements = []
    elements.append(Paragraph("5. Leave & Absenteeism Analytics", styles['SectionHeader']))
    
    if 'AbsenteeismRate' not in df.columns:
        elements.append(Paragraph("Leave data not available.", styles['BodyText2']))
        return elements
    
    avg_sick = df['SickLeaveTaken'].mean()
    avg_annual = df['AnnualLeaveTaken'].mean()
    high_absenteeism = len(df[df['AbsenteeismRate'] > 5])
    
    elements.append(Paragraph(f"<b>Average Sick Days:</b> {avg_sick:.1f} | <b>Average Vacation Days:</b> {avg_annual:.1f}", styles['BodyText2']))
    elements.append(Paragraph(f"<b>Employees with High Absenteeism (>5%):</b> {high_absenteeism}", styles['BodyText2']))
    elements.append(Spacer(1, 0.15 * inch))
    
    if temp_dir and 'Department' in df.columns:
        import plotly.express as px
        dept_stats = df.groupby('Department')['AbsenteeismRate'].mean().reset_index()
        fig = px.bar(
            dept_stats,
            x='Department',
            y='AbsenteeismRate',
            title="Absenteeism Rate by Department",
            color='AbsenteeismRate',
            color_continuous_scale='Reds'
        )
        chart_path = export_plotly_chart(fig, 'leave_chart.png', width=700, height=400)
        elements.append(Image(chart_path, width=6*inch, height=3.5*inch))
    
    return elements


# ==========================================
# SECTION 7: DIVERSITY & DEMOGRAPHICS
# ==========================================
def build_diversity_report(df, styles, temp_dir=None):
    """Build diversity and demographics section."""
    elements = []
    elements.append(Paragraph("6. Diversity & Demographics", styles['Heading1']))
    
    if 'Gender' not in df.columns:
        elements.append(Paragraph("Diversity data not available.", styles['BodyText2']))
        return elements
    
    # Gender distribution
    gender_counts = df['Gender'].value_counts()
    elements.append(Paragraph(f"<b>Gender Distribution:</b> Male: {gender_counts.get('Male', 0)} | Female: {gender_counts.get('Female', 0)}", styles['BodyText2']))
    
    if 'Department' in df.columns:
        dept_counts = df['Department'].value_counts()
        elements.append(Paragraph(f"<b>Department Distribution:</b> {', '.join([f'{k}: {v}' for k, v in dept_counts.items()])}", styles['BodyText2']))
    
    if 'Age' in df.columns:
        elements.append(Paragraph(f"<b>Age Statistics:</b> Mean: {df['Age'].mean():.1f} | Median: {df['Age'].median():.1f} | Range: {df['Age'].min()}-{df['Age'].max()}", styles['BodyText2']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    if temp_dir:
        import plotly.express as px
        # Gender by role chart
        gender_role = df.groupby(['JobRole', 'Gender']).size().reset_index(name='Count')
        fig = px.bar(
            gender_role,
            x='JobRole',
            y='Count',
            color='Gender',
            barmode='stack',
            title="Gender Distribution by Job Role",
            color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'}
        )
        chart_path = export_plotly_chart(fig, 'diversity_chart.png', width=700, height=400)
        elements.append(Paragraph("<b>Figure 3:</b> Gender Distribution by Role", styles['SubHeader']))
        elements.append(Image(chart_path, width=6*inch, height=3.5*inch))
    
    return elements


# ==========================================
# SECTION 8: COMPENSATION ANALYSIS
# ==========================================
def build_compensation_report(df, styles, temp_dir=None):
    """Build compensation analysis section."""
    elements = []
    elements.append(Paragraph("7. Compensation Analysis", styles['SectionHeader']))
    
    if 'MonthlyIncome' not in df.columns:
        elements.append(Paragraph("Compensation data not available.", styles['BodyText2']))
        return elements
    
    avg_salary = df['MonthlyIncome'].mean()
    max_salary = df['MonthlyIncome'].max()
    min_salary = df['MonthlyIncome'].min()
    
    elements.append(Paragraph(f"<b>Average Monthly Income:</b> ${avg_salary:,.0f}", styles['BodyText2']))
    elements.append(Paragraph(f"<b>Highest Salary:</b> ${max_salary:,.0f} | <b>Lowest Salary:</b> ${min_salary:,.0f}", styles['BodyText2']))
    elements.append(Spacer(1, 0.15 * inch))
    
    # Pay equity observation
    if 'Gender' in df.columns and 'JobRole' in df.columns:
        pay_by_role_gender = df.groupby(['JobRole', 'Gender'])['MonthlyIncome'].mean().unstack()
        elements.append(Paragraph("<b>Pay Equity Observations:</b>", styles['SubHeader']))
        for role in pay_by_role_gender.index:
            male_pay = pay_by_role_gender.loc[role].get('Male', 0)
            female_pay = pay_by_role_gender.loc[role].get('Female', 0)
            if male_pay > 0 and female_pay > 0:
                gap = ((male_pay - female_pay) / male_pay) * 100
                elements.append(Paragraph(f"• {role}: Male ${male_pay:,.0f} | Female ${female_pay:,.0f} (Gap: {gap:.1f}%)", styles['BulletPoint']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    if temp_dir:
        import plotly.express as px
        pay_data = df.groupby(['JobRole', 'Gender'])['MonthlyIncome'].mean().reset_index()
        fig = px.bar(
            pay_data,
            x='JobRole',
            y='MonthlyIncome',
            color='Gender',
            barmode='group',
            title="Average Monthly Income by Gender",
            color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'}
        )
        chart_path = export_plotly_chart(fig, 'compensation_chart.png', width=700, height=400)
        elements.append(Paragraph("<b>Figure 4:</b> Gender Pay Gap by Role", styles['SubHeader']))
        elements.append(Image(chart_path, width=6*inch, height=3.5*inch))
    
    return elements


# ==========================================
# SECTION 9: CORRELATION ANALYSIS
# ==========================================
def build_correlation_report(df, styles, temp_dir=None):
    """Build correlation analysis section with interpretation."""
    elements = []
    elements.append(Paragraph("8. Correlation Analysis", styles['SectionHeader']))
    
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    if len(numeric_df.columns) < 2:
        elements.append(Paragraph("Insufficient numeric data for correlation analysis.", styles['BodyText2']))
        return elements
    
    corr_matrix = numeric_df.corr()
    
    elements.append(Paragraph(
        "The heatmap below shows the correlation between all numeric features. "
        "Values range from -1 (strong negative) to +1 (strong positive).",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.2 * inch))
    
    if temp_dir:
        import plotly.express as px
        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            title="Feature Correlation Heatmap",
            color_continuous_scale='RdBu_r',
            aspect="auto"
        )
        chart_path = export_plotly_chart(fig, 'correlation_chart.png', width=800, height=600)
        elements.append(Image(chart_path, width=6.5*inch, height=4.5*inch))
    
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("<b>Key Correlations:</b>", styles['SubHeader']))
    
    # Find strongest correlations (excluding self-correlations)
    import numpy as np
    np.fill_diagonal(corr_matrix.values, 0)
    
    # Strongest positive
    max_corr = corr_matrix.unstack().sort_values(ascending=False)
    max_corr = max_corr[max_corr < 1.0]  # Remove self-correlations
    
    if len(max_corr) > 0:
        strongest_pos = max_corr.index[0]
        elements.append(Paragraph(
            f"• <b>Strongest Positive Correlation:</b> {strongest_pos[0]} and {strongest_pos[1]} ({max_corr.iloc[0]:.2f})",
            styles['BulletPoint']
        ))
        
        strongest_neg = max_corr.index[-1]
        elements.append(Paragraph(
            f"• <b>Strongest Negative Correlation:</b> {strongest_neg[0]} and {strongest_neg[1]} ({max_corr.iloc[-1]:.2f})",
            styles['BulletPoint']
        ))
    
    return elements


# ==========================================
# SECTION 10: AI INSIGHTS
# ==========================================
def generate_ai_insights(df, styles):
    """Generate data-driven business insights."""
    elements = []
    elements.append(Paragraph("9. Key AI Insights", styles['SectionHeader']))
    elements.append(Paragraph(
        "The following insights are automatically generated from your workforce data:",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.1 * inch))
    
    insights = []
    
    # Attrition insight
    if 'Attrition' in df.columns:
        attrition_rate = (df['Attrition'] == 'Yes').mean() * 100
        insights.append(f"• Overall attrition rate is {attrition_rate:.1f}%, indicating {'high' if attrition_rate > 15 else 'moderate' if attrition_rate > 10 else 'low'} turnover.")
        
        if 'Department' in df.columns:
            dept_attrition = df[df['Attrition'] == 'Yes']['Department'].value_counts()
            if len(dept_attrition) > 0:
                insights.append(f"• {dept_attrition.index[0]} department has the highest number of resignations ({dept_attrition.iloc[0]} employees).")
    
    # Flight risk insight
    if 'Risk_Category' in df.columns:
        high_risk = len(df[df['Risk_Category'] == 'High Risk'])
        insights.append(f"• {high_risk} employees are identified as high flight risk (>70% probability of leaving).")
    
    # Sentiment insight
    if 'Sentiment_Category' in df.columns:
        positive_pct = (df['Sentiment_Category'] == 'Positive').mean() * 100
        insights.append(f"• {positive_pct:.1f}% of employee feedback is positive, suggesting {'strong' if positive_pct > 70 else 'moderate' if positive_pct > 50 else 'concerning'} morale.")
    
    # Compensation insight
    if 'MonthlyIncome' in df.columns and 'Gender' in df.columns:
        avg_pay = df.groupby('Gender')['MonthlyIncome'].mean()
        if 'Male' in avg_pay.index and 'Female' in avg_pay.index:
            gap = ((avg_pay['Male'] - avg_pay['Female']) / avg_pay['Male']) * 100
            insights.append(f"• Gender pay gap is {abs(gap):.1f}%, with {'males' if gap > 0 else 'females'} earning more on average.")
    
    # Leave insight
    if 'AbsenteeismRate' in df.columns:
        high_absenteeism = len(df[df['AbsenteeismRate'] > 5])
        insights.append(f"• {high_absenteeism} employees show high absenteeism rates (>5%), which may indicate burnout.")
    
    # Add insights to document
    for insight in insights[:8]:  # Limit to 8 insights
        elements.append(Paragraph(insight, styles['BulletPoint']))
    
    return elements


# ==========================================
# SECTION 11: RECOMMENDATIONS
# ==========================================
def generate_recommendations(df, styles):
    """Generate practical HR recommendations based on data."""
    elements = []
    elements.append(Paragraph("10. Recommendations", styles['SectionHeader']))
    elements.append(Paragraph(
        "Based on the analysis, we recommend the following actions:",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.1 * inch))
    
    recommendations = []
    
    # Retention strategy
    if 'Risk_Category' in df.columns:
        high_risk = len(df[df['Risk_Category'] == 'High Risk'])
        if high_risk > 0:
            recommendations.append("• <b>Retention Strategy:</b> Conduct stay interviews with high-risk employees to understand their concerns and address them proactively.")
    
    # Salary review
    if 'MonthlyIncome' in df.columns and 'YearsAtCompany' in df.columns:
        recommendations.append("• <b>Salary Review:</b> Implement a structured compensation framework that rewards tenure and performance to reduce turnover among experienced employees.")
    
    # Engagement
    if 'Sentiment_Category' in df.columns:
        negative_pct = (df['Sentiment_Category'] == 'Negative').mean() * 100
        if negative_pct > 20:
            recommendations.append("• <b>Employee Engagement:</b> Launch quarterly pulse surveys and action plans to address the concerns raised in negative feedback.")
    
    # Leave management
    if 'AbsenteeismRate' in df.columns:
        recommendations.append("• <b>Leave Management:</b> Encourage employees to use their annual leave to prevent burnout. Monitor sick leave patterns as early warning signs.")
    
    # Workforce planning
    if 'Age' in df.columns:
        older_workers = len(df[df['Age'] > 50])
        if older_workers > 0:
            recommendations.append("• <b>Workforce Planning:</b> Develop succession plans for senior employees approaching retirement to ensure knowledge transfer.")
    
    # Diversity
    if 'Gender' in df.columns and 'JobRole' in df.columns:
        recommendations.append("• <b>Diversity & Inclusion:</b> Review promotion criteria to ensure equitable advancement opportunities across all genders.")
    
    for rec in recommendations:
        elements.append(Paragraph(rec, styles['BulletPoint']))
    
    return elements


# ==========================================
# SECTION 12: APPENDIX
# ==========================================
def build_appendix(df, styles):
    """Build appendix with data preview."""
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("11. Appendix: Data Preview", styles['SectionHeader']))
    elements.append(Paragraph(
        "The table below shows the first 10 rows of the analyzed dataset:",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.15 * inch))
    
    # Select key columns for preview
    preview_cols = ['Age', 'Gender', 'Department', 'JobRole', 'MonthlyIncome', 'YearsAtCompany', 'OverTime', 'Attrition']
    preview_cols = [col for col in preview_cols if col in df.columns]
    
    preview_df = df[preview_cols].head(10)
    
    # Convert to table data
    table_data = [preview_cols]
    for _, row in preview_df.iterrows():
        table_data.append([str(row[col]) for col in preview_cols])
    
    # Create table
    col_widths = [1.2*inch] * len(preview_cols)
    table = Table(table_data, colWidths=col_widths)
    
    table_style = [
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 7),
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, -1), black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    table.setStyle(TableStyle(table_style))
    
    elements.append(table)
    return elements


# ==========================================
# MAIN REPORT GENERATION FUNCTION
# ==========================================
def generate_hr_report(df, filename="HR_Report.pdf", cleaning_summary=None, model_accuracy=None):
    """
    Main function to generate the complete HR Analytics PDF report.
    """
    # Create temp directory for charts
    temp_dir = tempfile.mkdtemp()
    
    # Initialize PDF document
    doc = BaseDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="HR Analytics Report",
        author="HR Analytics Dashboard",
        subject="Workforce Analysis & AI Insights"
    )
    
    # Create page template with header/footer
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id='normal'
    )
    template = PageTemplate(id='main', frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])
    
    # Get styles
    styles = get_styles()
    
    # Build document elements
    elements = []
    
    # 1. Cover Page
    elements.extend(build_cover_page(df, filename, styles))
    
    # 2. Executive Summary (CORRECTED ORDER: df, styles, model_accuracy)
    elements.extend(build_executive_summary(df, styles, model_accuracy))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 3. Data Cleaning Summary
    elements.extend(build_data_cleaning_summary(df, cleaning_summary, styles))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 4. Attrition Prediction (CORRECTED ORDER: df, styles, model_accuracy, temp_dir)
    elements.extend(build_attrition_report(df, styles, model_accuracy, temp_dir))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 5. Sentiment Analysis (CORRECTED ORDER: df, styles, temp_dir)
    elements.extend(build_sentiment_report(df, styles, temp_dir))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 6. Leave & Absenteeism
    elements.extend(build_leave_report(df, styles, temp_dir))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 7. Diversity & Demographics
    elements.extend(build_diversity_report(df, styles, temp_dir))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 8. Compensation Analysis
    elements.extend(build_compensation_report(df, styles, temp_dir))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 9. Correlation Analysis
    elements.extend(build_correlation_report(df, styles, temp_dir))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 10. AI Insights
    elements.extend(generate_ai_insights(df, styles))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 11. Recommendations
    elements.extend(generate_recommendations(df, styles))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 12. Appendix
    elements.extend(build_appendix(df, styles))
    
    # Build PDF
    doc.build(elements)
    
    # Cleanup temp files
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    return filename