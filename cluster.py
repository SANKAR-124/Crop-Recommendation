import joblib
import numpy as np
import pandas as pd

model=joblib.load("modelss/kmeans_cluster_model.pkl")
scaler=joblib.load("modelss/standard_scaler.pkl")

def get_cluster(N,P,K,temp,humidity,ph,rainfall):

    # input_data=np.array([[N,P,K,temp,humidity,ph,rainfall]])

    input_data = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temp,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])
    scaled=scaler.transform(input_data)

    prediction=model.predict(scaled)

    return int(prediction[0])

