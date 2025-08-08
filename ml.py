from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

app = Flask(__name__)

# Load and preprocess dataset
df = pd.read_excel("Dataset.csv.xlsx")

def clean_symptoms(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r"[;]", ",", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    return ""

df['Symptoms'] = df['Symptoms'].apply(clean_symptoms)

X = df[['Age', 'Symptoms']]
y = df['Disease']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['Age']),
    ('text', TfidfVectorizer(), 'Symptoms')
])

model_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model_pipeline.fit(X_train, y_train)

@app.route('/')
def home():
    # Serve frontend HTML page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        age = int(data.get('age', ''))
        symptoms = data.get('symptoms', '')
        cleaned = clean_symptoms(symptoms)
        input_df = pd.DataFrame([{'Age': age, 'Symptoms': cleaned}])
        prediction = model_pipeline.predict(input_df)[0]
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Debug off to avoid socket-related issues
    app.run(debug=False)
