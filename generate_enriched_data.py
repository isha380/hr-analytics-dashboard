"""
Script to generate a realistic dummy HR dataset with employee feedback.
"""

import pandas as pd
import random

# 1. Load the existing dummy data
df = pd.read_csv("data/hr_data.csv")

# 2. Create pools of realistic feedback comments
positive_comments = [
    "Great work life balance and love the team.",
    "Management is very supportive and I enjoy my projects.",
    "Excellent benefits and a positive office culture.",
    "I feel valued here and see a clear path for growth.",
    "Collaborative environment, very happy with my role."
]

neutral_comments = [
    "Work is okay, could be better.",
    "The job is stable but lacks excitement.",
    "Decent pay, but the commute is a bit long.",
    "Tasks are repetitive, but the team is nice.",
    "It's an average place to work, nothing special."
]

negative_comments = [
    "Too much stress and bad management.",
    "I feel burnt out and underappreciated.",
    "Lack of communication from upper leadership.",
    "Workload is unmanageable, looking for other options.",
    "Toxic environment, no work-life balance."
]

# 3. Assign feedback based on Attrition and OverTime (Columns we actually have!)
feedback_list = []

for index, row in df.iterrows():
    left_company = row['Attrition'] == 'Yes'
    does_overtime = row['OverTime'] == 'Yes'
    
    # Logic: If they left, they are definitely unhappy.
    if left_company:
        comment = random.choice(negative_comments)
    # If they work overtime but stayed, they might be neutral/stressed.
    elif does_overtime:
        comment = random.choice(neutral_comments)
    # If they stayed and don't work overtime, they are likely happy.
    else:
        comment = random.choice(positive_comments)
        
    feedback_list.append(comment)

# 4. Add the new column and save
df['Feedback'] = feedback_list

# Save to a new file so we don't overwrite our original clean data
df.to_csv("data/hr_data_enriched.csv", index=False)

print("✅ Successfully created 'data/hr_data_enriched.csv' with realistic feedback!")