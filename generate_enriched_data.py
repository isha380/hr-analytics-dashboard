"""
Script to generate a realistic dummy HR dataset with employee feedback and leave data.
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

# 3. Assign feedback based on Attrition and OverTime
feedback_list = []

for index, row in df.iterrows():
    left_company = row['Attrition'] == 'Yes'
    does_overtime = row['OverTime'] == 'Yes'
    
    if left_company:
        comment = random.choice(negative_comments)
    elif does_overtime:
        comment = random.choice(neutral_comments)
    else:
        comment = random.choice(positive_comments)
        
    feedback_list.append(comment)

df['Feedback'] = feedback_list

# 4. Generate Leave and Absenteeism Data
annual_leave = []
sick_leave = []
absenteeism_rate = []

for index, row in df.iterrows():
    left_company = row['Attrition'] == 'Yes'
    does_overtime = row['OverTime'] == 'Yes'
    
    # Logic: People who quit usually have high sick leave and low annual leave (burnout)
    if left_company:
        annual = random.randint(0, 5)      # Didn't take vacations
        sick = random.randint(10, 20)      # Called in sick often
    elif does_overtime:
        annual = random.randint(5, 12)     # Took some vacation
        sick = random.randint(3, 8)        # Occasional sick days
    else:
        annual = random.randint(10, 20)    # Healthy work-life balance
        sick = random.randint(0, 3)        # Rarely sick
        
    annual_leave.append(annual)
    sick_leave.append(sick)
    
    # Calculate absenteeism rate (Sick days / 250 working days in a year)
    rate = round((sick / 250) * 100, 2)
    absenteeism_rate.append(rate)

df['AnnualLeaveTaken'] = annual_leave
df['SickLeaveTaken'] = sick_leave
df['AbsenteeismRate'] = absenteeism_rate

# 5. Save to a new file
df.to_csv("data/hr_data_enriched.csv", index=False)

print("✅ Successfully created 'data/hr_data_enriched.csv' with feedback and leave data!")
print(f"   Columns added: Feedback, AnnualLeaveTaken, SickLeaveTaken, AbsenteeismRate")