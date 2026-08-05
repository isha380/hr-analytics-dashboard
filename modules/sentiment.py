# """
# Sentiment Analysis module for HR Analytics.
# Uses TextBlob to analyze employee feedback and categorize it.
# """

# from textblob import TextBlob
import pandas as pd

# def analyze_text_sentiment(text):
#     """
#     Analyzes a single piece of text and returns a polarity score.
    
#     Input: A string of text (e.g., "Great work environment")
#     Output: A float between -1.0 (Negative) and 1.0 (Positive)
#     """
#     if pd.isna(text) or text == "Unknown":
#         return 0.0 # Neutral if no text
    
#     # TextBlob calculates the polarity
#     return TextBlob(str(text)).sentiment.polarity

# def categorize_sentiment(score):
#     """
#     Converts a decimal polarity score into a human-readable category.
    
#     Input: Float between -1.0 and 1.0
#     Output: String ('Positive', 'Neutral', 'Negative')
#     """
#     if score > 0.1:
#         return 'Positive'
#     elif score < -0.1:
#         return 'Negative'
#     else:
#         return 'Neutral'

# def process_feedback_column(df, text_column='Feedback'):
#     """
#     Main function to process an entire column of text data.
#     Adds 'Sentiment_Score' and 'Sentiment_Category' to the dataframe.
#     """
#     # Check if the column exists. If not, we'll handle it in the app.
#     if text_column not in df.columns:
#         return df
        
#     # 1. Calculate the score for every row
#     df['Sentiment_Score'] = df[text_column].apply(analyze_text_sentiment)
    
#     # 2. Categorize the score
#     df['Sentiment_Category'] = df['Sentiment_Score'].apply(categorize_sentiment)
    
#     return df

from textblob import TextBlob


def analyze_text_sentiment(text):
    """
    Analyzes text using a hybrid approach with negation handling.
    """
    if pd.isna(text) or text == "Unknown":
        return 0.0
    
    # Convert to lowercase for easier matching
    text_lower = str(text).lower()
    
    # 1. STRONG NEGATION DETECTION
    # Check for negation patterns that flip the meaning
    negation_words = ["don't", "dont", "not", "never", "no", "neither", "nobody", "nothing"]
    
    # If the sentence contains negation + a positive word, it's actually negative!
    positive_words = ['enjoy', 'love', 'great', 'excellent', 'amazing', 'valued', 'supportive', 'happy', 'good']
    
    has_negation = any(neg in text_lower for neg in negation_words)
    has_positive = any(pos in text_lower for pos in positive_words)
    
    # If we have BOTH negation AND positive words, it's negative
    # Example: "I don't enjoy" = negative
    if has_negation and has_positive:
        return -0.6
    
    # 2. Check for strong domain-specific negative keywords
    strong_negative_words = ['burnt out', 'underappreciated', 'toxic', 'terrible', 'hate', 'worst', 'stress', 'dislike', 'bad', 'poor']
    
    for word in strong_negative_words:
        if word in text_lower:
            return -0.8  # Force negative
            
    # 3. Check for strong positive keywords (without negation)
    strong_positive_words = ['love', 'great', 'excellent', 'amazing', 'valued', 'supportive']
    
    if not has_negation:  # Only if there's no negation
        for word in strong_positive_words:
            if word in text_lower:
                return 0.8
    
    # 4. Fallback to TextBlob
    return TextBlob(text).sentiment.polarity

def categorize_sentiment(score):
    """
    Converts a decimal polarity score into a human-readable category.
    
    Input: Float between -1.0 and 1.0
    Output: String ('Positive', 'Neutral', 'Negative')
    """
    if score > 0.1:
        return 'Positive'
    elif score < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

def process_feedback_column(df, text_column='Feedback'):
    """
    Main function to process an entire column of text data.
    Adds 'Sentiment_Score' and 'Sentiment_Category' to the dataframe.
    """
    # Check if the column exists. If not, we'll handle it in the app.
    if text_column not in df.columns:
        return df
        
    # 1. Calculate the score for every row
    df['Sentiment_Score'] = df[text_column].apply(analyze_text_sentiment)
    
    # 2. Categorize the score
    df['Sentiment_Category'] = df['Sentiment_Score'].apply(categorize_sentiment)
    
    return df