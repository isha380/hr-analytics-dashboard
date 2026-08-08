# import streamlit as st
# import pandas as pd

# # 1. Professional Page Configuration
# st.set_page_config(
#     page_title="HR Analytics Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # 2. Custom CSS for Professional Styling
# st.markdown("""
#     <style>
#     .stApp {
#         background-color: #f8f9fa;
#     }
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: 700;
#         color: #1e3a8a;
#         margin-bottom: 0.2rem;
#         border-bottom: 3px solid #3b82f6;
#         padding-bottom: 0.5rem;
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         font-weight: 600;
#         color: #374151;
#         margin-top: 0.8rem;
#         margin-bottom: 0.5rem;
#     }
#     .metric-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         text-align: center;
#     }
#     .metric-label {
#         font-size: 0.9rem;
#         color: #6b7280;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
#     .metric-value {
#         font-size: 2rem;
#         font-weight: 700;
#         color: #1e3a8a;
#         margin-top: 0.5rem;
#     }
#     .success-box {
#         background-color: #10b981;
#         color: white;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
#     .info-box {
#         background-color: #3b82f6;
#         color: white;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 0.5rem 0;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # 3. Professional Header
# st.markdown('<div class="main-header">HR Analytics Dashboard</div>', unsafe_allow_html=True)


# # 4. Data Cleaning Function
# def clean_data(df):
#     """Automated data cleaning function"""
#     original_rows = len(df)
#     df_clean = df.drop_duplicates()
#     duplicates_removed = original_rows - len(df_clean)

#     numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
#     for col in numeric_cols:
#         if df_clean[col].isnull().sum() > 0:
#             df_clean[col].fillna(df_clean[col].median(), inplace=True)

#     text_cols = df_clean.select_dtypes(include=['object']).columns
#     for col in text_cols:
#         if df_clean[col].isnull().sum() > 0:
#             df_clean[col].fillna('Unknown', inplace=True)

#     return df_clean, duplicates_removed

# # 5. File Upload Section
# st.markdown('<div class="sub-header">Step 1: Data Upload</div>', unsafe_allow_html=True)
# uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")

# # 6. Data Processing
# if uploaded_file is not None:
#     try:
#         with st.spinner('Loading data...'):
#             df = pd.read_csv(uploaded_file)

#         st.markdown('<div class="success-box">File uploaded successfully</div>', unsafe_allow_html=True)

#         st.markdown('<div class="sub-header">Dataset Overview</div>', unsafe_allow_html=True)
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">Total Rows</div>
#                     <div class="metric-value">{len(df):,}</div>
#                 </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">Total Columns</div>
#                     <div class="metric-value">{len(df.columns)}</div>
#                 </div>
#             """, unsafe_allow_html=True)

#         with col3:
#             file_size_kb = uploaded_file.size / 1024
#             st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">File Size</div>
#                     <div class="metric-value">{file_size_kb:.2f} KB</div>
#                 </div>
#             """, unsafe_allow_html=True)

#         st.markdown('<div class="sub-header">Step 2: Data Cleaning</div>', unsafe_allow_html=True)

#         with st.spinner('Cleaning data...'):
#             df_clean, duplicates_removed = clean_data(df)

#         st.markdown('<div class="success-box">Data cleaning completed successfully</div>', unsafe_allow_html=True)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown(f"""
#                 <div class="info-box">
#                     <strong>Duplicates Removed:</strong> {duplicates_removed} rows
#                 </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#                 <div class="info-box">
#                     <strong>Final Dataset:</strong> {len(df_clean):,} rows
#                 </div>
#             """, unsafe_allow_html=True)

#         st.markdown('<div class="sub-header">Data Preview</div>', unsafe_allow_html=True)
#         st.dataframe(df_clean.head(10), use_container_width=True)

#         st.session_state['df_clean'] = df_clean

#     except Exception as e:
#         st.error(f"Error loading file: {e}")
# else:
#     st.info("Please upload a CSV file to get started.")


"""
Main Streamlit application for HR Analytics Dashboard.
"""

import streamlit as st
import pandas as pd
from modules import cleaning
from modules import charts
from modules import attrition
from modules import sentiment
import plotly.express as px
from modules import leave
from modules import diversity
from modules import compensation
from modules import pdf_report
import config

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============ CUSTOM CSS ============
st.markdown(
    """
    <style>
    .stApp { background-color: #f8f9fa; padding-top: 1rem; }
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1e3a8a; border-bottom: 3px solid #3b82f6; padding-bottom: 0.3rem; }
    .sub-header { font-size: 1.3rem; font-weight: 600; color: #374151; margin-top: 1rem; margin-bottom: 0.5rem; }
    .metric-card { background: white; padding: 1.2rem; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center; }
    .metric-label { font-size: 0.85rem; color: #6b7280; text-transform: uppercase; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #1e3a8a; margin-top: 0.3rem; }
    .success-box { background-color: #10b981; color: white; padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; }
    .info-box { background-color: #3b82f6; color: white; padding: 0.8rem; border-radius: 6px; margin: 0.3rem 0; }
    .risk-high { color: #ef4444; font-weight: bold; }
    .risk-medium { color: #f59e0b; font-weight: bold; }
    .risk-low { color: #10b981; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============ HEADER ============
st.markdown(
    '<div class="main-header">HR Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    "Upload your HR dataset to begin automated analysis, cleaning, and ML prediction."
)

st.markdown("---")

# ============ FILE UPLOAD ============
st.markdown(
    '<div class="sub-header">Step 1: Data Upload</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    label_visibility="collapsed"
)

# ============ DATA PROCESSING ============
if uploaded_file is not None:
    try:

        with st.spinner("Loading and cleaning data..."):
            df_clean, summary = cleaning.load_and_clean_data(uploaded_file)

        st.markdown(
            '<div class="success-box">Data loaded and cleaned successfully!</div>',
            unsafe_allow_html=True,
        )

        # ==========================================
        # BASIC METRICS
        # ==========================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total Rows</div>
                    <div class="metric-value">{summary["final_rows"]:,}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Duplicates Removed</div>
                    <div class="metric-value">{summary["duplicates_removed"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Missing Values Fixed</div>
                    <div class="metric-value">{summary["missing_values_filled"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ==========================================
        # DAY 9 : SIDEBAR FILTERS
        # ==========================================

        st.sidebar.header("🔍 Filter Data")

        # Department Filter
        if "Department" in df_clean.columns:
            departments = sorted(df_clean["Department"].dropna().unique())
            selected_depts = st.sidebar.multiselect(
                "Department",
                departments,
                default=departments,
            )
        else:
            selected_depts = []

        # Job Role Filter
        if "JobRole" in df_clean.columns:
            job_roles = sorted(df_clean["JobRole"].dropna().unique())
            selected_roles = st.sidebar.multiselect(
                "Job Role",
                job_roles,
                default=job_roles,
            )
        else:
            selected_roles = []

        # Create filtered dataframe
        df_filtered = df_clean.copy()

        if "Department" in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered["Department"].isin(selected_depts)
            ]

        if "JobRole" in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered["JobRole"].isin(selected_roles)
            ]

        st.sidebar.info(
            f"Showing {len(df_filtered)} of {len(df_clean)} employees"
        )

        # ==========================================
        # DAY 7 : MACHINE LEARNING
        # ==========================================

        if len(df_filtered) > 10:

            st.markdown(
                '<div class="sub-header">Step 2: AI Attrition Prediction</div>',
                unsafe_allow_html=True,
            )

            with st.spinner("Training ML model and calculating flight risk..."):

                X, y, target_encoder = attrition.prepare_ml_data(df_filtered)

                model, accuracy = attrition.train_attrition_model(X, y)

                risk_scores = model.predict_proba(X)[:, 1]

                df_filtered = df_filtered.copy()

                df_filtered["Flight_Risk_Score"] = (
                    risk_scores * 100
                ).round(1)

                def categorize_risk(score):
                    if score >= 70:
                        return "High Risk"
                    elif score >= 40:
                        return "Medium Risk"
                    else:
                        return "Low Risk"

                df_filtered["Risk_Category"] = (
                    df_filtered["Flight_Risk_Score"]
                    .apply(categorize_risk)
                )

            ml_col1, ml_col2 = st.columns(2)

            with ml_col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Model Accuracy</div>
                        <div class="metric-value">{accuracy*100:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with ml_col2:

                high_risk_count = len(
                    df_filtered[
                        df_filtered["Risk_Category"] == "High Risk"
                    ]
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">High Risk Employees</div>
                        <div class="metric-value" style="color:#ef4444;">
                            {high_risk_count}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.warning(
                "⚠️ Not enough records after filtering to train the ML model."
            )

        # ==========================================
        # DAY 8 : NLP SENTIMENT
        # ==========================================

        st.markdown(
            '<div class="sub-header">Step 3: AI Sentiment Analysis (NLP)</div>',
            unsafe_allow_html=True,
        )

        if len(df_filtered) > 0 and "Feedback" in df_filtered.columns:

            with st.spinner("Analyzing employee feedback sentiment..."):

                df_filtered = sentiment.process_feedback_column(
                    df_filtered,
                    text_column="Feedback",
                )

            sent_col1, sent_col2 = st.columns(2)

            with sent_col1:

                avg_sentiment = (
                    df_filtered["Sentiment_Score"].mean()
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Avg Sentiment Score
                        </div>
                        <div class="metric-value">
                            {avg_sentiment:.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with sent_col2:

                positive_count = len(
                    df_filtered[
                        df_filtered["Sentiment_Category"]
                        == "Positive"
                    ]
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Positive Feedback
                        </div>
                        <div class="metric-value"
                             style="color:#10b981;">
                             {positive_count}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            sent_counts = (
                df_filtered["Sentiment_Category"]
                .value_counts()
            )

            fig_sentiment = px.pie(
                values=sent_counts.values,
                names=sent_counts.index,
                title="Employee Feedback Sentiment Distribution",
                color=sent_counts.index,
                color_discrete_map={
                    "Positive": "#10b981",
                    "Neutral": "#f59e0b",
                    "Negative": "#ef4444",
                },
            )

            st.plotly_chart(
                fig_sentiment,
                use_container_width=True,
            )
        elif len(df_filtered) == 0:
            st.warning("⚠️ No employees match your current filters. Please adjust your filters.")
        else:

            st.warning(
                "⚠️ No 'Feedback' column found. NLP analysis skipped."
            )

        # ==========================================
        # --- DAY 10: LEAVE & ABSENTEEISM ---
        # ==========================================
        st.markdown('<div class="sub-header">Step 4: Leave & Absenteeism Analytics</div>', unsafe_allow_html=True)
        
       
        if "AbsenteeismRate" in df_filtered.columns:
            
            
            dept_stats = leave.calculate_department_leave_stats(df_filtered)
            
            # 2. Display High-Level Metrics
            avg_sick = df_filtered['SickLeaveTaken'].mean()
            avg_annual = df_filtered['AnnualLeaveTaken'].mean()
            
            leave_col1, leave_col2 = st.columns(2)
            with leave_col1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Sick Days (Company)</div><div class="metric-value">{avg_sick:.1f}</div></div>', unsafe_allow_html=True)
            with leave_col2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Vacation Days Used</div><div class="metric-value">{avg_annual:.1f}</div></div>', unsafe_allow_html=True)

            # 3. Create a Bar Chart for Department Absenteeism
            # We reset_index() because groupby makes 'Department' the index, and Plotly needs it as a column
            dept_stats_reset = dept_stats.reset_index() 
            
            fig_leave = px.bar(
                dept_stats_reset, 
                x='Department', 
                y='AbsenteeismRate', 
                title="Absenteeism Rate by Department (%)",
                color='AbsenteeismRate',
                color_continuous_scale='Reds' # Redder means higher absenteeism
            )
            st.plotly_chart(fig_leave, use_container_width=True)

            # 4. Show Top Absentees Table
            st.markdown('<div class="sub-header">⚠️ Employees Requiring Wellness Check-in</div>', unsafe_allow_html=True)
            top_absentees = leave.get_top_absentees(df_filtered, top_n=5)
            st.dataframe(top_absentees, use_container_width=True)
            
        else:
            st.warning("⚠️ Leave data is not available in this dataset.")

        # ==========================================
        # --- DAY 11: DIVERSITY & DEMOGRAPHICS ---
        # ==========================================
        st.markdown('<div class="sub-header">Step 5: Diversity & Demographics</div>', unsafe_allow_html=True)
        
        # Create two columns for the charts
        div_col1, div_col2 = st.columns(2)
        
        with div_col1:
            st.markdown("#### Gender Distribution by Job Role")
            # Get the data from our module
            gender_data = diversity.get_gender_distribution_by_role(df_filtered)
            
            # Create a stacked bar chart
            # barmode='stack' puts Male and Female on top of each other to show total role size
            fig_gender = px.bar(
                gender_data, 
                x='JobRole', 
                y='Count', 
                color='Gender', 
                barmode='stack',
                title="Gender Breakdown per Role",
                color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'} # Blue and Pink
            )
            st.plotly_chart(fig_gender, use_container_width=True)
            
        with div_col2:
            st.markdown("#### Age Distribution by Department")
            # Get the stats table
            age_stats = diversity.get_age_stats_by_department(df_filtered)
            st.dataframe(age_stats, use_container_width=True)
            
            fig_age = px.box(
                df_filtered, 
                x='Department', 
                y='Age', 
                color='Department',
                title="Age Spread per Department",
                points="outliers" # Shows individual dots for very young/old employees
            )
            st.plotly_chart(fig_age, use_container_width=True)

        # ==========================================
        # --- DAY 12: COMPENSATION & PAY EQUITY ---
        # ==========================================
        st.markdown('<div class="sub-header">Step 6: Compensation & Pay Equity</div>', unsafe_allow_html=True)
        
        
        if "MonthlyIncome" in df_filtered.columns and "YearsAtCompany" in df_filtered.columns:
            
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("#### Gender Pay Gap by Role")
                # Get the average pay data
                pay_data = compensation.get_average_pay_by_role_and_gender(df_filtered)
                
                # Create a grouped bar chart (barmode='group' puts bars side-by-side)
                fig_pay = px.bar(
                    pay_data, 
                    x='JobRole', 
                    y='MonthlyIncome', 
                    color='Gender', 
                    barmode='group',
                    title="Average Monthly Income by Gender",
                    color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'}
                )
                st.plotly_chart(fig_pay, use_container_width=True)
                
            with comp_col2:
                st.markdown("#### Income vs. Experience")
                # Create a scatter plot
                # Each dot is one employee. X-axis is years worked, Y-axis is salary.
                fig_scatter = px.scatter(
                    df_filtered, 
                    x='YearsAtCompany', 
                    y='MonthlyIncome', 
                    color='Gender',
                    title="Salary Growth Over Time",
                    opacity=0.7 # Makes dots slightly transparent so we can see overlaps
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
                
        else:
            st.warning("⚠️ Compensation data is not available in this dataset.")

        # ==========================================
        # VISUALIZATIONS
        # ==========================================

        st.markdown(
            '<div class="sub-header">Step 4: Visualizations & Correlations</div>',
            unsafe_allow_html=True,
        )

        all_charts = charts.create_all_charts(df_filtered)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(
                all_charts["department"],
                use_container_width=True,
            )

        with chart_col2:
            st.plotly_chart(
                all_charts["age"],
                use_container_width=True,
            )

        st.plotly_chart(
            all_charts["attrition"],
            use_container_width=True,
        )

        # Correlation Heatmap
        try:
            heatmap_chart = charts.create_correlation_heatmap(
                df_filtered
            )

            st.plotly_chart(
                heatmap_chart,
                use_container_width=True,
            )

        except Exception:
            pass

        # ==========================================
        # DATA PREVIEW
        # ==========================================

        st.markdown(
            '<div class="sub-header">Step 5: Filtered Data Preview</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            df_filtered.head(10),
            use_container_width=True,
        )

        st.session_state["df_clean"] = df_filtered

       
  
        # ==========================================
        # --- DAY 13: PDF EXPORT ---
        # ==========================================
  
        st.markdown("---")
        st.markdown('<div class="sub-header">Step 7: Export Executive Report</div>', unsafe_allow_html=True)
        st.markdown("Download a professional PDF report with charts, insights, and recommendations.")
        
        # SAFETY CHECK: Only show PDF download if we have data
        if len(df_filtered) > 0:
            try:
                temp_pdf_path = "output/temp_hr_report.pdf"
                
                import os
                os.makedirs("output", exist_ok=True)
                
                # Show progress
                with st.spinner("Generating professional PDF report..."):
                    pdf_path, csv_path = pdf_report.generate_hr_report(
                        df_filtered, 
                        temp_pdf_path,
                        cleaning_summary=summary,
                        model_accuracy=accuracy if 'accuracy' in locals() else None,
                        export_csv=True
                    )
                    print(f"✓ PDF Report: {pdf_path}")
                    print(f"✓ Cleaned Data: {csv_path}")
                
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_file,
                        file_name="HR_Executive_Summary.pdf",
                        mime="application/pdf"
                    )
                    
            except Exception as pdf_error:
                st.error(f"❌ **PDF Generation Failed**\n\nError: {str(pdf_error)}\n\nPlease check the terminal for more details.")
                import traceback
                st.code(traceback.format_exc())
        else:
            st.warning("️ **Cannot generate report**\n\nNo employees match your current filters.")
    except Exception as e:
        st.error("No data to visualize.\n\n The filters you selected returned 0 employees. Please adjust your filters in the sidebar to see charts and data.")
else:
    st.info("Please upload a CSV file to get started.")
