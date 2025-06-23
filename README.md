# NHANES Diabetes Risk Modeling

- How do biometric, demographic, and socioeconomic factors jointly influence Hemoglobin A1c levels—a key indicator of diabetes risk—in the U.S. population? 
- Using data from NHANES, can we model these relationships non-linearly and explore interaction effects (e.g., between age, sex, BMI, and race/ethnicity) to identify subgroups with elevated glycemic risk? Furthermore, how do model structures and variable interactions shape our understanding of disparities in predicted A1c across demographic strata?


## Objective

To model HbA1c levels as a function of:

- Age, sex, and race/ethnicity
- BMI and waist circumference
- Income-to-poverty ratio and education level

and to explore:
- Non-linear and interaction effects
- Subgroup disparities (e.g., stratified by ethnicity, sex, or BMI level)
- Predictive modeling performance across model types

## Dataset and Variables

Source: NHANES (National Health and Nutrition Examination Survey), publicly available via CDC.

Primary Outcome:
- `LBXGH`: Hemoglobin A1c (%)

Key Predictors:
- `RIDAGEYR`: Age (years)
- `RIAGENDR`: Sex (M/F)
- `RIDRETH1`: Race/Ethnicity
- `BMXBMI`: Body Mass Index
- `BMXWAIST`: Waist Circumference
- `INDFMPIR`: Family Income-to-Poverty Ratio
- `DMDEDUC2`: Education Level
- Optional: `DIQ010` (Self-reported diabetes diagnosis), `LBXGLU` (Fasting glucose)

Recommended cycle: NHANES 2017–2018

## Methods and Models

- Linear regression (`lm`)
- Generalized Additive Models (`mgcv::gam`)
- Basis splines (`splines::bs`)
- Sliced Inverse Regression (`statsmodels.regression.dimred.SIR`)
- Model evaluation using AIC, residual analysis, and stratified visualizations

## Step-by-Step Analysis Plan

### 1. Data Acquisition and Cleaning
- Download NHANES 2017–2018 data:
  - Demographics
  - Body Measures
  - Laboratory: Glycohemoglobin
  - Questionnaire: Diabetes
- Merge datasets on `SEQN`
- Keep only complete cases for selected variables
- Recode `RIAGENDR` to factor or numeric
- Recode or filter `RIDRETH1` if necessary

### 2. Exploratory Data Analysis
- Distribution of HbA1c by sex, age, BMI
- Check missing data patterns
- Correlations between numeric predictors
- Boxplots of HbA1c by race/ethnicity and sex

### 3. Baseline Modeling (Linear Models)
- Start with additive model:
  - `LBXGH ~ RIDAGEYR + RIAGENDR + BMXBMI`
- Add interactions:
  - Age * Sex, BMI * Sex, Age * BMI
  - Full 3-way interaction if useful
- Compare models via AIC and residual plots

### 4. Add Nonlinear Effects (GAMs)
- Replace age and BMI with smooth terms:
  - `s(RIDAGEYR)`, `s(BMXBMI)`
- Allow smooths to vary by sex or ethnicity:
  - `s(RIDAGEYR, by=RIAGENDR)`
- Include tensor products for Age × BMI:
  - `te(RIDAGEYR, BMXBMI)`

### 5. Dimension Reduction (Optional)
- Construct feature matrix of predictors
- Use SIR to reduce dimensions
- Project scores and visualize against HbA1c
- Compare model performance using reduced dimensions

### 6. Visualization
- Predicted HbA1c vs. age at fixed BMI (by sex)
- HbA1c differences between sex or race groups
- Stratified plots: e.g., income or education levels
- Confidence bands from GAMs

### 7. Model Comparison and Interpretation
- Compare final models via AIC, R², visual fit
- Interpret marginal effects and interaction surfaces
- Discuss which features most strongly affect HbA1c

### 8. (Optional) Policy or Clinical Framing
- Discuss how BMI, income, or education may influence diabetes risk
- Highlight disparities in predicted outcomes by ethnicity or SES

## Notes

- Primary modeling will be done in R
- Dimension reduction (SIR) will be implemented in Python if needed
- Outputs (plots, models) will be stored in a separate `figs/` or `results/` folder

## To Do

- [ ] Finalize variable selection
- [ ] Write data-cleaning script
- [ ] Draft base linear models
- [ ] Implement GAMs with interactions
- [ ] Explore SIR if time permits
- [ ] Create figures and finalize results
