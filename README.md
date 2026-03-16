# Data Science Projects — Raajit

A collection of end-to-end data science projects built in 15 days.
Each project builds on skills from the previous one.

## Projects

### 01 — Loan EDA + Credit Risk Model
Exploratory analysis and decision tree classifier on 45k loan records.
- 91.2% accuracy · 0.945 ROC-AUC
- Key finding: loan_percent_income strongest default predictor

### 02 — Nifty 50 Time Series + Macro Analysis  
ARIMA forecasting on Indian market index with inflation correlation.
- ADF stationarity testing · seasonal decomposition
- Key finding: Nifty returns follow Efficient Market Hypothesis

### 03 — Finance KPI Pipeline
Automated pipeline calculating CAGR, Sharpe ratio, max drawdown
for any ticker via single terminal command.
- Reliance outperformed Nifty and TCS on risk-adjusted basis
- Pipeline runs on any Yahoo Finance ticker

## Stack
Python · pandas · numpy · scikit-learn · matplotlib · 
seaborn · statsmodels · yfinance

## Structure
Each project folder contains data/, notebooks/, outputs/
and its own README with findings and setup instructions.