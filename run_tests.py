import sqlite3
import scipy.stats as stats
import pandas as pd

import subprocess
subprocess.run(['python3', 'clean_data.py'])
subprocess.run(['python3', 'load_to_db.py'])

connection = sqlite3.connect('db/abtest.db')
cursor = connection.cursor()

query1 = """
SELECT 
    SUM(CASE WHEN converted = 0 THEN 1 ELSE 0 END),
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END)
FROM ab_test
GROUP BY "group"
ORDER BY "group";
"""

cursor.execute(query1)
rows = cursor.fetchall() # Returns a list of tuples like [(control_0, control_1), (test_0, test_1)]

chi2, p_chi, dof, expected = stats.chi2_contingency(rows)

print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"P-value: {p_chi:.4f}")

if p_chi < 0.05:
    print("Result is statistically significant (Reject Null Hypothesis)")
else:
    print("Result is not statistically significant (Fail to reject Null Hypothesis)")


# Test 2 
query2 = """SELECT converted FROM ab_test WHERE "group" = 'control';"""
query3 = """SELECT converted FROM ab_test WHERE "group" = 'treatment';"""
cursor.execute(query2)
control_converted = [row[0] for row in cursor.fetchall()]
cursor.execute(query3)
treatment_converted = [row[0] for row in cursor.fetchall()]

t_stat, p_t = stats.ttest_ind(control_converted, treatment_converted, alternative='two-sided')
print(f"T-Statistic: {t_stat:.4f}")
print(f"P-value: {p_t:.4f}")

if p_t < 0.05:
    print("Reject H₀ — significant difference between groups")
else:
    print("Fail to reject H₀ — no significant difference")

u_stat, p_u = stats.mannwhitneyu(control_converted, treatment_converted, alternative='two-sided')
print(f"Mann-Whitney U Statistic: {u_stat:.4f}")
print(f"P-value: {p_u:.4f}")

if p_u < 0.05:
    print("Reject H₀ — significant difference between groups")
else:
    print("Fail to reject H₀ — no significant difference")

df = pd.DataFrame({
    'Test': ['Chi-Square', 'T-Test', 'Mann-Whitney U'],
    'Statistic': [chi2, t_stat, u_stat],
    'P-Value': [p_chi, p_t, p_u],
    'Result': [
        'Reject H₀' if p_chi < 0.05 else 'Fail to reject H₀',
        'Reject H₀' if p_t < 0.05 else 'Fail to reject H₀',
        'Reject H₀' if p_u < 0.05 else 'Fail to reject H₀',
    ],
    'Conclusion': [
        'Significant difference in conversion rates' if p_chi < 0.05 else 'No significant difference in conversion rates',
        'Significant difference in conversion rates' if p_t < 0.05 else 'No significant difference in conversion rates',
        'Significant difference in conversion rates' if p_u < 0.05 else 'No significant difference in conversion rates',
    ]
})

df.to_excel('outputs/ab_report.xlsx', index=False)
connection.close()
