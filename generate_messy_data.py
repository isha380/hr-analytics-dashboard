"""
Generate a LARGE, MESSY HR dataset (1000+ records) with realistic noise.
This will naturally prevent ML overfitting and give realistic 70-85% accuracy.
"""

import pandas as pd
import random
import numpy as np

# Set seed for reproducibility (but you can remove this for true randomness)
random.seed(42)
np.random.seed(42)

# Configuration
NUM_EMPLOYEES = 1200  # Large dataset!

# Pools of data
departments = ['Sales', 'R&D', 'Human Resources', 'IT', 'Finance', 'Marketing', 'Operations']
job_roles = {
    'Sales': ['Sales Executive', 'Sales Representative', 'Sales Manager'],
    'R&D': ['Research Scientist', 'Lab Technician', 'Research Director'],
    'Human Resources': ['HR Representative', 'HR Manager', 'Recruiter'],
    'IT': ['Software Engineer', 'IT Support', 'Data Analyst', 'DevOps Engineer'],
    'Finance': ['Accountant', 'Financial Analyst', 'Finance Manager'],
    'Marketing': ['Marketing Specialist', 'Marketing Manager', 'Content Creator'],
    'Operations': ['Operations Manager', 'Supply Chain Analyst', 'Logistics Coordinator']
}

genders = ['Male', 'Female']
education_fields = ['Computer Science', 'Business', 'Engineering', 'Psychology', 'Marketing', 'Finance', 'HR Management']
marital_statuses = ['Single', 'Married', 'Divorced']

positive_comments = [
    "Great work life balance and love the team.",
    "Management is very supportive and I enjoy my projects.",
    "Excellent benefits and a positive office culture.",
    "I feel valued here and see a clear path for growth.",
    "Collaborative environment, very happy with my role.",
    "Amazing opportunities for learning and development.",
    "Love the flexibility and remote work options."
]

neutral_comments = [
    "Work is okay, could be better.",
    "The job is stable but lacks excitement.",
    "Decent pay, but the commute is a bit long.",
    "Tasks are repetitive, but the team is nice.",
    "It's an average place to work, nothing special.",
    "Some days are good, some days are not.",
    "It's a job, pays the bills."
]

negative_comments = [
    "Too much stress and bad management.",
    "I feel burnt out and underappreciated.",
    "Lack of communication from upper leadership.",
    "Workload is unmanageable, looking for other options.",
    "Toxic environment, no work-life balance.",
    "No growth opportunities, feeling stuck.",
    "Underpaid and overworked.",
    "Management plays favorites."
]

# Generate the dataset
data = {
    'Age': [],
    'Gender': [],
    'Department': [],
    'JobRole': [],
    'MonthlyIncome': [],
    'YearsAtCompany': [],
    'YearsInCurrentRole': [],
    'TotalWorkingYears': [],
    'NumCompaniesWorked': [],
    'OverTime': [],
    'EducationField': [],
    'MaritalStatus': [],
    'DistanceFromHome': [],
    'JobSatisfaction': [],
    'WorkLifeBalance': [],
    'EnvironmentSatisfaction': [],
    'JobInvolvement': [],
    'PerformanceRating': [],
    'Attrition': [],
    'Feedback': [],
    'AnnualLeaveTaken': [],
    'SickLeaveTaken': [],
    'AbsenteeismRate': []
}

for i in range(NUM_EMPLOYEES):
    # Basic demographics
    age = random.randint(22, 62)
    gender = random.choice(genders)
    dept = random.choice(departments)
    role = random.choice(job_roles[dept])
    
    # Experience
    years_at_company = random.randint(0, min(20, age - 22))
    years_in_role = random.randint(0, years_at_company)
    total_working_years = random.randint(max(0, age - 25), age - 18)
    num_companies = random.randint(1, 10)
    
    # Income (with some realism - varies by role and experience)
    base_salary = {
        'Sales Executive': 5000, 'Sales Representative': 3500, 'Sales Manager': 12000,
        'Research Scientist': 6000, 'Lab Technician': 4000, 'Research Director': 15000,
        'HR Representative': 4000, 'HR Manager': 10000, 'Recruiter': 4500,
        'Software Engineer': 7000, 'IT Support': 4000, 'Data Analyst': 6000, 'DevOps Engineer': 8000,
        'Accountant': 5000, 'Financial Analyst': 6500, 'Finance Manager': 11000,
        'Marketing Specialist': 4500, 'Marketing Manager': 9000, 'Content Creator': 4000,
        'Operations Manager': 8000, 'Supply Chain Analyst': 5500, 'Logistics Coordinator': 4500
    }
    
    income = base_salary.get(role, 5000) + (years_at_company * 200) + random.randint(-2000, 3000)
    income = max(2000, min(income, 25000))  # Cap between 2k and 25k
    
    # Overtime (somewhat random)
    overtime = 'Yes' if random.random() < 0.35 else 'No'
    
    # Job satisfaction and work-life balance (1-5 scale)
    job_satisfaction = random.randint(1, 5)
    work_life_balance = random.randint(1, 5)
    env_satisfaction = random.randint(1, 5)
    job_involvement = random.randint(1, 5)
    performance_rating = random.randint(1, 5)
    
    # Distance from home
    distance = random.randint(1, 28)
    
    # Education and marital status
    edu_field = random.choice(education_fields)
    marital = random.choice(marital_statuses)
    
    # ATTRITION LOGIC (with MESSY, REALISTIC PROBABILITIES)
    # Multiple factors influence attrition, but none are deterministic
    
    attrition_probability = 0.15  # Base 15% chance
    
    # Factors that INCREASE attrition probability
    if job_satisfaction <= 2:
        attrition_probability += 0.25
    if work_life_balance <= 2:
        attrition_probability += 0.20
    if env_satisfaction <= 2:
        attrition_probability += 0.15
    if overtime == 'Yes':
        attrition_probability += 0.10
    if years_at_company < 2:
        attrition_probability += 0.10  # New employees leave more
    if income < 4000:
        attrition_probability += 0.10
    if distance > 15:
        attrition_probability += 0.05
    
    # Factors that DECREASE attrition probability
    if job_satisfaction >= 4:
        attrition_probability -= 0.15
    if work_life_balance >= 4:
        attrition_probability -= 0.15
    if income > 8000:
        attrition_probability -= 0.10
    if years_at_company > 10:
        attrition_probability -= 0.10  # Loyal employees stay
    
    # Cap probability between 5% and 70%
    attrition_probability = max(0.05, min(0.70, attrition_probability))
    
    # Decide attrition based on probability
    will_leave = random.random() < attrition_probability
    attrition = 'Yes' if will_leave else 'No'
    
    # FEEDBACK LOGIC (messy - not perfectly correlated with attrition)
    if attrition == 'Yes':
        # 60% negative, 25% neutral, 15% positive (some leave for good reasons)
        feedback_roll = random.random()
        if feedback_roll < 0.60:
            feedback = random.choice(negative_comments)
        elif feedback_roll < 0.85:
            feedback = random.choice(neutral_comments)
        else:
            feedback = random.choice(positive_comments)
    else:
        # 70% positive, 25% neutral, 5% negative (some stay despite unhappiness)
        feedback_roll = random.random()
        if feedback_roll < 0.70:
            feedback = random.choice(positive_comments)
        elif feedback_roll < 0.95:
            feedback = random.choice(neutral_comments)
        else:
            feedback = random.choice(negative_comments)
    
    # LEAVE DATA (messy - weak correlation with attrition)
    if attrition == 'Yes':
        # 50% high sick leave, 50% normal (many reasons to leave)
        if random.random() < 0.50:
            annual_leave = random.randint(0, 6)
            sick_leave = random.randint(8, 20)
        else:
            annual_leave = random.randint(8, 18)
            sick_leave = random.randint(1, 5)
    else:
        # 80% healthy pattern, 20% high sick leave (some stay despite illness)
        if random.random() < 0.80:
            annual_leave = random.randint(10, 22)
            sick_leave = random.randint(0, 4)
        else:
            annual_leave = random.randint(3, 10)
            sick_leave = random.randint(6, 15)
    
    absenteeism_rate = round((sick_leave / 250) * 100, 2)
    
    # Append to data
    data['Age'].append(age)
    data['Gender'].append(gender)
    data['Department'].append(dept)
    data['JobRole'].append(role)
    data['MonthlyIncome'].append(income)
    data['YearsAtCompany'].append(years_at_company)
    data['YearsInCurrentRole'].append(years_in_role)
    data['TotalWorkingYears'].append(total_working_years)
    data['NumCompaniesWorked'].append(num_companies)
    data['OverTime'].append(overtime)
    data['EducationField'].append(edu_field)
    data['MaritalStatus'].append(marital)
    data['DistanceFromHome'].append(distance)
    data['JobSatisfaction'].append(job_satisfaction)
    data['WorkLifeBalance'].append(work_life_balance)
    data['EnvironmentSatisfaction'].append(env_satisfaction)
    data['JobInvolvement'].append(job_involvement)
    data['PerformanceRating'].append(performance_rating)
    data['Attrition'].append(attrition)
    data['Feedback'].append(feedback)
    data['AnnualLeaveTaken'].append(annual_leave)
    data['SickLeaveTaken'].append(sick_leave)
    data['AbsenteeismRate'].append(absenteeism_rate)

# Create DataFrame
df = pd.DataFrame(data)

# Add some MISSING VALUES (realistic messiness)
missing_indices = random.sample(range(len(df)), int(len(df) * 0.03))  # 3% missing
for idx in missing_indices:
    col_to_null = random.choice(['JobSatisfaction', 'WorkLifeBalance', 'DistanceFromHome', 'EnvironmentSatisfaction'])
    df.loc[idx, col_to_null] = np.nan

# Add some DUPLICATES (2% duplicates)
num_duplicates = int(len(df) * 0.02)
duplicate_indices = random.sample(range(len(df)), num_duplicates)
duplicates = df.iloc[duplicate_indices]
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle the data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
df.to_csv("data/hr_data_messy.csv", index=False)

print(f"✅ Successfully created 'data/hr_data_messy.csv'!")
print(f"   Total Records: {len(df):,}")
print(f"   Attrition Rate: {(df['Attrition'] == 'Yes').mean()*100:.1f}%")
print(f"   Missing Values: {df.isnull().sum().sum()}")
print(f"   Columns: {', '.join(df.columns)}")