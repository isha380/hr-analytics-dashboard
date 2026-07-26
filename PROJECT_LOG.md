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