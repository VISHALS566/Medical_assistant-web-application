import pandas as pd
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

# Clean symptoms function
def clean_symptoms(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[;]", ",", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    return ""

# Load dataset
df = pd.read_excel("Dataset.csv.xlsx")
df['Symptoms'] = df['Symptoms'].apply(clean_symptoms)

# Features & labels
X = df[['Age', 'Symptoms']]
y = df['Disease']

# Preprocessing
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['Age']),
    ('text', TfidfVectorizer(), 'Symptoms')
])

# Pipeline
model_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model_pipeline.fit(X_train, y_train)

# Save the trained model
with open('model.pkl', 'wb') as f:
    pickle.dump(model_pipeline, f)

print("✅ Model saved as model.pkl")
