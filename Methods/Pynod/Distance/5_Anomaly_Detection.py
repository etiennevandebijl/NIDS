from paths_data import *
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima
import numpy as np

paths_ = paths_df[((paths_df["Analyser"]=="BRO_ZEEK") & (paths_df["File"].str.contains("Event")))]["Path"].values

df = pd.read_csv(paths_[2])
df["t"] = pd.to_datetime(df["t"])
df.index = df["t"]
df.drop(["t"],1,inplace=True)

for c in df.columns:
    df[c].plot(figsize=(20,10))
    plt.show()
    print(c)


df.columns
df_ = df["MCS_Edge_Distance"]
df_.plot()

def arima_(df):
    stepwise_model = auto_arima(df, 
                            start_p=1, start_q=1,
                            max_p=5, max_q=5, m=12,
                            start_P=0, 
                            max_d = 3,
                            seasonal=False,
                            trace=True,
                            error_action='ignore',  
                            suppress_warnings=True, 
                            stepwise=True)
    return stepwise_model

df_.shape
res = []
for i in range(30,239):
    train = df_.iloc[:i,]
    test = df_.iloc[i+1,]
    model = arima_(train)
    predict = model.predict(n_periods=1)
    res.append(test-predict)

result = pd.DataFrame(res)
result.index = df_.iloc[30:239,].index
threshold = 2* np.std(result)[0]
result["L"] = -threshold
result["U"] = threshold
result.plot(figsize=(15,10))
model = ARIMA(df["Umeyama_distance"], order=(1,0,0))
model_fit = model.fit(disp=0)

residuals = np.absolute(pd.DataFrame(model_fit.resid))
residuals.index = pd.to_datetime(residuals.index)
residuals.plot(figsize=(15,10))