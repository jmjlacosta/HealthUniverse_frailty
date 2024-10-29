import streamlit as st
import math

# Define the function to calculate the Frailty Index
def calculate_frailty(impaired_mobility, depression, chf, parkinson, white_race, arthritis, cognitive_impairment, 
                      charlson_comorbidity, stroke, paranoia, skin_ulcer, pneumonia, male_sex, soft_tissue_infection, 
                      mycoses, age, admission_past_6mo, gout, falls, musculoskeletal_problems, uti):
    # Considering 6.92 as the max (80yrs old) and 0.49 the min (65yrs old) then we divide by 6.92 as a solution to the issue of over-predicting that is unadressed by the paper
    # Intercept for frailty index logistic model
    LP = 0
    if age == 0:
        age = 72
    # Adjust linear predictor with weights from the paper's model
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
    LP += 0.09 * age / 5
    LP += 0.09 * admission_past_6mo
    LP += 0.08 * gout
    LP += 0.08 * falls
    LP += 0.05 * musculoskeletal_problems
    LP += 0.05 * uti

    # Apply logistic transformation to get the probability of frailty
    probability = LP/6.92
    
    # Categorize frailty risk
    if probability < 0.12:
        category = "Low Frailty"
    elif probability < 0.20:
        category = "Medium Frailty"
    else:
        category = "High Frailty"
    
    return probability, category

# Streamlit UI for Frailty Index
st.title("Claims-based Frailty Index App")

# Add a brief description at the start
st.markdown("""
### Overview
This app calculates a frailty index based on key comorbidities and demographic factors using a regression model derived from claims data. 
Patients are classified into frailty risk categories as follows:
- **Low Frailty**: Probability < 0.12
- **Medium Frailty**: Probability 0.12 - 0.20
- **High Frailty**: Probability ≥ 0.20
""")

# Input fields for variables
st.header("Frailty Risk Indicators")
col1, col2 = st.columns(2)

with col1:
    impaired_mobility = st.checkbox("Impaired Mobility")
    depression = st.checkbox("Depression")
    chf = st.checkbox("Congestive Heart Failure")
    parkinson = st.checkbox("Parkinson Disease")
    white_race = st.checkbox("White Race")
    arthritis = st.checkbox("Arthritis (any type)")
    cognitive_impairment = st.checkbox("Cognitive Impairment")
    charlson_comorbidity = st.checkbox("Charlson Comorbidity Index (>0)")
    
with col2:
    stroke = st.checkbox("Stroke")
    paranoia = st.checkbox("Paranoia")
    skin_ulcer = st.checkbox("Chronic Skin Ulcer")
    pneumonia = st.checkbox("Pneumonia")
    male_sex = st.checkbox("Male Sex")
    soft_tissue_infection = st.checkbox("Skin & Soft Tissue Infection")
    mycoses = st.checkbox("Mycoses")
    age = st.number_input("Age", min_value=0, max_value=115)
    admission_past_6mo = st.checkbox("Admission in Past 6 Months")
    gout = st.checkbox("Gout or Other Crystal-Induced Arthropathy")
    falls = st.checkbox("Falls")
    musculoskeletal_problems = st.checkbox("Musculoskeletal Problems")
    uti = st.checkbox("Urinary Tract Infection")

# Compute Frailty score
if st.button("Calculate Frailty Index"):
    probability, category = calculate_frailty(
        impaired_mobility, depression, chf, parkinson, white_race, arthritis, cognitive_impairment, 
        charlson_comorbidity, stroke, paranoia, skin_ulcer, pneumonia, male_sex, soft_tissue_infection, 
        mycoses, age, admission_past_6mo, gout, falls, musculoskeletal_problems, uti
    )
    
    # Display result with tooltip
    st.markdown(f"### Frailty Index Probability: {probability:.2f}")
    st.markdown(f"### Frailty Risk Category: {category}")
    
    if probability >= 0.2:
        st.markdown("⚠️ **Note**: Individuals with a frailty index ≥ 0.2 have an increased risk of adverse outcomes, including higher likelihoods of hospital and nursing home admissions and mortality.")
