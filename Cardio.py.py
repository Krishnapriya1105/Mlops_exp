
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif

file_path = "cardio_train.csv"
df = pd.read_csv(file_path, delimiter=";")

df.drop(columns=['id'], inplace=True)

df['age'] = df['age'] // 365

imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_imputed.drop('cardio', axis=1)), columns=df_imputed.drop('cardio', axis=1).columns)

df_scaled['cardio'] = df_imputed['cardio']

correlations = df_scaled.corr()['cardio'].sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

plt.figure(figsize=(10, 6))
correlations.drop('cardio').plot(kind='bar', color='b')
plt.title("Correlation Between Features and Target")
plt.ylabel("Correlation Coefficient")
plt.axhline(0, color='red', linestyle='--', linewidth=1)
plt.tight_layout()
plt.show()

selected_features = correlations[abs(correlations) > 0.1].index.drop('cardio').tolist()
print("Selected Features for Model Training:", selected_features)

X = df[selected_features]
y = df['cardio']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.2f}")

plt.figure(figsize=(8, 6))
sns.histplot(y_prob, kde=True, bins=20, color='blue', label='Predicted Probabilities')
plt.axvline(0.5, color='red', linestyle='--', label='Threshold (0.5)')
plt.title("Distribution of Predicted Probabilities")
plt.xlabel("Probability of High Risk")
plt.ylabel("Frequency")
plt.legend()
plt.show()

import pandas as pd
def predict_heart_disease(model):
    print("\n--- Heart Disease Risk Prediction ---")
    age = int(input("Enter your age (in years): "))
    cholesterol = int(input("Enter your cholesterol level (1: Normal, 2: Above Normal, 3: Well Above Normal): "))
    weight = float(input("Enter your weight (in kg): "))
    user_data = pd.DataFrame({
        'age': [age],
        'cholesterol': [cholesterol],
        'weight': [weight]
    })
    probability = model.predict_proba(user_data)[:, 1][0]  # Probability of being high risk (class 1)
    risk_category = "High Risk" if probability > 0.5 else "Low Risk"
    print("\n--- Prediction Results ---")
    print(f"Predicted Probability of Heart Disease: {probability:.2f}")
    print(f"Risk Category: {risk_category}\n")
    print("______________________________________________________________")
def menu():
    while True:
        print("=== Heart Disease Prediction Menu ===")
        print("1. Predict Heart Disease Risk")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            predict_heart_disease(model)
        elif choice == '2':
            print("Exiting the program. Stay healthy!")
            break
        else:
            print("Invalid choice. Please try again.\n")
menu()

print("URK22CS1192")


add