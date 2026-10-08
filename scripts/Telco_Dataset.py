#Telco_Dataset
import pandas as pd
from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)

url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)

# Save the dataset locally in this project folder
df.to_csv("data/Telco-Customer-Churn.csv", index=False)

print("Dataset saved successfully!")
print(df.head())