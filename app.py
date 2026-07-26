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
This file handles ONLY the user interface.
All business logic is in the modules/ folder.
"""

import streamlit as st
import pandas as pd
from modules import cleaning
from modules import charts
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
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1e3a8a; 
                   border-bottom: 3px solid #3b82f6; padding-bottom: 0.3rem; }
    .sub-header { font-size: 1.3rem; font-weight: 600; color: #374151; 
                  margin-top: 1rem; margin-bottom: 0.5rem; }
    .metric-card { background: white; padding: 1.2rem; border-radius: 8px; 
                   box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center; }
    .metric-label { font-size: 0.85rem; color: #6b7280; text-transform: uppercase; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #1e3a8a; margin-top: 0.3rem; }
    .success-box { background-color: #10b981; color: white; padding: 0.8rem; 
                   border-radius: 6px; margin: 0.5rem 0; }
    .info-box { background-color: #3b82f6; color: white; padding: 0.8rem; 
                border-radius: 6px; margin: 0.3rem 0; }
    </style>
""", unsafe_allow_html=True)


# ============ HEADER ============
st.markdown('<div class="main-header">HR Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown("Upload your HR dataset to begin automated analysis and visualization.")
st.markdown("---")


# ============ FILE UPLOAD ============
st.markdown('<div class="sub-header">Step 1: Data Upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")


# ============ DATA PROCESSING ============
if uploaded_file is not None:
    try:
        # Show loading spinner
        with st.spinner('Loading and cleaning data...'):
            
            # Call our cleaning module
            df_clean, summary = cleaning.load_and_clean_data(uploaded_file)
        
        # Success message
        st.markdown('<div class="success-box">Data loaded and cleaned successfully!</div>', 
                   unsafe_allow_html=True)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Total Rows</div>
                    <div class="metric-value">{summary["final_rows"]:,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Duplicates Removed</div>
                    <div class="metric-value">{summary["duplicates_removed"]}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Missing Values Fixed</div>
                    <div class="metric-value">{summary["missing_values_filled"]}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # ============ VISUALIZATIONS ============
        st.markdown('<div class="sub-header">Step 2: Visualizations</div>', unsafe_allow_html=True)
        
        # Generate all charts from our charts module
        all_charts = charts.create_all_charts(df_clean)
        
        # Display charts in a grid
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.plotly_chart(all_charts["department"], use_container_width=True)
        
        with chart_col2:
            st.plotly_chart(all_charts["age"], use_container_width=True)
        
        # Full-width chart
        st.plotly_chart(all_charts["attrition"], use_container_width=True)
        
        # ============ DATA PREVIEW ============
        st.markdown('<div class="sub-header">Step 3: Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df_clean.head(10), use_container_width=True)
        
        # Save to session state (so other pages can use it later)
        st.session_state['df_clean'] = df_clean
        
    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.info("Please make sure your CSV has the required columns.")
else:
    st.info("👆 Please upload a CSV file to get started.")