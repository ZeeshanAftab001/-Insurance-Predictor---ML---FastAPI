from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Annotated, Literal,Dict
from config.city_tiers import tier_1_cities,tier_2_cities

class Response_Data(BaseModel):

    prediction : Annotated[str,Field(...,description="This is the output prediction of the model.",examples=["medium","low","high"])]
   
    Confidence : Annotated[float,Field(...,description="This is the confidence score of the model.")]
    Confidence : Annotated[Dict[str,float],Field(...,description="This is the confidence score of the model for each of the output category.")]
