import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load Dataset
data = pd.read_csv("dataset/student.csv")

# Input Features
X = data[[
    "StudyHours",
    "Attendance",
    "InternalMarks",
    "Assignment"
]]

# Output
y = data["Performance"]

# Train Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Create model folder
os.makedirs("model", exist_ok=True)

# Save Model
joblib.dump(model, "model/model.pkl")

print("✅ Machine Learning Model Trained Successfully")