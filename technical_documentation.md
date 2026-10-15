# HR Analytics Dashboard 

## 1. Project Overview

The HR Analytics Dashboard is a Python-based web application built with Streamlit. It helps users clean, filter, analyze, and visualize HR data. It also includes attrition risk prediction, employee feedback sentiment analysis, and PDF report generation.

The project is organized into separate Python modules, with each module handling a specific task.

## 2. Tools and Technologies

- **Python:** Main programming language.
- **Streamlit:** Dashboard interface.
- **Pandas:** Data cleaning and analysis.
- **Plotly:** Charts and visualizations.
- **Scikit-learn:** Random Forest classification and model evaluation.
- **TextBlob:** Basic sentiment analysis.
- **ReportLab:** PDF report generation.
- **Kaleido:** Exporting charts as images for PDF reports.

## 3. Data Cleaning

The cleaning module reads uploaded CSV files and checks for three required columns: Age, Department, and Attrition.

It removes duplicate rows, standardizes text formatting in selected columns, and fills missing numeric values with the median. Missing text values are filled with the most frequent value or “Unknown” when no mode is available.

The dashboard displays a summary of the cleaning process. One detail to improve is that the current “Missing Values Filled” figure also counts text-formatting corrections.

## 4. Interactive Dashboard

Users can filter records by Department and JobRole. The dashboard updates its analysis based on the selected records and displays the number of records remaining.

The current version supports CSV uploads only.

## 5. Attrition Risk Prediction

The attrition module prepares the data, converts categorical variables into numerical columns, and trains a Random Forest classifier using an 80/20 train-test split.

It also performs five-fold cross-validation. The accuracy displayed on the dashboard is the average cross-validation score, not the test-set accuracy.

The model's predicted probabilities are used to group records into high-, medium-, and low-risk categories. These categories are estimates, not guarantees that an employee will leave.

## 6. Employee Feedback Sentiment Analysis

The sentiment module uses predefined positive and negative keywords along with TextBlob to analyze employee feedback. It assigns a sentiment score and classifies feedback as positive, neutral, or negative.

This is a basic approach and may not correctly understand sarcasm or complex sentences.

## 7. Analytics Modules

**Leave and Absenteeism:** Calculates average annual leave, sick leave, and absenteeism rates by department. It also identifies records with the highest absenteeism rates. These results show patterns in the data but do not explain why absenteeism occurs.

**Diversity and Demographics:** Counts gender distribution across job roles and calculates average, median, minimum, and maximum ages by department. These results provide a basic overview of workforce demographics.

**Compensation:** Calculates average monthly income by job role and gender. It also supports visual comparisons of income and years at the company. Differences in average pay may need further investigation and do not automatically prove unequal pay.

**Charts and Correlation:** Generates department counts, an age histogram, an attrition pie chart, and a correlation heatmap. The heatmap shows relationships between numeric variables, but correlation does not prove causation.

## 8. PDF Report Generation

The reporting module uses ReportLab to generate a PDF containing an executive summary, data-cleaning results, analytics, charts, automatically generated insights, recommendations, and a small data preview.

It can also export the analyzed dataset to a timestamped CSV file. Employee-level information should be checked carefully before sharing these files.

## 9. Limitations and Future Improvements

- Display test-set accuracy separately from cross-validation accuracy.
- Evaluate the model using additional metrics, such as precision, recall, and a confusion matrix.
- Improve input validation and handling of missing columns.
- Improve sentiment analysis for more complex feedback.
- Make the risk thresholds consistent across the dashboard and PDF report.
- Review automatically generated insights before using them to make HR decisions.
- Protect employee information in reports and exported files.

## 10. Conclusion

The project combines data cleaning, visualization, workforce analytics, basic sentiment analysis, attrition risk prediction, and PDF reporting in one application. It demonstrates how Python tools can help organize HR data and identify patterns for further investigation. The results still need to be checked before being used to make workplace decisions.
