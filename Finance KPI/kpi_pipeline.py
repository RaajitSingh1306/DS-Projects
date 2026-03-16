import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ── CONFIG — change these to run on any ticker ─────────────────
TICKER         = '^NSEI'
START_DATE     = '2014-04-10'
END_DATE       = datetime.today().strftime('%Y-%m-%d')
RISK_FREE_RATE = 0.065
OUTPUT_DIR     = './outputs'

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Finance KPI Pipeline'
    )
    parser.add_argument('--ticker', 
                        type=str, 
                        default='^NSEI',
                        help='Yahoo Finance ticker symbol')
    parser.add_argument('--start', 
                        type=str, 
                        default='2014-01-01',
                        help='Start date YYYY-MM-DD')
    parser.add_argument('--risk_free', 
                        type=float, 
                        default=0.065,
                        help='Annual risk free rate (decimal)')
    return parser.parse_args()

# ── STEP 1: DATA INGESTION ─────────────────────────────────────
def load_data(ticker, start, end):
    print(f"[1/4] Downloading {ticker}...")
    df = yf.download(ticker, start=start, end=end, progress=False)
    df.columns = df.columns.get_level_values(0)
    df = df[['Close']]
    df.index = pd.to_datetime(df.index)
    df['returns'] = df['Close'].pct_change()
    print(f"      {len(df)} rows loaded")
    return df

# ── STEP 2: KPI CALCULATION ────────────────────────────────────
def calculate_kpis(df, risk_free_rate):
    print("[2/4] Calculating KPIs...")
    
    start_price = df['Close'].iloc[0]
    end_price   = df['Close'].iloc[-1]
    n_years     = (df.index[-1] - df.index[0]).days / 365.25
    cagr        = (end_price / start_price) ** (1 / n_years) - 1

    returns_clean   = df['returns'].dropna()
    risk_free_daily = risk_free_rate / 252
    excess_returns  = returns_clean - risk_free_daily
    sharpe          = (excess_returns.mean() / 
                       excess_returns.std()) * np.sqrt(252)

    rolling_max = df['Close'].cummax()
    drawdown    = (df['Close'] - rolling_max) / rolling_max
    max_dd      = drawdown.min()
    max_dd_date = drawdown.idxmin()

    kpis = {
        'ticker'       : TICKER,
        'start_date'   : df.index[0].date(),
        'end_date'     : df.index[-1].date(),
        'start_price'  : round(float(start_price), 2),
        'end_price'    : round(float(end_price), 2),
        'cagr_pct'     : round(cagr * 100, 2),
        'sharpe'       : round(sharpe, 3),
        'max_dd_pct'   : round(max_dd * 100, 2),
        'max_dd_date'  : max_dd_date.date(),
        'n_years'      : round(n_years, 2)
    }

    return kpis, drawdown, excess_returns

# ── STEP 3: GENERATE REPORT ────────────────────────────────────
def generate_report(df, kpis, drawdown, excess_returns):
    print("[3/4] Generating charts...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(
        f"{kpis['ticker']} — KPI Report | "
        f"CAGR: {kpis['cagr_pct']}% | "
        f"Sharpe: {kpis['sharpe']} | "
        f"Max DD: {kpis['max_dd_pct']}%",
        fontsize=12
    )

    # Price + CAGR line
    days = (df.index - df.index[0]).days
    cagr_line = kpis['start_price'] * \
                (1 + kpis['cagr_pct']/100) ** (days/365.25)
    axes[0,0].plot(df.index, df['Close'], 
                   color='steelblue', linewidth=0.8)
    axes[0,0].plot(df.index, cagr_line, color='coral', 
                   linewidth=1.5, linestyle='--',
                   label=f"CAGR {kpis['cagr_pct']}%")
    axes[0,0].set_title('Price vs CAGR trendline')
    axes[0,0].legend()

    # Drawdown
    axes[0,1].fill_between(drawdown.index, drawdown*100, 0,
                            color='coral', alpha=0.6)
    axes[0,1].axhline(y=kpis['max_dd_pct'], color='red',
                       linestyle='--',
                       label=f"Max DD: {kpis['max_dd_pct']}%")
    axes[0,1].set_title('Drawdown')
    axes[0,1].legend()

    # Rolling Sharpe
    roll = excess_returns.rolling(252)
    r_sharpe = (roll.mean() / roll.std()) * np.sqrt(252)
    axes[1,0].plot(r_sharpe.index, r_sharpe, 
                   color='teal', linewidth=0.8)
    axes[1,0].axhline(y=1, color='green', linestyle='--', 
                       alpha=0.5, label='Sharpe=1')
    axes[1,0].axhline(y=0, color='gray', linewidth=0.8)
    axes[1,0].set_title(f"Rolling Sharpe (overall: {kpis['sharpe']})")
    axes[1,0].legend()

    # Annual returns
    df_copy = df.copy()
    df_copy['year'] = df_copy.index.year
    annual = df_copy.groupby('year')['returns'].mean() * 252
    colors = ['steelblue' if x > 0 else 'coral' for x in annual]
    axes[1,1].bar(annual.index, annual*100, 
                  color=colors, edgecolor='white')
    axes[1,1].axhline(y=kpis['cagr_pct'], color='coral',
                       linestyle='--',
                       label=f"CAGR {kpis['cagr_pct']}%")
    axes[1,1].set_title('Annual returns')
    axes[1,1].legend()

    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    chart_path = f"{OUTPUT_DIR}/kpi_report_{TICKER.replace('^','')}.png"
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      Chart saved: {chart_path}")
    return chart_path

# ── STEP 4: SAVE KPI SUMMARY ───────────────────────────────────
def save_summary(kpis):
    print("[4/4] Saving KPI summary...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary_path = f"{OUTPUT_DIR}/kpi_summary_{TICKER.replace('^','')}.csv"
    pd.DataFrame([kpis]).to_csv(summary_path, index=False)
    print(f"      Saved: {summary_path}")
    return summary_path

if __name__ == '__main__':
    args = parse_args()
    
    # Override config with command line args
    TICKER         = args.ticker
    START_DATE     = args.start
    RISK_FREE_RATE = args.risk_free

    df                         = load_data(TICKER, START_DATE, END_DATE)
    kpis, drawdown, excess_ret = calculate_kpis(df, RISK_FREE_RATE)
    generate_report(df, kpis, drawdown, excess_ret)
    save_summary(kpis)

    print("\n── KPI Summary ───────────────────────────────")
    for k, v in kpis.items():
        print(f"  {k:<15}: {v}")
    print("Done.")
