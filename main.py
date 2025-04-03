from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI(
    title="Claims-Based Frailty Index API",
    description="Predicts frailty risk category from comorbidities and demographic factors using a logistic regression model.",
    version="1.0.0"
)

# Enable CORS for all origins (for dev/testing convenience)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FrailtyResponse(BaseModel):
    probability: float = Field(..., description="Predicted frailty index probability (normalized)")
    category: str = Field(..., description="Frailty risk category")

@app.post(
    "/calculate_frailty",
    response_model=FrailtyResponse,
    summary="Calculate Claims-Based Frailty Index",
    description="Computes the frailty index and categorizes risk level."
)
def calculate_frailty(
    request: Request,
    impaired_mobility: Annotated[Literal["True", "False"], Form(...)] = "False",
    depression: Annotated[Literal["True", "False"], Form(...)] = "False",
    chf: Annotated[Literal["True", "False"], Form(...)] = "False",
    parkinson: Annotated[Literal["True", "False"], Form(...)] = "False",
    white_race: Annotated[Literal["True", "False"], Form(...)] = "False",
    arthritis: Annotated[Literal["True", "False"], Form(...)] = "False",
    cognitive_impairment: Annotated[Literal["True", "False"], Form(...)] = "False",
    charlson_comorbidity: Annotated[Literal["True", "False"], Form(...)] = "False",
    stroke: Annotated[Literal["True", "False"], Form(...)] = "False",
    paranoia: Annotated[Literal["True", "False"], Form(...)] = "False",
    skin_ulcer: Annotated[Literal["True", "False"], Form(...)] = "False",
    pneumonia: Annotated[Literal["True", "False"], Form(...)] = "False",
    male_sex: Annotated[Literal["True", "False"], Form(...)] = "False",
    soft_tissue_infection: Annotated[Literal["True", "False"], Form(...)] = "False",
    mycoses: Annotated[Literal["True", "False"], Form(...)] = "False",
    age: Annotated[int, Form(...)] = 72,
    admission_past_6mo: Annotated[Literal["True", "False"], Form(...)] = "False",
    gout: Annotated[Literal["True", "False"], Form(...)] = "False",
    falls: Annotated[Literal["True", "False"], Form(...)] = "False",
    musculoskeletal_problems: Annotated[Literal["True", "False"], Form(...)] = "False",
    uti: Annotated[Literal["True", "False"], Form(...)] = "False",
) -> FrailtyResponse:
    
    def to_int(val: str) -> int:
        return 1 if val == "True" else 0

    # Convert form booleans
    impaired_mobility = to_int(impaired_mobility)
    depression = to_int(depression)
    chf = to_int(chf)
    parkinson = to_int(parkinson)
    white_race = to_int(white_race)
    arthritis = to_int(arthritis)
    cognitive_impairment = to_int(cognitive_impairment)
    charlson_comorbidity = to_int(charlson_comorbidity)
    stroke = to_int(stroke)
    paranoia = to_int(paranoia)
    skin_ulcer = to_int(skin_ulcer)
    pneumonia = to_int(pneumonia)
    male_sex = to_int(male_sex)
    soft_tissue_infection = to_int(soft_tissue_infection)
    mycoses = to_int(mycoses)
    admission_past_6mo = to_int(admission_past_6mo)
    gout = to_int(gout)
    falls = to_int(falls)
    musculoskeletal_problems = to_int(musculoskeletal_problems)
    uti = to_int(uti)

    if age == 0:
        age = 72  # Default age

    # Linear predictor calculation
    LP = 0
    LP += 1.24 * impaired_mobility
    LP += 0.54 * depression
    LP += 0.50 * chf
    LP += 0.50 * parkinson
    LP -= 0.49 * white_race
    LP += 0.43 * arthritis
    LP += 0.33 * cognitive_impairment
    LP += 0.31 * charlson_comorbidity
    LP += 0.28 * stroke
    LP += 0.24 * paranoia
    LP += 0.23 * skin_ulcer
    LP += 0.21 * pneumonia
    LP -= 0.19 * male_sex
    LP += 0.18 * soft_tissue_infection
    LP += 0.14 * mycoses
    LP += 0.09 * (age / 5)
    LP += 0.09 * admission_past_6mo
    LP += 0.08 * gout
    LP += 0.08 * falls
    LP += 0.05 * musculoskeletal_problems
    LP += 0.05 * uti

    probability = LP / 6.92

    if probability < 0.12:
        category = "Low Frailty"
    elif probability < 0.20:
        category = "Medium Frailty"
    else:
        category = "High Frailty"

    return FrailtyResponse(probability=round(probability, 4), category=category)
