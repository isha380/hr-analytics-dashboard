

import streamlit as st
import pandas as pd
import plotly.io as pio
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

pio.templates.default = "plotly_white"

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============ DESIGN SYSTEM & CUSTOM CSS ============
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    :root {
        --primary: #824DFF;
        --primary-2: #9B6DFF;
        --lavender: #F0EBFF;
        --lavender-2: #D8C7FF;
        --lavender-3: #B99AFF;
        --ink: #171321;
        --muted: #756F82;
        --white: #FFFFFF;
        --success: #159A72;
        --danger: #D84B5B;
        --warning: #D9822B;
        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 22px;
        --shadow: 0 10px 30px rgba(55, 32, 115, .08);
        --shadow-hover: 0 16px 38px rgba(55, 32, 115, .13);
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: #F6F3FC !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 78% 0%, rgba(130,77,255,.08), transparent 28%),
            #F6F3FC !important;
        color: var(--ink);
    }

    .main .block-container {
        padding: 0 2.5rem 3rem !important;
        max-width: 1500px !important;
    }
    
    /* ========== HIDE DEFAULT STREAMLIT NAVBAR ========== */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Hide the Deploy button specifically (if on Streamlit Cloud) */
    .stDeployButton {
        display: none !important;
    }

    /* ========== FIXED SIDEBAR - VISIBLE ON DESKTOP ========== */
    [data-testid="stSidebar"] {
        background: var(--white) !important;
        border-right: 1px solid #E9E3F6 !important;
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        z-index: 999 !important;
        box-shadow: 8px 0 32px rgba(55, 32, 115, 0.12) !important;
        overflow-y: auto !important;
        transform: none !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: var(--white) !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1.25rem 2rem !important;
    }

    /* HIDE COLLAPSE/EXPAND BUTTONS ON DESKTOP */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarExpandButton"] {
        display: none !important;
    }

    /* Adjust main content to account for fixed sidebar */
    [data-testid="stAppViewContainer"] {
        margin-left: 300px !important;
        width: calc(100% - 300px) !important;
    }

    [data-testid="stAppViewContainer"] > section {
        margin-left: 0 !important;
        max-width: 100% !important;
    }

    /* Ensure full width coverage */
    .main .block-container {
        padding-top: 1rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 100% !important;
    }

    /* ========== SIDEBAR STYLING ========== */
    .sidebar-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 0 1.4rem;
        padding: .2rem .15rem 1.2rem;
        border-bottom: 1px solid #EEEAF6;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: .7rem;
    }

    .sidebar-brand-icon {
        width: 36px;
        height: 36px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        background: var(--lavender);
        color: var(--primary);
    }

    .sidebar-brand-icon .material-icons {
        font-size: 20px;
    }

    .sidebar-header-text {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--ink);
        letter-spacing: -.3px;
    }

    .filter-card {
        background: #FAF8FF;
        border: 1px solid #EEE8FA;
        border-radius: var(--radius-md);
        padding: .95rem;
        margin-bottom: .9rem;
        box-shadow: 0 4px 15px rgba(55,32,115,.035);
    }

    .filter-card-title {
        display: flex;
        align-items: center;
        gap: .45rem;
        font-size: .78rem;
        font-weight: 800;
        color: var(--ink);
        letter-spacing: .2px;
        margin-bottom: .65rem;
    }

    .filter-card-title::before {
        font-family: 'Material Icons';
        font-size: 17px;
        color: var(--primary);
    }

    .filter-card.department .filter-card-title::before { content: 'business'; }
    .filter-card.role .filter-card-title::before { content: 'work_outline'; }

    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: white !important;
        border: 1px solid #E4DCF3 !important;
        border-radius: 11px !important;
        min-height: 44px !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stMultiSelect > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(130,77,255,.10) !important;
    }

    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background: var(--lavender) !important;
        color: var(--primary) !important;
        border: 0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        margin: 3px 4px 3px 0 !important;
    }

    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] svg {
        color: var(--primary) !important;
    }

    .sidebar-info {
        margin-top: 1.2rem;
        padding: 1rem;
        border-radius: var(--radius-md);
        background: linear-gradient(135deg, #F0EBFF, #FAF8FF);
        border: 1px solid #E1D6F6;
        color: var(--primary);
        text-align: left;
        font-size: .82rem;
        font-weight: 700;
        line-height: 1.45;
    }

    .sidebar-info::before {
        content: 'groups';
        font-family: 'Material Icons';
        vertical-align: middle;
        margin-right: .4rem;
        font-size: 17px;
    }

    /* ========== MAIN HEADER AREA ========== */
    .main-header-area {
        margin-top: -50px;
        padding: 1.5rem 2.5rem;
        border-radius: var(--radius-lg);
        background: linear-gradient(135deg, #FFFFFF 0%, #F7F2FF 100%);
        border: 1px solid #EAE2F7;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        width: 100%;
    }

    .main-header-area::after {
        content: '';
        position: absolute;
        width: 190px;
        height: 190px;
        right: -55px;
        top: -95px;
        border-radius: 50%;
        background: rgba(130,77,255,.08);
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        color: var(--primary);
        background: var(--lavender);
        padding: .4rem .7rem;
        border-radius: 999px;
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: .7px;
        text-transform: uppercase;
        margin-bottom: .75rem;
    }

    .eyebrow .material-icons { font-size: 15px; }

    .main-title {
        font-size: clamp(2rem, 3.2vw, 3rem);
        font-weight: 800;
        color: var(--ink);
        letter-spacing: -1.5px;
        margin: 0;
        line-height: 1.08;
    }

    .main-title span { color: var(--primary); }

    .main-subtitle {
        font-size: .98rem;
        color: var(--muted);
        margin-top: .65rem;
        line-height: 1.6;
        max-width: 680px;
    }

    /* ========== UPLOAD CARD ========== */
    .section-header {
        display: flex;
        align-items: center;
        gap: .55rem;
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--ink);
        margin: 1.5rem 0 .8rem;
        letter-spacing: -.2px;
    }

    .section-header::before {
        content: attr(data-icon);
        font-family: 'Material Icons';
        display: grid;
        place-items: center;
        width: 30px;
        height: 30px;
        border-radius: 9px;
        background: var(--lavender);
        color: var(--primary);
        font-size: 17px;
    }

    .upload-card {
        background: white;
        border: 1px solid #E8E1F3;
        border-radius: var(--radius-lg);
        padding: 1.15rem 1.25rem;
        box-shadow: var(--shadow);
    }

    .upload-card-title {
        font-size: .9rem;
        font-weight: 800;
        color: var(--ink);
        margin-bottom: .25rem;
    }

    .upload-card-subtitle {
        color: var(--muted);
        font-size: .78rem;
        margin-bottom: .8rem;
    }

    [data-testid="stFileUploader"] {
        background: transparent !important;
    }

    [data-testid="stFileUploader"] label {
        display: none !important;
    }

    [data-testid="fileUploadDropzone"] {
        min-height: 116px !important;
        border: 1.5px dashed #C9B7F0 !important;
        background: #FBFAFE !important;
        border-radius: 14px !important;
        padding: 1.15rem !important;
        transition: all .2s ease !important;
    }

    [data-testid="fileUploadDropzone"]:hover {
        border-color: var(--primary) !important;
        background: #F8F4FF !important;
    }

    [data-testid="fileUploadDropzone"] section > div:first-child {
        color: var(--muted) !important;
    }

    [data-testid="stFileUploader"] button {
        background: var(--primary) !important;
        color: white !important;
        border: 0 !important;
        border-radius: 9px !important;
        padding: .55rem 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 5px 14px rgba(130,77,255,.20) !important;
    }

    [data-testid="stFileUploader"] button::before {
        content: 'upload_file';
        font-family: 'Material Icons';
        margin-right: .4rem;
        vertical-align: -3px;
        font-size: 17px;
    }

    [data-testid="stFileUploader"] button:hover {
        background: var(--primary-2) !important;
    }

    /* Hide duplicate upload text */
    [data-testid="stFileUploader"] button span {
        display: none !important;
    }

    /* ========== METRIC CARDS ========== */
    .metric-card {
        position: relative;
        background: white;
        border: 1px solid #EAE3F4;
        border-radius: var(--radius-md);
        padding: 1.15rem 1.2rem;
        min-height: 126px;
        box-shadow: 0 7px 22px rgba(55,32,115,.055);
        transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
        border-color: #D5C4F5;
    }

    .metric-card::before {
        content: 'bar_chart';
        position: absolute;
        right: 12px;
        top: 12px;
        font-family: 'Material Icons';
        font-size: 18px;
        color: var(--primary-2);
        z-index: 2;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        right: -28px;
        bottom: -32px;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: var(--lavender);
    }

    .metric-label {
        color: var(--muted);
        font-size: .7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .7px;
        margin-bottom: .65rem;
    }

    .metric-value {
        color: var(--ink);
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1;
    }

    .metric-value-danger { color: var(--danger) !important; }
    .metric-value-success { color: var(--success) !important; }

    /* ========== STATUS BOXES ========== */
    .success-box, .info-box, .warning-box {
        display: flex;
        align-items: center;
        gap: .65rem;
        background: white;
        border: 1px solid #E8E1F3;
        border-radius: 13px;
        padding: .85rem 1rem;
        margin: .8rem 0;
        box-shadow: 0 5px 18px rgba(55,32,115,.045);
        font-size: .84rem;
        font-weight: 650;
    }

    .success-box { color: var(--success); border-left: 4px solid var(--success); }
    .info-box { color: var(--primary); border-left: 4px solid var(--primary); }
    .warning-box { color: var(--warning); border-left: 4px solid var(--warning); }

    .success-box::before { content: 'check_circle'; }
    .info-box::before { content: 'info'; }
    .warning-box::before { content: 'warning'; }

    .success-box::before, .info-box::before, .warning-box::before {
        font-family: 'Material Icons';
        font-size: 20px;
    }

    /* ========== STREAMLIT BUTTONS ========== */
    .stButton > button, .stDownloadButton > button {
        border: 0 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        background: var(--primary) !important;
        color: white !important;
        box-shadow: 0 6px 16px rgba(130,77,255,.18) !important;
        transition: all .2s ease !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--primary-2) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 10px 24px rgba(130,77,255,.25) !important;
    }

    .stDownloadButton > button::before {
        content: 'file_download';
        font-family: 'Material Icons';
        margin-right: .4rem;
        vertical-align: -3px;
    }

    /* ========== DATA / CHARTS ========== */
    .stDataFrame {
        border: 1px solid #E8E1F3 !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        background: white !important;
        box-shadow: 0 6px 20px rgba(55,32,115,.04);
    }

    .stDataFrame th {
        color: var(--primary) !important;
        font-weight: 800 !important;
        background: #F8F5FE !important;
    }

    .stDataFrame td {
        color: var(--ink) !important;
    }

    .plotly-graph-div {
        border-radius: 16px !important;
        overflow: hidden;
        background: white !important;
        border: 1px solid #E8E1F3 !important;
        box-shadow: 0 6px 20px rgba(55,32,115,.045);
    }

    /* Force Plotly labels to be black */
    .plotly .xtick text,
    .plotly .ytick text,
    .plotly .xlayer text,
    .plotly .ylayer text,
    .plotly .main-svg text,
    .plotly .plot-info text {
        fill: #000000 !important;
        color: #000000 !important;
    }

    .plotly .xtitle,
    .plotly .ytitle {
        fill: #000000 !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
        .plotly .xtitle,
    .plotly .ytitle {
        fill: #000000 !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* ========== FIX HOVER TOOLTIP TEXT ========== */
    /* Make hover tooltip text white so it's visible on dark background */
    .plotly .hovertext,
    .plotly .hovertext text,
    .js-plotly-plot .hoverlayer text,
    .plotly .hoverlayer > text {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Optional: Make tooltip background slightly lighter for better contrast */
    .plotly .hovertext > rect,
    .js-plotly-plot .hoverlayer rect {
        fill: rgba(30, 30, 30, 0.9) !important;
    }

    .subsection-header {
        font-size: .9rem;
        font-weight: 800;
        color: var(--ink);
        margin: 1rem 0 .65rem;
    }
    

    hr {
        border: 0 !important;
        height: 1px !important;
        background: #E9E3F2 !important;
        margin: 1.6rem 0 !important;
    }

    .stSpinner > div { border-top-color: var(--primary) !important; }

    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: var(--muted);
    }

    .empty-state-icon {
        font-family: 'Material Icons';
        font-size: 3rem;
        color: var(--lavender-3);
        margin-bottom: .8rem;
    }

    .risk-high { color: var(--danger); font-weight: 800; }
    .risk-medium { color: var(--warning); font-weight: 800; }
    .risk-low { color: var(--success); font-weight: 800; }

    /* ========== RESPONSIVE DESIGN ========== */
    
    /* Tablet - 1024px and below */
    @media (max-width: 1024px) {
        [data-testid="stSidebar"] { 
            width: 260px !important;
            min-width: 260px !important;
            max-width: 260px !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 260px !important;
            width: calc(100% - 260px) !important;
        }
        .main .block-container {
            padding: 0 1.5rem 2rem !important;
        }
        .main-header-area {
            padding: 1.25rem 1.5rem;
        }
        .main-title {
            font-size: 2.2rem;
        }
    }

    /* Mobile Landscape & Large Phones - 768px and below */
    @media (max-width: 768px) {
        /* Hide sidebar by default on mobile */
        [data-testid="stSidebar"] { 
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            transform: translateX(-100%) !important;
            transition: transform 0.3s ease !important;
            box-shadow: 4px 0 24px rgba(55, 32, 115, 0.15) !important;
        }
        
        /* Show sidebar when Streamlit activates it */
        [data-testid="stSidebar"][style*="transform: none"] {
            transform: translateX(0) !important;
        }
        
        /* Show the hamburger menu button on mobile */
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarExpandButton"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: fixed !important;
            top: 10px !important;
            left: 10px !important;
            z-index: 1000 !important;
            background: var(--primary) !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }
        
        [data-testid="stSidebarExpandButton"] {
            display: flex !important;
        }
        
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            width: 100% !important;
        }
        
        .main .block-container {
            padding: 0 1rem 1.5rem !important;
        }
        
        .main-header-area {
            padding: 1rem;
            margin: 0 0 0.75rem;
        }
        
        .main-header-area::after {
            width: 100px;
            height: 100px;
            right: -30px;
            top: -50px;
        }
        
        .eyebrow {
            font-size: 0.6rem;
            padding: 0.3rem 0.6rem;
        }
        
        .main-title {
            font-size: 1.75rem;
            letter-spacing: -0.5px;
        }
        
        .main-subtitle {
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        .section-header {
            font-size: 0.95rem;
            margin: 1rem 0 0.6rem;
        }
        
        .section-header::before {
            width: 26px;
            height: 26px;
            font-size: 15px;
        }
        
        /* Stack metric cards vertically on mobile */
        .metric-card {
            padding: 1rem;
            min-height: 100px;
            margin-bottom: 0.75rem;
        }
        
        .metric-label {
            font-size: 0.65rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .metric-card::after {
            width: 60px;
            height: 60px;
            right: -20px;
            bottom: -20px;
        }
        
        /* Adjust filter cards */
        .filter-card {
            padding: 0.75rem;
        }
        
        .filter-card-title {
            font-size: 0.75rem;
        }
        
        /* Adjust upload area */
        [data-testid="fileUploadDropzone"] {
            min-height: 100px !important;
            padding: 1rem !important;
        }
        
        /* Smaller status boxes */
        .success-box, .info-box, .warning-box {
            padding: 0.75rem;
            font-size: 0.8rem;
        }
        
        /* Adjust charts and dataframes */
        .stDataFrame {
            font-size: 0.85rem;
        }
        
        .subsection-header {
            font-size: 0.85rem;
        }
    }

    /* Mobile Portrait - 480px and below */
    @media (max-width: 480px) {
        .main-header-area {
            padding: 0.9rem;
            margin: 0 0 0.6rem;
        }
        
        .main-title {
            font-size: 1.5rem;
        }
        
        .main-subtitle {
            font-size: 0.8rem;
            line-height: 1.5;
        }
        
        .eyebrow {
            font-size: 0.55rem;
            padding: 0.25rem 0.5rem;
            gap: 0.3rem;
        }
        
        .eyebrow .material-icons {
            font-size: 13px;
        }
        
        .section-header {
            font-size: 0.9rem;
            gap: 0.4rem;
            margin: 0.8rem 0 0.5rem;
        }
        
        .section-header::before {
            width: 24px;
            height: 24px;
            font-size: 14px;
        }
        
        /* Further reduce metric card sizes */
        .metric-card {
            padding: 0.9rem;
            min-height: 90px;
            border-radius: 12px;
        }
        
        .metric-label {
            font-size: 0.6rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 1.4rem;
        }
        
        .metric-card::before {
            font-size: 16px;
            right: 10px;
            top: 10px;
        }
        
        .metric-card::after {
            width: 50px;
            height: 50px;
        }
        
        /* Adjust sidebar for small screens */
        [data-testid="stSidebar"] {
            width: 260px !important;
            min-width: 260px !important;
            max-width: 260px !important;
        }
        
        .sidebar-header-text {
            font-size: 0.95rem;
        }
        
        .filter-card {
            padding: 0.7rem;
        }
        
        .sidebar-info {
            font-size: 0.75rem;
            padding: 0.8rem;
        }
        
        /* Adjust buttons */
        .stButton > button, .stDownloadButton > button {
            padding: 0.5rem 0.9rem !important;
            font-size: 0.85rem;
            width: 100%;
        }
        
        /* Adjust data tables */
        .stDataFrame {
            font-size: 0.8rem;
            border-radius: 10px;
        }
        
        /* Adjust status boxes */
        .success-box, .info-box, .warning-box {
            padding: 0.7rem;
            font-size: 0.75rem;
            border-radius: 10px;
        }
        
        .success-box::before, .info-box::before, .warning-box::before {
            font-size: 18px;
        }
        
        /* Reduce padding in main container */
        .main .block-container {
            padding: 0 0.75rem 1rem !important;
        }
        
        /* Adjust upload button */
        [data-testid="stFileUploader"] button {
            padding: 0.5rem 0.9rem !important;
            font-size: 0.85rem;
        }
        
        /* Smaller subsection headers */
        .subsection-header {
            font-size: 0.8rem;
            margin: 0.8rem 0 0.5rem;
        }
        
        /* Adjust file upload dropzone text */
        [data-testid="fileUploadDropzone"] section > div:first-child {
            font-size: 0.85rem !important;
        }
    }

    /* Very Small Phones - 360px and below */
    @media (max-width: 360px) {
        .main-title {
            font-size: 1.3rem;
        }
        
        .main-subtitle {
            font-size: 0.75rem;
        }
        
        .metric-value {
            font-size: 1.25rem;
        }
        
        .metric-label {
            font-size: 0.55rem;
        }
        
        [data-testid="stSidebar"] {
            width: 240px !important;
            min-width: 240px !important;
            max-width: 240px !important;
        }
    }

    /* Custom scrollbar styling */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-track { background: #F6F3FC; }
    ::-webkit-scrollbar-thumb { background: #D8C7FF; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #B99AFF; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-header">
            <span class="sidebar-header-text">Filter data</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============ MAIN CONTENT HEADER ============
st.markdown(
    """
    <div class="main-header-area">
        <div class="eyebrow"><span class="material-icons">insights</span> Workforce intelligence</div>
        <div class="main-title">HR Analytics <span>Dashboard</span></div>
        <div class="main-subtitle">Turn workforce data into clear insights — monitor people trends, identify risks, and support smarter decisions.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============ FILE UPLOAD SECTION ============
st.markdown(
    '<div class="section-header">Data Upload</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    key="hr_data_uploader"
)

# ============ DATA PROCESSING ============
if uploaded_file is not None:
    try:
        with st.spinner("Loading and cleaning data..."):
            df_clean, summary = cleaning.load_and_clean_data(uploaded_file)

        st.markdown(
            '<div class="success-box">Data loaded and cleaned successfully</div>',
            unsafe_allow_html=True,
        )

        # ==========================================
        # OVERVIEW METRICS
        # ==========================================
        st.markdown(
            '<div class="section-header" data-icon="dataset">Dataset Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total Records</div>
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
                    <div class="metric-label">Issues Fixed</div>
                    <div class="metric-value">{summary["missing_values_filled"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ==========================================
        # SIDEBAR FILTERS
        # ==========================================
        with st.sidebar:
            # Department Filter
            if "Department" in df_clean.columns:
                st.markdown(
                    '<div class="filter-card">'
                    '<div class="filter-card-title">Department</div>',
                    unsafe_allow_html=True,
                )
                departments = sorted(df_clean["Department"].dropna().unique())
                selected_depts = st.multiselect(
                    "",
                    departments,
                    default=departments,
                    label_visibility="collapsed",
                    key="dept_filter"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                selected_depts = []

           
            if "JobRole" in df_clean.columns:
                st.markdown(
                    '<div class="filter-card">'
                    '<div class="filter-card-title">Job Role</div>',
                    unsafe_allow_html=True,
                )
                job_roles = sorted(df_clean["JobRole"].dropna().unique())
                selected_roles = st.multiselect(
                    "",
                    job_roles,
                    default=job_roles,
                    label_visibility="collapsed",
                    key="role_filter"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                selected_roles = []

            # Create filtered dataframe
            df_filtered = df_clean.copy()

            if "Department" in df_filtered.columns:
                df_filtered = df_filtered[df_filtered["Department"].isin(selected_depts)]

            if "JobRole" in df_filtered.columns:
                df_filtered = df_filtered[df_filtered["JobRole"].isin(selected_roles)]

            st.markdown(
                f'<div class="sidebar-info">Showing {len(df_filtered)} of {len(df_clean)} employees</div>',
                unsafe_allow_html=True,
            )

        # ==========================================
        # ML: ATTRITION PREDICTION
        # ==========================================
        if len(df_filtered) > 10:
            st.markdown(
                '<div class="section-header" data-icon="person_search">Attrition Prediction</div>',
                unsafe_allow_html=True,
            )

            with st.spinner("Training ML model..."):
                X, y, target_encoder = attrition.prepare_ml_data(df_filtered)
                model, accuracy = attrition.train_attrition_model(X, y)
                risk_scores = model.predict_proba(X)[:, 1]
                df_filtered = df_filtered.copy()
                df_filtered["Flight_Risk_Score"] = (risk_scores * 100).round(1)

                def categorize_risk(score):
                    if score >= 50:
                        return "High Risk"
                    elif score >= 35:
                        return "Medium Risk"
                    else:
                        return "Low Risk"

                df_filtered["Risk_Category"] = df_filtered["Flight_Risk_Score"].apply(categorize_risk)

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
               
                at_risk_count = len(df_filtered[df_filtered["Risk_Category"].isin(["High Risk"])])
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">At-Risk Employees</div>
                        <div class="metric-value metric-value-danger">{at_risk_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.warning("Not enough records after filtering to train the ML model.")

        # ==========================================
        # NLP: SENTIMENT ANALYSIS
        # ==========================================
        st.markdown(
            '<div class="section-header" data-icon="forum">Sentiment Analysis</div>',
            unsafe_allow_html=True,
        )

        if len(df_filtered) > 0 and "Feedback" in df_filtered.columns:
            with st.spinner("Analyzing employee feedback..."):
                df_filtered = sentiment.process_feedback_column(df_filtered, text_column="Feedback")

            sent_col1, sent_col2 = st.columns(2)

            with sent_col1:
                avg_sentiment = df_filtered["Sentiment_Score"].mean()
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Avg Sentiment Score</div>
                        <div class="metric-value">{avg_sentiment:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with sent_col2:
                positive_count = len(df_filtered[df_filtered["Sentiment_Category"] == "Positive"])
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Positive Responses</div>
                        <div class="metric-value metric-value-success">{positive_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            sent_counts = df_filtered["Sentiment_Category"].value_counts()
            fig_sentiment = px.pie(
                values=sent_counts.values,
                names=sent_counts.index,
                title="Employee Feedback Sentiment Distribution",
                color=sent_counts.index,
                color_discrete_map={
                    "Positive": "#059669",
                    "Neutral": "#EA580C",
                    "Negative": "#DC2626",
                },
            )
            fig_sentiment.update_layout(
                margin=dict(l=20, r=20, t=55, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="black", size=12),
                title=dict(font=dict(color="black", size=14)),
                xaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                yaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="black")),
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
        elif len(df_filtered) == 0:
            st.warning("No employees match your current filters.")
        else:
            st.info("No feedback data available for sentiment analysis.")

        # ==========================================
        # LEAVE & ABSENTEEISM
        # ==========================================
        st.markdown('<div class="section-header" data-icon="event_available">Leave & Absenteeism</div>', unsafe_allow_html=True)

        if "AbsenteeismRate" in df_filtered.columns:
            dept_stats = leave.calculate_department_leave_stats(df_filtered)
            avg_sick = df_filtered['SickLeaveTaken'].mean()
            avg_annual = df_filtered['AnnualLeaveTaken'].mean()

            leave_col1, leave_col2 = st.columns(2)
            with leave_col1:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Avg Sick Days</div><div class="metric-value">{avg_sick:.1f}</div></div>',
                    unsafe_allow_html=True
                )
            with leave_col2:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Avg Vacation Days</div><div class="metric-value">{avg_annual:.1f}</div></div>',
                    unsafe_allow_html=True
                )

            dept_stats_reset = dept_stats.reset_index()
            fig_leave = px.bar(
                dept_stats_reset,
                x='Department',
                y='AbsenteeismRate',
                title="Absenteeism Rate by Department",
                color='AbsenteeismRate',
                color_continuous_scale='Reds'
            )
            fig_leave.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="black", size=12),
                title=dict(font=dict(color="black", size=14)),
                xaxis=dict(
                    title='Department',
                    title_font=dict(color="black", size=13, family="Inter"),
                    tickfont=dict(color="black", size=11)
                ),
                yaxis=dict(
                    title='Absenteeism Rate',
                    title_font=dict(color="black", size=13, family="Inter"),
                    tickfont=dict(color="black", size=11)
                ),
            )
            st.plotly_chart(fig_leave, use_container_width=True)

            st.markdown('<div class="subsection-header">Employees Requiring Attention</div>', unsafe_allow_html=True)
            top_absentees = leave.get_top_absentees(df_filtered, top_n=5)
            st.dataframe(top_absentees, use_container_width=True)
        else:
            st.info("Leave data is not available in this dataset.")

        # ==========================================
        # DIVERSITY & DEMOGRAPHICS
        # ==========================================
        st.markdown('<div class="section-header" data-icon="diversity_3">Diversity & Demographics</div>', unsafe_allow_html=True)

        div_col1, div_col2 = st.columns(2)

        with div_col1:
            st.markdown("##### Gender Distribution by Role")
            gender_data = diversity.get_gender_distribution_by_role(df_filtered)
            fig_gender = px.bar(
                gender_data,
                x='JobRole',
                y='Count',
                color='Gender',
                barmode='stack',
                color_discrete_map={'Male': '#824DFF', 'Female': '#EA580C'}
            )
            fig_gender.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=120),
                xaxis=dict(
                    title='Job Role',
                    title_font=dict(color="black", size=13, family="Inter"),
                    tickfont=dict(color="black", size=10),
                    tickangle=45
                ),
                yaxis=dict(
                    title='Count',
                    title_font=dict(color="black", size=13, family="Inter"),
                    tickfont=dict(color="black", size=11)
                ),
                legend=dict(
                    font=dict(color="black", size=10),
                    orientation="h", yanchor="top", y=-0.35, xanchor="center", x=0.5
                ),
            )
            st.plotly_chart(fig_gender, use_container_width=True)

        with div_col2:
            st.markdown("##### Age Statistics")
            age_stats = diversity.get_age_stats_by_department(df_filtered)
            st.dataframe(age_stats, use_container_width=True)

            fig_age = px.box(
                df_filtered,
                x='Department',
                y='Age',
                color='Department',
                points="outliers"
            )
            fig_age.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=120),
               
                
                xaxis=dict(
                    title='Department',
                    title_font=dict(color="black", size=13, family="Inter"),
                    tickfont=dict(color="black", size=11)
                ),
                yaxis=dict(
                    title='Age',
                    title_font=dict(color="black", size=13, family="Inter"),
                    tickfont=dict(color="black", size=11)
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_age, use_container_width=True)

        # ==========================================
        # COMPENSATION & PAY EQUITY
        # ==========================================
        st.markdown('<div class="section-header" data-icon="payments">Compensation & Equity</div>', unsafe_allow_html=True)

        if "MonthlyIncome" in df_filtered.columns and "YearsAtCompany" in df_filtered.columns:
            comp_col1, comp_col2 = st.columns(2)

            with comp_col1:
                st.markdown("##### Gender Pay Gap by Role")
                pay_data = compensation.get_average_pay_by_role_and_gender(df_filtered)
                fig_pay = px.bar(
                    pay_data,
                    x='JobRole',
                    y='MonthlyIncome',
                    color='Gender',
                    barmode='group',
                    color_discrete_map={'Male': '#824DFF', 'Female': '#EA580C'}
                )
                fig_pay.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=120),
                    
                    xaxis=dict(
                        title='Job Role',
                        title_font=dict(color="black", size=13, family="Inter"),
                        tickfont=dict(color="black", size=10),
                        tickangle=45
                    ),
                    yaxis=dict(
                        title='Monthly Income',
                        title_font=dict(color="black", size=13, family="Inter"),
                        tickfont=dict(color="black", size=11)
                    ),
                    legend=dict(
                        font=dict(color="black", size=10),
                        orientation="h", yanchor="top", y=-0.35, xanchor="center", x=0.5
                        
                    ),
                )
                st.plotly_chart(fig_pay, use_container_width=True)

            with comp_col2:
                st.markdown("##### Income vs. Experience")
                fig_scatter = px.scatter(
                    df_filtered,
                    x='YearsAtCompany',
                    y='MonthlyIncome',
                    color='Gender',
                    opacity=0.7
                )
                fig_scatter.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=120),
                    xaxis=dict(
                        title='Years at Company',
                        title_font=dict(color="black", size=13, family="Inter"),
                        tickfont=dict(color="black", size=11)
                    ),
                    yaxis=dict(
                        title='Monthly Income',
                        title_font=dict(color="black", size=13, family="Inter"),
                        tickfont=dict(color="black", size=11)
                    ),
                    legend=dict(
                        font=dict(color="black", size=10),
                        orientation="h", yanchor="top", y=-0.35, xanchor="center", x=0.5
                       
                    ),
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Compensation data is not available in this dataset.")

        # ==========================================
        # ADDITIONAL CHARTS
        # ==========================================
        st.markdown(
            '<div class="section-header" data-icon="insights">Additional Analytics</div>',
            unsafe_allow_html=True,
        )

        all_charts = charts.create_all_charts(df_filtered)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            if "department" in all_charts:
                all_charts["department"].update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                   
                    font=dict(family="Inter, sans-serif", color="black", size=12),
                    xaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                    yaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                )
                st.plotly_chart(all_charts["department"], use_container_width=True)

        with chart_col2:
            if "age" in all_charts:
                all_charts["age"].update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", color="black", size=12),
                    xaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                    yaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                )
                st.plotly_chart(all_charts["age"], use_container_width=True)

        if "attrition" in all_charts:
            all_charts["attrition"].update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="black", size=12),
                xaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                yaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
            )
            st.plotly_chart(all_charts["attrition"], use_container_width=True)

        # Correlation Heatmap
        try:
            heatmap_chart = charts.create_correlation_heatmap(df_filtered)
            heatmap_chart.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="black", size=12),
                xaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
                yaxis=dict(title_font=dict(color="black", size=13), tickfont=dict(color="black", size=11)),
            )
            st.plotly_chart(heatmap_chart, use_container_width=True)
        except Exception:
            pass

        # ==========================================
        # DATA PREVIEW
        # ==========================================
        st.markdown(
            '<div class="section-header" data-icon="table_view">Data Preview</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_filtered.head(10), use_container_width=True)
        st.session_state["df_clean"] = df_filtered

        # ==========================================
        # PDF EXPORT
        # ==========================================
        st.markdown('<div class="section-header" data-icon="file_download">Export Report</div>', unsafe_allow_html=True)
        st.markdown("Download a professional executive summary with charts, metrics, and insights.")

        if len(df_filtered) > 0:
            try:
                temp_pdf_path = "output/temp_hr_report.pdf"
                import os
                os.makedirs("output", exist_ok=True)

                with st.spinner("Generating professional PDF report..."):
                    pdf_path, csv_path = pdf_report.generate_hr_report(
                        df_filtered,
                        temp_pdf_path,
                        cleaning_summary=summary,
                        model_accuracy=accuracy if 'accuracy' in locals() else None,
                        export_csv=True
                    )

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Export",
                        data=pdf_file,
                        file_name="HR_Executive_Summary.pdf",
                        mime="application/pdf"
                    )
            except Exception as pdf_error:
                st.error(f"PDF generation failed: {str(pdf_error)}")
                import traceback
                st.code(traceback.format_exc())
        else:
            st.warning("No employees match your current filters. Adjust filters to generate a report.")

    except Exception as e:
        st.error("An error occurred during processing. Please check your data and try again.")
        import traceback
        st.code(traceback.format_exc())

else:
    st.markdown(
        """
        <div class="info-box">
            <strong>Get Started</strong><br>
            Upload a CSV file with your HR data to begin. The dashboard will automatically clean your data and provide AI-powered insights.
        </div>
        """,
        unsafe_allow_html=True
    )