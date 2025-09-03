
import numpy as np, json, os
MODEL_OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)),"models","aqi_model.json")

def make_synthetic(n=5000,seed=42):
    rng = np.random.default_rng(seed)
    pm25 = rng.uniform(5,200,n)
    temp = rng.uniform(5,40,n)
    hum = rng.uniform(20,95,n)
    wind = rng.uniform(0,10,n)
    hours = rng.integers(0,24,n)
    y = 0.8*pm25 + 0.2*temp - 0.12*hum + 0.4*wind + 0.5*hours + rng.normal(0,5,n)
    return np.vstack([pm25,temp,hum,wind,hours]).T, y

def train_and_save(path=MODEL_OUT):
    X,y = make_synthetic()
    X1 = np.hstack([np.ones((X.shape[0],1)), X])
    coeffs,*_ = np.linalg.lstsq(X1,y,rcond=None)
    intercept = float(coeffs[0])
    coefs = coeffs[1:].tolist()
    names = ["pm25","temperature","humidity","wind_speed","hours_ahead"]
    model_json = {"model_type":"linear","intercept":intercept,"coefficients":{n: float(c) for n,c in zip(names,coefs)}}
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(model_json,f,indent=2)
    print("Saved model to",path)

if __name__ == '__main__':
    train_and_save()
