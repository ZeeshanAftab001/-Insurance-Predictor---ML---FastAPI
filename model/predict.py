import pickle
import pandas as pd

MODEL_VERSION="1.0.0"

with open("model/model.pkl","rb") as f:
    model = pickle.load(f)

class_labels=model.classes_.tolist()

def predict_data(data : dict):
    
    df=pd.DataFrame([data])

    probabilities=model.predict_proba(df)[0]
    confidence=max(probabilities)

    class_probabilities=dict(zip(class_labels,map(lambda p : round(p,4),probabilities)))
    return {
        "Prediction : ":model.predict(df)[0],
        "Confidence : ":round(confidence,4),
        "class_probabilities : ":class_probabilities
    }