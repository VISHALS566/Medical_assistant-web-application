import pickle
import pandas as pd
import re

# Load model once when imported
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def clean_symptoms(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[;]", ",", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    return ""

def predict_disease(age, symptoms):
    symptoms_clean = clean_symptoms(symptoms)
    input_df = pd.DataFrame([{'Age': age, 'Symptoms': symptoms_clean}])
    prediction = model.predict(input_df)
    return prediction[0]
