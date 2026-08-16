"""
Generate a messy HR dataset with 1000+ records for realistic ML testing.
"""

import pandas as pd
import random
import numpy as np

random.seed(123)
np.random.seed(123)

NUM_EMPLOYEES = 1000

# Data pools
departments = ['Sales', 'R&D', 'Human Resources', 'IT', 'Finance']
job_roles_by_dept = {
    'Sales': ['Sales Executive', 'Sales Manager'],
    'R&D': ['Research Scientist', 'Lab Technician'],
    'Human Resources': ['HR Representative', 'HR Manager'],
    'IT': ['Software Engineer', 'IT Support'],
    'Finance': ['Accountant', 'Financial Analyst']
}

genders = ['Male', 'Female']
education_fields = ['Computer Science', 'Business', 'Engineering', 'Psychology', 'Marketing']
marital_statuses = ['Single', 'Married', 'Divorced']

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

# Generate data
data = []

for i in range(NUM_EMPLOYEES):
    age = random.randint(22, 60)
    gender = random.choice(genders)
    dept = random.choice(departments)
    role = random.choice(job_roles_by_dept[dept])
    
    years_at_company = random.randint(0, min(15, age - 22))
    monthly_income = random.randint(3000, 15000) + (years_at_company * 150)
    overtime = 'Yes' if random.random() < 0.3 else 'No'
    
    # Job satisfaction (1-5)
    job_satisfaction = random.randint(1, 5)
    work_life_balance = random.randint(1, 5)
    
    # ATTRITION with realistic probabilities
    attrition_prob = 0.15  # Base rate
    
    if job_satisfaction <= 2:
        attrition_prob += 0.25
    if work_life_balance <= 2:
        attrition_prob += 0.20
    if overtime == 'Yes':
        attrition_prob += 0.10
    if monthly_income < 5000:
        attrition_prob += 0.10
    if job_satisfaction >= 4:
        attrition_prob -= 0.15
    if work_life_balance >= 4:
        attrition_prob -= 0.15
    
    attrition_prob = max(0.05, min(0.65, attrition_prob))
    attrition = 'Yes' if random.random() < attrition_prob else 'No'
    
    # FEEDBACK (messy correlation)
    if attrition == 'Yes':
        roll = random.random()
        if roll < 0.60:
            feedback = random.choice(negative_comments)
        elif roll < 0.85:
            feedback = random.choice(neutral_comments)
        else:
            feedback = random.choice(positive_comments)
    else:
        roll = random.random()
        if roll < 0.70:
            feedback = random.choice(positive_comments)
        elif roll < 0.95:
            feedback = random.choice(neutral_comments)
        else:
            feedback = random.choice(negative_comments)
    
    # LEAVE DATA (weak correlation)
    if attrition == 'Yes':
        if random.random() < 0.55:
            annual_leave = random.randint(0, 5)
            sick_leave = random.randint(8, 18)
        else:
            annual_leave = random.randint(8, 18)
            sick_leave = random.randint(1, 5)
    else:
        if random.random() < 0.80:
            annual_leave = random.randint(10, 20)
            sick_leave = random.randint(0, 3)
        else:
            annual_leave = random.randint(3, 10)
            sick_leave = random.randint(4, 10)
    
    absenteeism_rate = round((sick_leave / 250) * 100, 2)
    
    data.append({
        'Age': age,
        'Gender': gender,
        'Department': dept,
        'JobRole': role,
        'MonthlyIncome': monthly_income,
        'YearsAtCompany': years_at_company,
        'OverTime': overtime,
        'JobSatisfaction': job_satisfaction,
        'WorkLifeBalance': work_life_balance,
        'Attrition': attrition,
        'Feedback': feedback,
        'AnnualLeaveTaken': annual_leave,
        'SickLeaveTaken': sick_leave,
        'AbsenteeismRate': absenteeism_rate
    })

df = pd.DataFrame(data)

# Add 3% missing values
missing_count = int(len(df) * 0.03)
missing_indices = random.sample(range(len(df)), missing_count)
for idx in missing_indices:
    col = random.choice(['JobSatisfaction', 'WorkLifeBalance', 'Age'])
    df.loc[idx, col] = np.nan

# Add 2% duplicates
dup_count = int(len(df) * 0.02)
dup_indices = random.sample(range(len(df)), dup_count)
duplicates = df.iloc[dup_indices]
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
df.to_csv("data/hr_data_test.csv", index=False)

print(f"✅ Created 'data/hr_data_test.csv'")
print(f"   Records: {len(df):,}")
print(f"   Attrition Rate: {(df['Attrition'] == 'Yes').mean()*100:.1f}%")
print(f"   Missing Values: {df.isnull().sum().sum()}")