from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load ML model once at startup
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from HTML form
    age = int(request.form['age'])
    symptoms = request.form['symptoms']
    
    # Preprocess and prepare input for model
    input_df = pd.DataFrame([{'Age': age, 'Symptoms': symptoms}])
    
    # Run model prediction
    prediction = model.predict(input_df)[0]
    
    # Render results page with prediction displayed
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
