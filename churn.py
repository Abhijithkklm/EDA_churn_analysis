from operator import index

import pandas as pd
from fontTools.diff import color
from fontTools.varLib import plot
from matplotlib.lines import lineStyles
from packaging import markers
from pandas import crosstab
from pandas.core.algorithms import duplicated
from unicodedata import normalize

df=pd.read_csv("D:/manhaw/customer_churn_analysis_2000.csv")
print(df.info())
print(df.shape)
print(df.head)

print(df.isna().sum())
print(df.duplicated().sum())
print(df["CustomerID"].duplicated().sum())
print(df.describe().T)




q1=df["MonthlyCharges"].quantile(0.25)
q3=df["MonthlyCharges"].quantile(0.75)

iqr=q3-q1

lower_limit=q1-1.5*iqr
upper_limit=q3+1.5*iqr

outliers=(
        (df["MonthlyCharges"]<lower_limit) |
        (df["MonthlyCharges"]>upper_limit)
)

print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Lower limit:", lower_limit)
print("Upper limit:", upper_limit)
print("Number of outliers:", len(outliers))




#
#
# outlier_condition = (
#     (df["MonthlyCharges"] < lower_limit) |
#    (df["MonthlyCharges"] > upper_limit)
# )

print(outliers.value_counts())
print("Actual number of outliers:", outliers.sum())


outliers_val=df[outliers]

print(outliers_val[["CustomerID","MonthlyCharges"]])

print(
    outliers_val[
        [
            "CustomerID",
            "MonthlyCharges",
            "ContractType",
            "DiscountApplied",
            "InternetService",
            "TenureMonths"
        ]
    ]
.T)

print(outliers_val["Churn"].value_counts())

print(df["Churn"].value_counts(normalize=True)*100)


print(df.groupby("ContractType")["Churn"].value_counts(normalize=True)*100)



print(df.groupby("Churn")["SatisfactionScore"].mean())

high_risk = df[
    (df["ContractType"] == "Month-to-month") &
    (df["SatisfactionScore"] <= 2)
]

print(high_risk["Churn"].value_counts())


age_contract=(df.groupby("Age")
     ["ContractType"].value_counts(normalize=True)*100)

print(age_contract)


age_churn=(df.groupby("Age")["Churn"].value_counts(normalize=True))
print(age_churn)


print(df.columns)


discount_based_churn=pd.crosstab(df["DiscountApplied"],df["Churn"],normalize="index")*100

print(discount_based_churn)





import matplotlib.pyplot as plt

churn_percentage = df["Churn"].value_counts(normalize=True) * 100

plt.bar(churn_percentage.index, churn_percentage.values)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn Status")
plt.ylabel("Percentage of Customers")

plt.show()




churn_percentage_satisfaction=df.groupby("Churn")["SatisfactionScore"].mean()

plt.bar(
    churn_percentage_satisfaction.index,
    churn_percentage_satisfaction.values
)
plt.title("average satissfaction by churn percentage")
plt.xlabel("churn status")
plt.ylabel("average satisfaction score")

plt.show()


churn_rate_contract_type = pd.crosstab(
    df["ContractType"],
    df["Churn"],
    normalize="index"
) * 100


plt.bar(churn_rate_contract_type.index,
        churn_rate_contract_type["Yes"]
        )

plt.title("churn rate by contract type")
plt.xlabel("contract type ")
plt.ylabel("churn rate ")
plt.show()



churn_payment=pd.crosstab(df["PaymentMethod"],
                  df["Churn"],normalize="index")*100


plt.bar(churn_payment.index,
        churn_payment["Yes"])
plt.title("customer churn due to payment ")
plt.xlabel("payment type  ")
plt.ylabel("customer churn percentage ")
plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Select customers who have churned
churned_customers = df[df["Churn"] == "Yes"]

# Count churned customers by contract type
contract_counts = churned_customers["ContractType"].value_counts()

# Plot pie chart
plt.pie(
    contract_counts.values,
    labels=contract_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribution of Churned Customers by Contract Type")
plt.show()


print(df.isna().sum())

churned_customers = df[df["Churn"] == "Yes"]

satisfaction_counts = churned_customers["SatisfactionScore"].value_counts().sort_index()

plt.pie(
    satisfaction_counts.values,
    labels=satisfaction_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Satisfaction Scores Among Churned Customers")
plt.show()



df["ChurnDate"] = df["ChurnDate"].fillna("Date unavailable")



support_ticket=pd.crosstab(df["SupportTickets"],
                           df["Churn"],normalize="index")
plt.bar(support_ticket.index,support_ticket["Yes"])

plt.plot(support_ticket.index,support_ticket["Yes"],marker="o",linestyle="--",color="Red")


plt.title("Churn Rate by Number of Support Tickets")
plt.xlabel("Number of Support Tickets")
plt.ylabel("Churn Rate (%)")
plt.show()


plt.scatter(df["Age"],df["MonthlyCharges"])
plt.title("Age vs Monthly charges")
plt.title("Relationship Between Customer Age and Monthly Charges")
plt.xlabel("Customer Age (Years)")
plt.ylabel("Monthly Charges")
plt.show()



plt.hist(df["Age"], bins=20)


plt.title("Distribution of Customer Ages")

plt.xlabel("Age")
plt.ylabel("Frequency")

plt.show()