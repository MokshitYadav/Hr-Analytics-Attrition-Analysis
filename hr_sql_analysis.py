import pandas as pd
import sqlite3

df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')

conn = sqlite3.connect(':memory:')
df.to_sql('employees', conn, index=False, if_exists='replace')

print("--- SQL ANALYSIS ---")

q1 = pd.read_sql_query("SELECT Attrition, COUNT(*) as Total FROM employees GROUP BY Attrition", conn)
print("\nQ1 - Attrition Count:\n", q1)

q2 = pd.read_sql_query("SELECT Department, Attrition, COUNT(*) as Total FROM employees GROUP BY Department, Attrition ORDER BY Department", conn)
print("\nQ2 - Attrition by Department:\n", q2)

q3 = pd.read_sql_query("SELECT Attrition, ROUND(AVG(MonthlyIncome),2) as Avg_Income FROM employees GROUP BY Attrition", conn)
print("\nQ3 - Average Income by Attrition:\n", q3)

q4 = pd.read_sql_query("SELECT Attrition, ROUND(AVG(Age),2) as Avg_Age FROM employees GROUP BY Attrition", conn)
print("\nQ4 - Average Age by Attrition:\n", q4)

q5 = pd.read_sql_query("SELECT OverTime, Attrition, COUNT(*) as Total FROM employees GROUP BY OverTime, Attrition ORDER BY OverTime", conn)
print("\nQ5 - Overtime vs Attrition:\n", q5)

q6 = pd.read_sql_query("SELECT JobRole, COUNT(*) as Left_Company FROM employees WHERE Attrition='Yes' GROUP BY JobRole ORDER BY Left_Company DESC", conn)
print("\nQ6 - Top Job Roles with Attrition:\n", q6)

conn.close()
print("\n--- SQL ANALYSIS COMPLETE ---")