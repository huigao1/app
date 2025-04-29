# A Multi-page Streamlit App

Team members: Hui Gao, Phunsok Norboo, Zehui Wang

The Colab Notebook can be found here:
https://colab.research.google.com/drive/1UEtogwYzasK_aPcH7118oASjKyBvi6Hx?usp=sharing

# ESG and Financial Signals for Margin Prediction

## Project Overview

This project builds machine learning models to predict a company's EBITDA Margin and Operating Margin by combining Environmental, Social, and Governance (ESG) scores with traditional financial metrics.  
The goal is to translate sustainability profiles into concrete financial outcomes that support forecasting, risk analysis, and valuation work.

## Dataset

- Source: Wharton Research Data Services (WRDS)
- Coverage: 3,473 U.S.-listed companies (both active and delisted)
- Period: 2002–2023
- Data Types: Financial statement data and company-level ESG scores

## Features

**Financial Metrics**  
- Asset Turnover (Revenues / Assets)  
- Debt Ratio (Liabilities / Assets)  
- Log Assets (ln(Assets))  
- ROA (Net Income / Assets)  
- Net Profit Margin (Net Income / Revenues)  
- CashFlow Margin (Operating Cash Flow / Revenues)  
- CapEx Intensity (Capital Expenditures / Revenues)

**ESG Metrics**  
- Environmental Score  
- Social Score  
- Governance Score  

## Modeling Approach

- Algorithm: HistGradientBoostingRegressor
- Separate models trained for EBITDA Margin and Operating Margin
- Features selected based on domain intuition and exploratory analysis
- Missing values handled by median imputation

### Model Performance

| Metric           | EBITDA Model (Test) | Operating Margin Model (Test) |
|------------------|---------------------|-------------------------------|
| R²               | 0.949               | 0.940                         |
| MAE              | 1.74                | 1.98                          |

## Application

An interactive Streamlit dashboard was developed to explore the models, including:
- Exploratory Data Analysis (EDA) of ESG and financial variables
- Model comparison between Linear Regression and Gradient Boosting
- Real-time margin prediction using ticker-level data from Yahoo Finance
- What-if scenario analysis to simulate changes in ESG risks

## Why This Matters

This project bridges the gap between ESG ratings and traditional financial metrics by providing a quantitative link between sustainability risks and company profitability. It supports data-driven financial forecasting, valuation analysis, and ESG risk management.
