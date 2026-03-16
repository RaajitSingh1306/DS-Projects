# Loan Default — EDA & Credit Risk Model

## Overview
Exploratory data analysis and classification model on a loan dataset 
to identify key predictors of loan default.

## Dataset
- 45,000 rows, 14 columns
- Source: [write where you got it]
- Target variable: loan_status (0 = approved, 1 = default)

## Key Findings
- loan_percent_income was the strongest default predictor (r=0.39)
- Renters default at 4x the rate of homeowners (32% vs 8%)
- Education level showed no predictive value (~22% default across all levels)
- person_age and person_emp_exp were redundant (r=0.95)

## Model
- Algorithm: Decision Tree Classifier (max_depth=4)
- Test Accuracy: 91.2%
- ROC-AUC: 0.945
- Key insight: full tree overfit (100% train, 90.1% test)

## What I Learned
- Initial Data cleaning
- Data understanding and subsequently removing undesired/anomaly datapoints
- Why capping large anomalies is better than dropping entire rows
- Encoding, decision tree, also with confidence matrix and how prediction actually rely on it

## Files
- loan_eda.ipynb — cleaning, EDA, visualisation
- eda_overview.png — distribution charts
- eda_deep.png — deeper analysis charts
- confusion_matrix.png — model evaluation
- decision_tree.png — visualised model logic

## Setup
pip install pandas numpy matplotlib seaborn scikit-learn