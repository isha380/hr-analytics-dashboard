# """
# Generate a messy HR dataset with 1000+ records for realistic ML testing.
# """

# import pandas as pd
# import random
# import numpy as np

# random.seed(123)
# np.random.seed(123)

# NUM_EMPLOYEES = 1000

# # Data pools
# departments = ['Sales', 'R&D', 'Human Resources', 'IT', 'Finance']
# job_roles_by_dept = {
#     'Sales': ['Sales Executive', 'Sales Manager'],
#     'R&D': ['Research Scientist', 'Lab Technician'],
#     'Human Resources': ['HR Representative', 'HR Manager'],
#     'IT': ['Software Engineer', 'IT Support'],
#     'Finance': ['Accountant', 'Financial Analyst']
# }

# genders = ['Male', 'Female']
# education_fields = ['Computer Science', 'Business', 'Engineering', 'Psychology', 'Marketing']
# marital_statuses = ['Single', 'Married', 'Divorced']

# positive_comments = [
#     "Great work life balance and love the team.",
#     "Management is very supportive and I enjoy my projects.",
#     "Excellent benefits and a positive office culture.",
#     "I feel valued here and see a clear path for growth.",
#     "Collaborative environment, very happy with my role."
# ]

# neutral_comments = [
#     "Work is okay, could be better.",
#     "The job is stable but lacks excitement.",
#     "Decent pay, but the commute is a bit long.",
#     "Tasks are repetitive, but the team is nice.",
#     "It's an average place to work, nothing special."
# ]

# negative_comments = [
#     "Too much stress and bad management.",
#     "I feel burnt out and underappreciated.",
#     "Lack of communication from upper leadership.",
#     "Workload is unmanageable, looking for other options.",
#     "Toxic environment, no work-life balance."
# ]

# # Generate data
# data = []

# for i in range(NUM_EMPLOYEES):
#     age = random.randint(22, 60)
#     gender = random.choice(genders)
#     dept = random.choice(departments)
#     role = random.choice(job_roles_by_dept[dept])
    
#     years_at_company = random.randint(0, min(15, age - 22))
#     monthly_income = random.randint(3000, 15000) + (years_at_company * 150)
#     overtime = 'Yes' if random.random() < 0.3 else 'No'
    
#     # Job satisfaction (1-5)
#     job_satisfaction = random.randint(1, 5)
#     work_life_balance = random.randint(1, 5)
    
#     # ATTRITION with realistic probabilities
#     attrition_prob = 0.15  # Base rate
    
#     if job_satisfaction <= 2:
#         attrition_prob += 0.25
#     if work_life_balance <= 2:
#         attrition_prob += 0.20
#     if overtime == 'Yes':
#         attrition_prob += 0.10
#     if monthly_income < 5000:
#         attrition_prob += 0.10
#     if job_satisfaction >= 4:
#         attrition_prob -= 0.15
#     if work_life_balance >= 4:
#         attrition_prob -= 0.15
    
#     attrition_prob = max(0.05, min(0.65, attrition_prob))
#     attrition = 'Yes' if random.random() < attrition_prob else 'No'
    
#     # FEEDBACK (messy correlation)
#     if attrition == 'Yes':
#         roll = random.random()
#         if roll < 0.60:
#             feedback = random.choice(negative_comments)
#         elif roll < 0.85:
#             feedback = random.choice(neutral_comments)
#         else:
#             feedback = random.choice(positive_comments)
#     else:
#         roll = random.random()
#         if roll < 0.70:
#             feedback = random.choice(positive_comments)
#         elif roll < 0.95:
#             feedback = random.choice(neutral_comments)
#         else:
#             feedback = random.choice(negative_comments)
    
#     # LEAVE DATA (weak correlation)
#     if attrition == 'Yes':
#         if random.random() < 0.55:
#             annual_leave = random.randint(0, 5)
#             sick_leave = random.randint(8, 18)
#         else:
#             annual_leave = random.randint(8, 18)
#             sick_leave = random.randint(1, 5)
#     else:
#         if random.random() < 0.80:
#             annual_leave = random.randint(10, 20)
#             sick_leave = random.randint(0, 3)
#         else:
#             annual_leave = random.randint(3, 10)
#             sick_leave = random.randint(4, 10)
    
#     absenteeism_rate = round((sick_leave / 250) * 100, 2)
    
#     data.append({
#         'Age': age,
#         'Gender': gender,
#         'Department': dept,
#         'JobRole': role,
#         'MonthlyIncome': monthly_income,
#         'YearsAtCompany': years_at_company,
#         'OverTime': overtime,
#         'JobSatisfaction': job_satisfaction,
#         'WorkLifeBalance': work_life_balance,
#         'Attrition': attrition,
#         'Feedback': feedback,
#         'AnnualLeaveTaken': annual_leave,
#         'SickLeaveTaken': sick_leave,
#         'AbsenteeismRate': absenteeism_rate
#     })

# df = pd.DataFrame(data)

# # Add 3% missing values
# missing_count = int(len(df) * 0.03)
# missing_indices = random.sample(range(len(df)), missing_count)
# for idx in missing_indices:
#     col = random.choice(['JobSatisfaction', 'WorkLifeBalance', 'Age'])
#     df.loc[idx, col] = np.nan

# # Add 2% duplicates
# dup_count = int(len(df) * 0.02)
# dup_indices = random.sample(range(len(df)), dup_count)
# duplicates = df.iloc[dup_indices]
# df = pd.concat([df, duplicates], ignore_index=True)

# # Shuffle
# df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# # Save
# df.to_csv("data/hr_data_test.csv", index=False)

# print(f"✅ Created 'data/hr_data_test.csv'")
# print(f"   Records: {len(df):,}")
# print(f"   Attrition Rate: {(df['Attrition'] == 'Yes').mean()*100:.1f}%")
# print(f"   Missing Values: {df.isnull().sum().sum()}")


import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

num_records = 250

# 1. Basic Demographics
employee_ids = [f"EMP{str(i).zfill(4)}" for i in range(1, num_records + 1)]
ages = np.random.randint(22, 65, num_records)
genders = np.random.choice(['Male', 'Female'], num_records, p=[0.55, 0.45])

# 2. Departments & Roles
departments = ['IT', 'HR', 'Sales', 'Marketing', 'Finance']
job_roles = {
    'IT': ['Software Developer', 'Data Analyst', 'IT Manager'],
    'HR': ['HR Specialist', 'HR Manager', 'Recruiter'],
    'Sales': ['Sales Representative', 'Account Executive', 'Sales Manager'],
    'Marketing': ['Marketing Coordinator', 'Marketing Manager', 'Content Strategist'],
    'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager']
}

dept_list = []
role_list = []
for _ in range(num_records):
    dept = random.choice(departments)
    dept_list.append(dept)
    role_list.append(random.choice(job_roles[dept]))

# 3. Compensation & Experience
monthly_incomes = np.random.randint(4000, 15000, num_records)
years_at_company = np.random.randint(0, 15, num_records)

# FIXED: Generate years with manager safely using np.minimum
years_with_current_manager = np.random.randint(0, 10, num_records)
years_with_current_manager = np.minimum(years_with_current_manager, years_at_company)

# 4. Leave & Absenteeism
sick_leave = np.random.randint(0, 10, num_records)
annual_leave = np.random.randint(0, 20, num_records)
absenteeism_rate = np.round(np.random.uniform(0.0, 0.15, num_records), 2)

# 5. OverTime
over_time = np.random.choice(['Yes', 'No'], num_records, p=[0.3, 0.7])

# 6. Attrition (Target for ML)
attrition_list = []
for i in range(num_records):
    prob = 0.15 # Base probability
    if monthly_incomes[i] < 6000: prob += 0.2
    if absenteeism_rate[i] > 0.10: prob += 0.25
    if years_at_company[i] < 2: prob += 0.15
    if over_time[i] == 'Yes': prob += 0.1
    attrition_list.append('Yes' if random.random() < prob else 'No')

# 7. Feedback (For Sentiment Analysis)
positive_feedback = [
    "I love working here, great team and culture.",
    "Excellent management and very supportive environment.",
    "Good work-life balance and fair compensation.",
    "I feel valued and have great growth opportunities."
]
negative_feedback = [
    "Too much workload and not enough support from management.",
    "Compensation is below market rate, very frustrating.",
    "Poor communication and toxic team environment.",
    "No clear career path, feeling stuck in my role."
]
neutral_feedback = [
    "It's an okay place to work, nothing special.",
    "Some good days, some bad days, average experience.",
    "The job is fine, but the benefits could be better."
]

feedback_list = []
for _ in range(num_records):
    sentiment_roll = random.random()
    if sentiment_roll < 0.4:
        feedback_list.append(random.choice(positive_feedback))
    elif sentiment_roll < 0.7:
        feedback_list.append(random.choice(negative_feedback))
    else:
        feedback_list.append(random.choice(neutral_feedback))

# Create DataFrame
df = pd.DataFrame({
    'EmployeeID': employee_ids,
    'Age': ages,
    'Gender': genders,
    'Department': dept_list,
    'JobRole': role_list,
    'MonthlyIncome': monthly_incomes,
    'YearsAtCompany': years_at_company,
    'YearsWithCurrManager': years_with_current_manager,
    'SickLeaveTaken': sick_leave,
    'AnnualLeaveTaken': annual_leave,
    'AbsenteeismRate': absenteeism_rate,
    'OverTime': over_time,
    'Feedback': feedback_list,
    'Attrition': attrition_list
})

# --- INTRODUCE INTENTIONAL ISSUES TO TEST CLEANING MODULE ---

# 1. Add exact duplicates (to test duplicate removal)
df = pd.concat([df, df.iloc[5:10]], ignore_index=True)

# 2. Add missing values (to test missing value imputation)
df.loc[15:20, 'MonthlyIncome'] = np.nan
df.loc[30:35, 'Feedback'] = np.nan
df.loc[40:42, 'Department'] = np.nan

# 3. Add some messy data (e.g., extra spaces, inconsistent casing)
df.loc[50, 'Department'] = '  it  '
df.loc[51, 'Gender'] = 'male'

# Shuffle the dataframe
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv('test_hr_data.csv', index=False)
print("✅ Successfully generated 'test_hr_data.csv' with 255 rows!")
print("You can now upload this file to your Streamlit dashboard.")