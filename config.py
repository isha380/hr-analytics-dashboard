"""
Configuration settings for the HR Analytics Dashboard.
Central place for constants, paths, and settings.
"""

# File paths
DATA_FOLDER = "data"
DEFAULT_CSV_FILE = "hr_data.csv"

# Data cleaning settings
DUPLICATE_COLUMNS = None  # Check all columns for duplicates
NUMERIC_FILL_METHOD = "median"  # Options: "mean", "median", "zero"
TEXT_FILL_VALUE = "Unknown"

# Chart settings
DEFAULT_CHART_THEME = "plotly_white"
COLOR_PALETTE = {
    "primary": "#3b82f6",      # Blue
    "success": "#10b981",      # Green
    "danger": "#ef4444",       # Red
    "warning": "#f59e0b",      # Orange
}