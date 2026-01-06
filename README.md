# Velocity-Based Training (VBT) 1RM Estimator

This Streamlit app estimates **1RM using barbell velocity**
based on **exercise-specific velocity at 1RM (V1RM)** values
from the strength & conditioning literature.

## Features
- Exercise-specific V1RM reference values
- %1RM and absolute 1RM estimation
- Velocity–%1RM visualisation
- Designed for applied sport science use

## Method
The app assumes a **linear load–velocity relationship** and
uses population-average V1RM values. Estimates are best used
for **daily autoregulation**, not maximal testing.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
