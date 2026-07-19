import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of dummy employees
num_employees = 150

# Generate dummy data matching our ER Diagram columns
data = {
    'Age': np.random.randint(22, 60, num_employees),
    'Gender': np.random.choice(['Male', 'Female'], num_employees),
    'Department': np.random.choice(['Sales', 'R&D', 'Human Resources'], num_employees),
    'JobRole': np.random.choice(['Sales Executive', 'Research Scientist', 'Manager', 'HR Representative'], num_employees),
    'MonthlyIncome': np.random.randint(3000, 20000, num_employees),
    'YearsAtCompany': np.random.randint(0, 20, num_employees),
    'OverTime': np.random.choice(['Yes', 'No'], num_employees, p=[0.3, 0.7]),
    'Attrition': np.random.choice(['Yes', 'No'], num_employees, p=[0.2, 0.8])
}

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('hr_data.csv', index=False)

print("✅ Dummy 'hr_data.csv' created successfully!")