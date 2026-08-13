#Telco_Dataset
import pandas as pd

url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)

# Save the dataset locally in this project folder
df.to_csv("data/Telco-Customer-Churn.csv", index=False)

print("Dataset saved successfully!")
print(df.head())