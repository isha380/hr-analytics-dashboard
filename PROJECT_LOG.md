### Understanding: 
- "Why did you separate the code into modules?"
 *"To follow the Single Responsibility Principle. Each module has one job: cleaning.py handles data cleaning, charts.py handles visualization, and app.py handles the UI. This makes testing and maintenance easier."*
- "What is the benefit of a config file?"
*"It provides a single source of truth for settings. If I need to change colors or file paths, I edit one file instead of searching through hundreds of lines of code."*
- "Why return a summary dictionary from the cleaning function?"
*"It separates data from metadata. The caller gets both the cleaned data AND information about what was cleaned, which is useful for logging and user feedback."*

Feature: Modular Refactoring
Why: To prepare for scalable development and demonstrate professional coding practices
How: Separated UI (app.py) from business logic (modules/) and configuration (config.py)
Files: config.py, modules/cleaning.py, modules/charts.py, app.py
Key Functions: load_and_clean_data(), create_all_charts()
Interview Notes: Demonstrates understanding of Single Responsibility Principle and clean architecture

## Intelligence Features & Advanced Visualizations (Days 7-9)

**Feature:**
Machine Learning Attrition Prediction, NLP Sentiment Analysis, and Interactive Dashboard.

**Why:**
HR needs to predict who is likely to quit, understand employee morale through unstructured feedback, and dynamically filter data to find specific trends.

**How:**
- Used Random Forest Classifier for attrition prediction.
- Used TextBlob with custom keyword overrides and negation handling for sentiment analysis.
- Added Streamlit sidebar multiselect filters to dynamically slice the dataframe.
- Added a Plotly correlation heatmap to visualize relationships between numeric features.

**Files:**
`modules/attrition.py`, `modules/sentiment.py`, `modules/charts.py`, `app.py`, `generate_enriched_data.py`

**Key Functions:**
`prepare_ml_data()`, `train_attrition_model()`, `analyze_text_sentiment()`, `create_correlation_heatmap()`

**Edge Cases Handled:**
- **ML Crash:** Dropped text columns (like 'Feedback') before feeding data to the ML model.
- **NLP Context:** Added custom logic to handle negation (e.g., "don't enjoy") and corporate slang (e.g., "burnt out").
- **Empty Filters:** Added safety checks (`if len(df_filtered) > 0`) to prevent Plotly and Pandas from crashing when sidebar filters return zero employees.

**Interview Notes:**
- Explained the difference between `predict` (binary 0/1) and `predict_proba` (continuous probability score).
- Explained the "Dummy Variable Trap" and why we use `drop_first=True` in One-Hot Encoding.
- Acknowledged that TextBlob is a baseline and production systems would use Transformer models (like BERT) for better context understanding.