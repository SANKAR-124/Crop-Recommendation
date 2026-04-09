import pandas as pd

df=pd.read_csv("feature_importance.csv")
cp=pd.read_json("crop_profiles.json")

def why_pred(crop_name):
    
    crop_reason = {

    "rice": "Requires high rainfall and humidity, making it suitable for water-rich environments. Thrives in moderate temperatures with sufficient soil moisture.",

    "maize": "Grows well in moderate temperature and rainfall conditions with good nitrogen availability. It is adaptable and performs well under typical tropical climates.",

    "chickpea": "Prefers low rainfall and low humidity, making it suitable for dry and cooler environments. As a legume, it requires minimal nitrogen from soil.",

    "kidneybeans": "Grows best in controlled temperature and low humidity environments. It is sensitive to soil and climatic variations, requiring stable conditions.",

    "pigeonpeas": "Highly adaptable crop that can tolerate a wide range of humidity and rainfall conditions. Suitable for moderate environments with flexible growing conditions.",

    "mothbeans": "Extremely resilient crop that can grow in low rainfall and poor soil conditions. It tolerates a wide pH range, making it suitable for harsh environments.",

    "mungbean": "Performs well in low rainfall and moderate temperature conditions. Being a legume, it requires low nitrogen and is suitable for dry regions.",

    "blackgram": "Grows in low rainfall regions with moderate temperature conditions. It is a legume crop that requires minimal nitrogen input.",

    "lentil": "Prefers dry climates with low humidity and low rainfall. Suitable for cooler environments with stable soil conditions.",

    "banana": "Requires high nitrogen and grows well in moderate to high humidity conditions. Thrives in stable tropical climates with sufficient water availability.",

    "mango": "Prefers warm temperatures and moderate rainfall conditions. It grows well in tropical environments with balanced humidity levels.",

    "apple": "Requires cooler temperatures and grows best in high nutrient soils. It needs high phosphorus and potassium for optimal growth.",

    "grapes": "Highly adaptable crop that can tolerate a wide range of temperatures. Requires high phosphorus and potassium levels for proper growth.",

    "watermelon": "Grows well in moderate temperatures with controlled and low rainfall. Requires good nutrient supply, especially nitrogen, for optimal yield.",

    "muskmelon": "Prefers stable temperature conditions with high humidity but low rainfall. It requires nutrient-rich soil for proper development.",

    "orange": "Grows well in high humidity and moderate rainfall conditions. It is adaptable to varying temperature ranges and moderate soil conditions.",

    "papaya": "Highly adaptable crop that can grow in a wide range of rainfall conditions. Prefers high temperature and high humidity environments.",

    "coconut": "Thrives in high humidity and high rainfall regions, especially coastal areas. Suitable for warm tropical climates with consistent moisture.",

    "cotton": "Highly dependent on nitrogen and grows well in moderate rainfall conditions. It can tolerate variations in nutrient levels and environmental conditions.",

    "coffee": "Grows well in moderate temperature and humidity conditions with consistent rainfall. It can tolerate variations in humidity and climate conditions.",

    "jute": "Requires high humidity and high rainfall for proper growth. Suitable for warm and moist environmental conditions.",

    "pomegranate": "Grows well in high humidity and moderate rainfall conditions. It is adaptable and can tolerate variations in environmental conditions."}

    if crop_name in crop_reason:
        return crop_reason[crop_name]
    else:
        return "predicted crop not found"

def get_crop_prof(crop_name):
    if crop_name in cp:
        return cp[crop_name].to_dict()
    return "Crop profile not found"

def get_cluster_info(cluster_id):
    cluster_description = {

    0: {
        "title": "Hot, Humid, High Rainfall & Nutrient-Rich",
        "description": "This cluster represents hot, humid, and high-rainfall conditions with very high phosphorus and potassium levels. The combination of high temperature and heavy rainfall indicates tropical environments where nutrient-rich soil is essential.",
        "conditions": "High temperature, high humidity, very high rainfall, high P and K",
        "summary": "Tropical, high rainfall, nutrient-rich environment"
    },

    1: {
        "title": "Nitrogen-Dominant Humid Environment",
        "description": "This cluster is characterized by very high nitrogen levels, warm temperatures, and high humidity with moderate rainfall. It represents environments where nitrogen plays a dominant role in crop growth.",
        "conditions": "High nitrogen, warm temperature, high humidity, moderate rainfall",
        "summary": "Nitrogen-rich, warm and humid conditions"
    },

    2: {
        "title": "Moderate Climate with Low Nutrients",
        "description": "This cluster represents balanced environmental conditions with relatively low nitrogen and potassium levels. It supports crops that are adaptable and require fewer soil nutrients.",
        "conditions": "Moderate temperature, moderate humidity, moderate rainfall, low N and K",
        "summary": "Balanced climate with low nutrient dependency"
    },

    3: {
        "title": "Cool Climate with High Soil Fertility",
        "description": "This cluster is defined by very high phosphorus and potassium levels, high humidity, but comparatively lower temperatures and moderate rainfall. It represents nutrient-rich environments in cooler climates.",
        "conditions": "Lower temperature, high humidity, moderate rainfall, high P and K",
        "summary": "Cool, nutrient-rich, moderately wet conditions"
    },

    4: {
        "title": "High Rainfall but Low Soil Fertility",
        "description": "This cluster represents environments with high humidity and high rainfall but very low nitrogen, phosphorus, and potassium levels. It indicates regions where water is abundant but soil nutrients are limited.",
        "conditions": "High rainfall, high humidity, very low NPK",
        "summary": "Moist environment with poor soil fertility"
    },

    5: {
        "title": "Cool and Dry Environment",
        "description": "This cluster is characterized by low temperature and significantly low humidity with moderate rainfall. It represents relatively dry and cooler environmental conditions suitable for drought-tolerant crops.",
        "conditions": "Low temperature, low humidity, moderate rainfall",
        "summary": "Cool, dry, low-moisture environment"
    }

    }
    
    if cluster_id in cluster_description:
        return cluster_description[cluster_id]
    else:
        return "Cluster ID not found"
    

def get_top_features():
    sorted_df = df.sort_values(by="Importance", ascending=False)
    top = sorted_df.head(3)
    return list(top["Feature"])

def get_primary_driver():
    sorted_df = df.sort_values(by="Importance", ascending=False)
    return sorted_df.iloc[0]["Feature"]

def generate_exp(crop, cluster, user_input):

    reason = why_pred(crop)
    ideal_conditions = get_crop_prof(crop)
    cluster_info = get_cluster_info(cluster)
    top_features = get_top_features()
    primary_driver = get_primary_driver()

    return {
        "crop": crop,
        "reason": reason,
        "ideal_conditions": ideal_conditions,
        "cluster": cluster_info,
        "top_features": top_features,
        "primary_driver": primary_driver
    }