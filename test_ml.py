import pandas as pd
from modules.attrition import prepare_ml_data, train_attrition_model

# Load your dummy data
df = pd.read_csv("data/hr_data.csv")

# Prepare and Train
X, y, encoder = prepare_ml_data(df)
model, accuracy = train_attrition_model(X, y)

print(f"✅ Model trained successfully!")
print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")