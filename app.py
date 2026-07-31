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
from modules import attrition # NEW: Import our ML module
import config

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
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
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown('<div class="main-header">HR Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown("Upload your HR dataset to begin automated analysis, cleaning, and ML prediction.")
st.markdown("---")

# ============ FILE UPLOAD ============
st.markdown('<div class="sub-header">Step 1: Data Upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")

# ============ DATA PROCESSING ============
if uploaded_file is not None:
    try:
        with st.spinner('Loading and cleaning data...'):
            df_clean, summary = cleaning.load_and_clean_data(uploaded_file)
        
        st.markdown('<div class="success-box">Data loaded and cleaned successfully!</div>', unsafe_allow_html=True)
        
        # Display basic metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Rows</div><div class="metric-value">{summary["final_rows"]:,}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Duplicates Removed</div><div class="metric-value">{summary["duplicates_removed"]}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Missing Values Fixed</div><div class="metric-value">{summary["missing_values_filled"]}</div></div>', unsafe_allow_html=True)

        # ==========================================
        # --- DAY 7: MACHINE LEARNING INTEGRATION ---
        # ==========================================
        st.markdown('<div class="sub-header">Step 2: AI Attrition Prediction</div>', unsafe_allow_html=True)
        
        with st.spinner('Training ML model and calculating flight risk...'):
            # 1. Prepare data for ML (encoding)
            X, y, target_encoder = attrition.prepare_ml_data(df_clean)
            
            # 2. Train the model
            model, accuracy = attrition.train_attrition_model(X, y)
            
            # 3. Get probability scores (chance of leaving, from 0.0 to 1.0)
            # predict_proba returns [[prob_of_0, prob_of_1]]. We want index 1 (prob of 'Yes')
            risk_scores = model.predict_proba(X)[:, 1]
            
            # 4. Add scores back to our clean dataframe
            df_clean['Flight_Risk_Score'] = (risk_scores * 100).round(1) # Convert to percentage
            
            # 5. Categorize the risk
            def categorize_risk(score):
                if score >= 70:
                    return 'High Risk'
                elif score >= 40:
                    return 'Medium Risk'
                else:
                    return 'Low Risk'
            
            df_clean['Risk_Category'] = df_clean['Flight_Risk_Score'].apply(categorize_risk)

        # Display ML Metrics
        ml_col1, ml_col2 = st.columns(2)
        with ml_col1:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Model Accuracy</div>
                    <div class="metric-value">{accuracy * 100:.1f}%</div>
                </div>
            ''', unsafe_allow_html=True)
        with ml_col2:
            high_risk_count = len(df_clean[df_clean['Risk_Category'] == 'High Risk'])
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">High Risk Employees</div>
                    <div class="metric-value" style="color: #ef4444;">{high_risk_count}</div>
                </div>
            ''', unsafe_allow_html=True)

        # ==========================================
        # --- VISUALIZATIONS ---
        # ==========================================
        st.markdown('<div class="sub-header">Step 3: Visualizations</div>', unsafe_allow_html=True)
        all_charts = charts.create_all_charts(df_clean)
        
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.plotly_chart(all_charts["department"], use_container_width=True)
        with chart_col2:
            st.plotly_chart(all_charts["age"], use_container_width=True)
        st.plotly_chart(all_charts["attrition"], use_container_width=True)

        # ============ DATA PREVIEW WITH RISK ============
        st.markdown('<div class="sub-header">Step 4: Employee Risk Preview</div>', unsafe_allow_html=True)
        
        # Select only relevant columns for the preview to keep it clean
        preview_cols = ['Age', 'Department', 'JobRole', 'MonthlyIncome', 'OverTime', 'Flight_Risk_Score', 'Risk_Category', 'Attrition']
        # Only keep columns that actually exist in the dataframe (safety check)
        preview_cols = [col for col in preview_cols if col in df_clean.columns]
        
        st.dataframe(df_clean[preview_cols].head(15), use_container_width=True)
        
        # Save to session state
        st.session_state['df_clean'] = df_clean
        
    except ValueError as ve:
        st.error(f"⚠️ Data Validation Error: {ve}")
        st.info("Please check your CSV file and ensure it has the required columns.")
    except pd.errors.EmptyDataError:
        st.error("⚠️ The uploaded file is empty.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
        st.info("Please try uploading a different file.")
else:
    st.info("👆 Please upload a CSV file to get started.")
