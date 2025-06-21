from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import MODEL_VERSION,model,predict_data
from schema.Input_data import Input_Data
from schema.response_data import Response_Data

app=FastAPI()


@app.get("/")
def home():
    return {"message":"This is an Insurance Premium Predictor API -  Author - Zeeshan Aftab"}

@app.get("/health")
def health():
    return {
        "status":"OK",
        "version":MODEL_VERSION,
        "model_loaded":model is not None

    }

@app.post("/predict",response_model=Response_Data)
def predict(input_data : Input_Data):
    
    data={
        'bmi': input_data.bmi,
        'age_group': input_data.age_group,
        'life_style_risk': input_data.life_style_risk,
        'city_tier': input_data.city_tier,
        'income_lpa': input_data.income_lpa,
        'occupation': input_data.occupation
    }
    try:

        prediction=predict_data(data)
        return JSONResponse(status_code=200,content={"message" : f"response : {prediction}"})
    except(e):

        return JSONResponse(status_code=501,content={"message" : str(e)})