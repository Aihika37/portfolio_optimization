

```markdown
# Portfolio Optimization using Markowitz Theory

This project implements a mean–variance portfolio optimization framework to construct
the efficient frontier and identify the maximum Sharpe ratio portfolio using real market data.

The model is based on Modern Portfolio Theory and is commonly used in quantitative
asset management and trading.

---

## Assets

The portfolio is built using the following stocks:

- Apple (AAPL)  
- Walmart (WMT)  
- Tesla (TSLA)  
- General Electric (GE)  
- Amazon (AMZN)  
- Deutsche Bank (DB)  

Period: 2014 – 2024

---

## Theory

For a portfolio with weights w, expected returns μ, and covariance matrix Σ:

Expected return:
E(Rₚ) = wᵀ μ  

Risk (volatility):
σₚ = √(wᵀ Σ w)

Sharpe ratio:
S = E(Rₚ) / σₚ

The optimizer finds the portfolio that maximizes the Sharpe ratio under
long-only and fully-invested constraints.

---

## Features

- Downloads real historical stock prices  
- Computes log-returns  
- Annualizes returns and covariance  
- Generates 10,000 random portfolios  
- Constructs the efficient frontier  
- Uses numerical optimization (SLSQP) to find the maximum Sharpe ratio portfolio  
- Visualizes risk–return trade-offs  

---

## Methodology

1. Prices are downloaded from Yahoo Finance  
2. Log-returns are computed  
3. 10,000 random portfolios are generated  
4. Each portfolio’s return, risk, and Sharpe ratio is computed  
5. An optimizer searches for the Sharpe-maximizing allocation  
6. The efficient frontier is visualized  

---

## Outputs

The project produces:
- Efficient frontier scatter plot  
- Sharpe ratio heatmap  
- Optimal portfolio point  


⭐ Green star = Optimal portfolio
