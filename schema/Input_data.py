from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Annotated, Literal,Dict
from config.city_tiers import tier_1_cities,tier_2_cities

class Input_Data(BaseModel):

    age : Annotated[int,Field(...,gt=0,lt=120)]
    weight : int
    height : float
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
     

    @field_validator("city")
    @classmethod
    def transformCity(cls,value : str):
        return value.strip().title()
    