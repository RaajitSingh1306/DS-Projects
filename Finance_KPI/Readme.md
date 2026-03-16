# Finance KPI Dashboard & Automated Pipeline

## Overview
Automated pipeline that downloads market data for any ticker,
calculates key financial KPIs, generates a dashboard, and 
saves a CSV summary — triggered by a single terminal command.

## KPIs Calculated
- CAGR: compound annual growth rate
- Sharpe Ratio: return per unit of risk (vs 6.5% risk-free rate)
- Max Drawdown: largest peak-to-trough decline

## Results — 12yr Comparison (2014–2026)
| Ticker    | CAGR   | Sharpe | Max DD  |
|-----------|--------|--------|---------|
| Nifty 50  | 11.38% | 0.366  | -38.44% |
| Reliance  | 17.75% | 0.514  | -45.09% |
| TCS       |  9.34% | 0.229  | -44.09% |

## Usage
python pipeline/kpi_pipeline.py --ticker RELIANCE.NS --start 2014-01-01

## What I Learned
- I learned different KPIs
- How to use them is real-life
- Why is .py better than .ipynb (due to better automation capability)

## Setup
pip install yfinance pandas numpy matplotlib

-----------------------------------------
