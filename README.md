# Claims-based Frailty Index (CFI) App

This repository provides an implementation of the Claims-based Frailty Index (CFI), which classifies individuals as frail or non-frail using data derived solely from administrative claims. The model's area under the ROC curve is 0.75, and it is designed to aid in healthcare planning, emergency preparedness, and clinical decision-making for frail populations.

The CFI allows healthcare professionals to efficiently assess frailty risk, guiding interventions such as enrollment in care management programs or planning services in disaster situations.

## How It Works

The CFI model calculates a frailty score based on a range of patient factors, including age, gender, and the presence of key comorbidities. Each comorbidity is assigned a weight based on its predictive importance, derived from logistic regression coefficients.

### **Input:**  
Users manually input patient information, such as age and comorbidities (e.g., impaired mobility, depression, and cognitive impairment).

### **Output:**  
The app provides a frailty score with the following classifications:

- **Low Frailty:** Score < 0.2
- **Medium Frailty:** Score 0.2–0.4
- **High Frailty:** Score ≥ 0.4

Each result includes a tooltip indicating that scores above 0.2 are linked to increased risks of adverse events like hospitalization, disability, and mortality.

## Model Details

The CFI is based on logistic regression. Covariates, such as specific medical conditions, were selected for their relevance to frailty prediction and include diagnoses like congestive heart failure, depression, and musculoskeletal problems. The use of claims data alone ensures the model's practicality for widespread implementation.

## Summary

This application offers an accessible, data-driven tool for estimating frailty risk, supporting timely interventions and resource allocation for high-risk individuals. Designed for transparency, the model optimally balances predictive power and interpretability.
