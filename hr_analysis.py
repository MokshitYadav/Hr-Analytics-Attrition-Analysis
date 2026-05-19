import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')

print("Shape:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nAttrition Value Counts:\n", df['Attrition'].value_counts())

df = df.drop(columns=['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours'])

df['Attrition_Binary'] = (df['Attrition'] == 'Yes').astype(int)

print("\n--- DATA CLEANING ---")
print("Shape after cleaning:", df.shape)
print("\nColumns dropped: EmployeeCount, EmployeeNumber, Over18, StandardHours")
print("\nAttrition_Binary added:")
print(df['Attrition_Binary'].value_counts())
print("\nCleaning Complete!")

print("\n--- EDA CHARTS ---")

plt.figure(figsize=(6,4))
df['Attrition'].value_counts().plot(kind='bar', color=['steelblue','tomato'])
plt.title('Attrition Count')
plt.xlabel('Attrition')
plt.ylabel('Number of Employees')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('outputs/chart1_attrition_count.png')
plt.show()
print("Chart 1 saved!")

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='Department', hue='Attrition', palette=['steelblue','tomato'])
plt.title('Attrition by Department')
plt.xlabel('Department')
plt.ylabel('Number of Employees')
plt.tight_layout()
plt.savefig('outputs/chart2_attrition_by_department.png')
plt.show()
print("Chart 2 saved!")

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='Attrition', y='MonthlyIncome', palette=['steelblue','tomato'])
plt.title('Monthly Income vs Attrition')
plt.xlabel('Attrition')
plt.ylabel('Monthly Income')
plt.tight_layout()
plt.savefig('outputs/chart3_income_vs_attrition.png')
plt.show()
print("Chart 3 saved!")

plt.figure(figsize=(8,5))
sns.histplot(data=df, x='Age', hue='Attrition', bins=30, palette=['steelblue','tomato'])
plt.title('Age Distribution by Attrition')
plt.xlabel('Age')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('outputs/chart4_age_distribution.png')
plt.show()
print("Chart 4 saved!")

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='JobSatisfaction', hue='Attrition', palette=['steelblue','tomato'])
plt.title('Job Satisfaction vs Attrition')
plt.xlabel('Job Satisfaction (1=Low, 4=High)')
plt.ylabel('Number of Employees')
plt.tight_layout()
plt.savefig('outputs/chart5_jobsatisfaction_vs_attrition.png')
plt.show()
print("Chart 5 saved!")

plt.figure(figsize=(7,5))
sns.countplot(data=df, x='OverTime', hue='Attrition', palette=['steelblue','tomato'])
plt.title('Overtime vs Attrition')
plt.xlabel('OverTime')
plt.ylabel('Number of Employees')
plt.tight_layout()
plt.savefig('outputs/chart6_overtime_vs_attrition.png')
plt.show()
print("Chart 6 saved!")
print("\n--- ALL 6 CHARTS DONE! ---")

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

print("\n--- MACHINE LEARNING MODEL ---")

df_ml = df.copy()

cat_cols = df_ml.select_dtypes(include='object').columns
le = LabelEncoder()
for col in cat_cols:
    df_ml[col] = le.fit_transform(df_ml[col])

X = df_ml.drop(columns=['Attrition', 'Attrition_Binary'])
y = df_ml['Attrition_Binary']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

print("Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(data=feature_importance, x='Importance', y='Feature', palette='Reds_r')
plt.title('Top 10 Factors Causing Employee Attrition')
plt.xlabel('Importance Score')
plt.ylabel('Factor')
plt.tight_layout()
plt.savefig('outputs/chart7_feature_importance.png')
plt.show()
print("Chart 7 - Feature Importance saved!")

df.to_csv('outputs/hr_clean_data.csv', index=False)
print("\nClean data exported for Power BI!")