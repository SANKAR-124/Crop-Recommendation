from economics import calc_rev
from explanation import generate_exp
from model import predict
from cluster import get_cluster


N = float(input("enter the lvl of nitrogen: "))
P = float(input("enter the lvl of phosphorous: "))
K = float(input("enter the lvl of potassium: "))
temp = float(input("enter the temperature: "))
humidity = float(input("enter the humidity: "))
ph = float(input("enter the pH level: "))
rainfall = float(input("enter the rainfall: "))


user_input = {
    "N": N,
    "P": P,
    "K": K,
    "temperature": temp,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall
}

top3 = predict(N, P, K, temp, humidity, ph, rainfall)

cluster = get_cluster(N, P, K, temp, humidity, ph, rainfall)

for crop, prob in top3:

    exp = generate_exp(crop, cluster, user_input)
    rev = calc_rev(crop)

    print("\n==============================")
    print(f"Crop: {crop}")
    print(f"Probability: {round(prob, 2)}")
    print(f"Cluster: {exp['cluster']['title']}")
    print(f"Cluster Description: {exp['cluster']['description']}")
    print(f"Conditions: {exp['cluster']['conditions']}")
    print(f"Cluster summary : {exp['cluster']['summary']}")
    print(f"Reason: {exp['reason']} \n")
    print(f"Ideal conditions : {exp['ideal_conditions']}")
    print(f"Primary Driver: {exp['primary_driver']}")
    print(f"Top Features: {exp['top_features']}")
    print(f"Revenue: ₹{rev['revenue']}")
    print("==============================")