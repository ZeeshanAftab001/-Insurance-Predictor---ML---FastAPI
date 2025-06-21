from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal
import pandas as pd

app=FastAPI()

with open("model.pkl","rb") as f:
    model = pickle.load(f)

class Input_Data(BaseModel):

    age : Annotated[int,Field(...,gt=0,lt=120)]
    weight : int
    height : int
    income_lpa : float
    smoker : Annotated[bool,Field(...,description="Do you smoke? True or False",examples=["True","False"])] 
    city: Annotated[str,Field(...,description="Enter your city.")]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Enter your Occupation Please.")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height)**2

    @computed_field
    @property
    def life_style_risk(self) -> str:
        if self.bmi> 30 and self.smoker:
            return "high"
        elif self.bmi> 30 or self.smoker:
            return "medium"
        else :
            return "low"

    @computed_field
    @property
    def city_tier(self) -> int:
        tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        tier_2_cities = [
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        ]
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
     

@app.post("/predict")
def predict(input_data : Input_Data):
    
    df=pd.DataFrame([{
          'bmi': input_data.bmi,
        'age_group': input_data.age_group,
        'life_style_risk': input_data.life_style_risk,
        'city_tier': input_data.city_tier,
        'income_lpa': input_data.income_lpa,
        'occupation': input_data.occupation
    }])
    prediction=model.predict(df)[0]

    return JSONResponse(status_code=200,content={"message" : f"pridection : {prediction}"})
    