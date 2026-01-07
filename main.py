import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimization
stocks=['AAPL','WMT','TSLA','GE','AMZN','DB']
start_date="2014-01-01"
end_date="2024-01-01"
NUM_OF_T_DAYS=252
NUM_OF_PF=10000
def download_data():
    stocks_data={}
    for stock in stocks:
        ticker=yf.Ticker(stock)
        stocks_data[stock]=ticker.history(start=start_date,end=end_date)['Close']
    return (pd.DataFrame(stocks_data))
def show_data(data):
    data.plot(figsize=(10,5))
    plt.show()
def log_daily(data):
    return ((np.log(data/data.shift(1)))[1:])
def generate_portfolio(returns):
    expected_return=returns.mean()*NUM_OF_T_DAYS
    expected_return=((expected_return).to_numpy())
    weights=[]
    expected_returns_pf=[]
    expected_risk_pf=[]
    for _ in range(NUM_OF_PF):
        weight=(np.random.rand(len(stocks)))
        weight=weight/weight.sum()
        weights.append(weight)
        expected_returns_pf.append(np.dot(expected_return,weight))
        expected_risk_pf.append(np.sqrt(np.dot(weight.T,np.dot((returns.cov()*NUM_OF_T_DAYS),weight))))
    return (weights),(expected_returns_pf),(expected_risk_pf)

def func(weights,data):
    ret = np.sum(data.mean() * weights) * NUM_OF_T_DAYS
    ris = np.sqrt(np.dot(weights.T, np.dot((data.cov() * NUM_OF_T_DAYS), weights)))
    return -ret/ris
def optimizer(wei,data):
    constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    bound=tuple((0,1) for _ in range(len(stocks)))
    min=optimization.minimize(fun=func,x0=wei[0],args=data,method='SLSQP',
                          constraints=constraint,bounds=bound)
    print(f"Optimal Portfolio:{min['x'].round(3)}")
    ret = np.sum(data.mean() * min['x'].round(3)) * NUM_OF_T_DAYS
    ris = np.sqrt(np.dot(min['x'].round(3).T, np.dot((data.cov() * NUM_OF_T_DAYS), min['x'].round(3))))
    print(f"Risk:{ris},Return:{ret},Sharpe Ratio:{ret/ris}")
    return ris,ret
def plot_curve(ret,risk,optret,optris):
    plt.figure(figsize=(10,6))
    plt.scatter(risk,ret,c=ret/risk,marker='o')
    plt.xlabel("Expected Volatility")
    plt.ylabel("Expected Return")
    plt.grid(True)
    plt.colorbar(label="Sharpe Ratio")
    plt.plot(optris,optret,'g*',markersize=20)
    plt.show()
dataset=(download_data())
show_data(dataset)
log_daily_returns=(log_daily(dataset))
generate_portfolio(log_daily_returns)
pweights,preturns,prisks=generate_portfolio(log_daily_returns)
pweights=np.array(pweights)
preturns=np.array(preturns)
prisks=np.array(prisks)
oris,oret=optimizer(np.array(pweights),log_daily_returns)
plot_curve(np.array(preturns),np.array(prisks),oret,oris)

