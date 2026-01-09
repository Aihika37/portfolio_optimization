import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
pd.set_option("display.max_columns", None)
r_f=0.05
mon=12
class capm:
    def __init__(self,stocks,starting_date,ending_date):
        self.stocks=stocks
        self.starting_date=starting_date
        self.ending_date=ending_date
    def get_data(self):
        data={}
        for stock in self.stocks:
            ticker=yf.Ticker(stock)
            data[stock]=ticker.history(start=self.starting_date,end=self.ending_date)['Close']
        return pd.DataFrame(data)
    def arrange_data(self,r_data):
        r_data['s_logdaily_ret']=np.log(r_data['s_returns']/r_data['s_returns'].shift(1))
        r_data['m_logdaily_ret'] = np.log(r_data['m_returns'] / r_data['m_returns'].shift(1))
        return r_data
    def get_beta(self,da):
       cova=np.cov(da['s_logdaily_ret'],da['m_logdaily_ret'])
       return (cova[1][0]/cova[1][1])
    def regression(self,da):
        beta,alpha=np.polyfit(da['m_logdaily_ret'],da['s_logdaily_ret'],deg=1)
        print(f"Beta from regression:{beta}")
        expected_ret=r_f+beta*(da['m_logdaily_ret'].mean()*mon-r_f)
        print(f"Expected Return:{expected_ret}")
        self.plot(da,beta,alpha)
    def plot(self,da,beta,alpha):
        fig,axis=plt.subplots(1,figsize=(20,10))
        axis.scatter(da['m_logdaily_ret'],da['s_logdaily_ret'],label="Data points")
        axis.plot(da['m_logdaily_ret'],beta*(da['m_logdaily_ret'])+alpha,color='Red')
        plt.title("Capital Asset Price Model")
        plt.xlabel("Market Return",fontsize=18)
        plt.ylabel("Stock Return")
        plt.legend()
        plt.grid(True)
        plt.show()

stoc=['IBM','^GSPC']
s_d='2014-01-01'
e_d='2024-01-01'
c=capm(stoc,s_d,e_d)
d=(c.get_data())
d=d.resample('M').last()
dat=pd.DataFrame({'s_returns':d[stoc[0]],'m_returns':d[stoc[1]]})
data=c.arrange_data(dat)
data=data[1:]
print(f"Beta:{c.get_beta(data)}")
c.regression(data)
tick=yf.Ticker('IBM')
s={}
s['Price']=tick.history(start=s_d,end=e_d)['Close']
s=pd.DataFrame(s)
s=np.log(s/s.shift(1))
s=s[1:]
plt.hist(s,bins=700)
m=s.mean()
v=s.var()
sig=np.sqrt(v)
x=np.linspace(m-3*sig,m+3*sig,100)
plt.plot(x,norm.pdf(x,m,sig))

plt.show()
