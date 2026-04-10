from flask import render_template, Flask, request, redirect, url_for
import pandas as pd

from model import predict
from cluster import get_cluster
from economics import calc_rev
from explanation import generate_exp

app = Flask(__name__)

final_result = None


@app.route('/')
def home():
    return render_template("index.html")



@app.route('/input')
def input_page():
    return render_template("input.html")


@app.route('/predict', methods=['POST'])
def predict_route():
    global final_result

    try:
        # 🛡️ TRAP 1: Form Inputs Empty or Invalid
        # If a user submits without filling a box, float("") throws a ValueError.
        # .get("N", 0) ensures there is a fallback, but we use a try-except to be safe.
        try:
            N = float(request.form.get("N", 0))
            P = float(request.form.get("P", 0))
            K = float(request.form.get("K", 0))
            temp = float(request.form.get("temperature", 0))
            humidity = float(request.form.get("humidity", 0))
            ph = float(request.form.get("ph", 0))
            rainfall = float(request.form.get("rainfall", 0))
        except (TypeError, ValueError):
            return "Error: Please ensure all input fields contain valid numbers.", 400

        # Get Predictions
        result = predict(N, P, K, temp, humidity, ph, rainfall)
        
        # 🛡️ TRAP 2: Re-integrating the Cluster Call
        # We call the cluster model here. Ensure get_cluster() uses the standard_scaler.pkl!
        cluster_id = get_cluster(N, P, K, temp, humidity, ph, rainfall)
        user_input = pd.DataFrame([{
            "N": N,
            "P": P,
            "K": K,
            "temperature": temp,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }])
        top_crops_data = []

        for crop_name, conf in result:
            conf_percentage = conf * 100
            
            exp = generate_exp(crop_name,cluster_id,user_input)
            
            # 🛡️ TRAP 3: Missing Crop in Economics JSON
            # If the model predicts a crop that you forgot to add to crop_economics.json,
            # calc_rev() will crash the whole app. We wrap it in a try-except.
            try:
                rev = calc_rev(crop_name)
            except Exception:
                # Fallback dictionary so the UI doesn't break
                rev = {"crop": crop_name, "unit": "N/A", "revenue": "Data Unavailable"}

            c_info = exp.get('cluster', {})

            top_crops_data.append({
                "name": crop_name.capitalize(),
                "confidence": round(conf_percentage, 2),
                "crop_info": exp.get("reason", "Suitable based on soil profile."),
                "cluster_label": c_info.get("title", f"Cluster {cluster_id}"),
                "cluster_description": c_info.get("description", ""),
                "cluster_conditions": c_info.get("conditions", ""),
                "cluster_summary": c_info.get("summary", ""),
                "ideal_conditions":exp.get("ideal_conditions",""),
                "revenue_data": rev
            })
        
        try:
            feature_df = pd.read_csv("feature_importance.csv")
            sorted_features = feature_df.sort_values(by="Importance", ascending=False).head(5)
            
            top_features = []
            for _, row in sorted_features.iterrows():
                top_features.append({
                    "feature": row["Feature"],
                    "importance": round(row["Importance"], 2),
                })
        except FileNotFoundError:
            # Safe fallback if the file isn't found
            top_features = [{"feature": "Data Unavailable", "importance": 0}]
        
        # Package everything up safely
        final_result = {
            "top_crops": top_crops_data,
            # "crop_info": exp["reason"],
            # "cluster_label": exp["cluster"]["title"],
            # "cluster_description": exp["cluster"]["description"],
            # "cluster_conditions":exp["cluster"]["conditions"],
            # "cluster_summary":exp["cluster"]["summary"],
            # "ideal_conditions": exp["ideal_conditions"],
            "input_summary": {
                "nitrogen": N,
                "phosphorus": P,
                "potassium": K,
                "temperature": temp,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            },
            # "revenue":rev,
            "top_features": top_features,
            "revenue_note": "Estimated based on average market conditions and crop yield."
        }

        return redirect(url_for('results'))

    except Exception as e:
        # Catch-all for any completely unexpected server errors
        return f"A critical error occurred: {str(e)}", 500



@app.route('/results')
def results():
    global final_result
    if final_result is None:
        return redirect(url_for('input_page'))
    
    return render_template("results.html", **final_result)


if __name__ == "__main__":
    app.run(debug=True)