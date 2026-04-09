import joblib
import numpy as np
import pandas as pd

def predict(N,P,K,temp,humidity,ph,rainfall):
    model=joblib.load("modelss/svm_model.pkl")
    # scaler=joblib.load("modelss/scaler_svm.pkl")

    # input_data=np.array([[N,P,K,temp,humidity,ph,rainfall]])
    # scaled_input=scaler.transform(input_data)
    

    input_data = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temp,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    predictions=model.predict_proba(input_data)
    top_3_indices=predictions[0].argsort()[-3:][::-1]
    
    # Map to crop names with probabilities
    result = []
    for idx in top_3_indices:
        crop_name = model.classes_[idx]
        probability = round(predictions[0][idx], 2)
        result.append((crop_name, probability))
    
    return result
