
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

# -------------------------------
# 1. Page configuration
# -------------------------------
st.set_page_config(
    page_title="Customer Churn Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Churn Analysis Dashboard")
st.write(
    "Exploratory Data Analysis of customer churn using Python, "
    "Pandas and Matplotlib."
)

# -------------------------------
# 2. Load dataset
# -------------------------------
DATA_FILE = Path(__file__).parent / "customer_churn_analysis_2000.csv"

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

try:
    df = load_data(str(DATA_FILE))
except FileNotFoundError:
    st.error(
        "Dataset not found. Upload customer_churn_analysis_2000.csv "
        "to the same GitHub repository folder as app.py."
    )
    st.stop()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

st.success("Dataset loaded successfully!")

# -------------------------------
# 3. Data overview
# -------------------------------
st.header("1. Data Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rows", f"{df.shape[0]:,}")
col2.metric("Total Columns", f"{df.shape[1]:,}")
col3.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

with st.expander("View first five rows"):
    st.dataframe(df.head(), use_container_width=True)

with st.expander("View dataset information"):
    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isna().sum().values
    })
    st.dataframe(info_df, use_container_width=True)

with st.expander("View descriptive statistics"):
    st.dataframe(df.describe(include="all").T, use_container_width=True)

# -------------------------------
# 4. Missing values and duplicates
# -------------------------------
st.header("2. Data Quality Analysis")

missing_values = df.isna().sum().sort_values(ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Missing Values by Column")
    st.dataframe(
        missing_values.rename("Missing Values").to_frame(),
        use_container_width=True
    )

with col2:
    st.subheader("Duplicate Customer IDs")

    if "CustomerID" in df.columns:
        st.metric(
            "Duplicate Customer IDs",
            f"{df['CustomerID'].duplicated().sum():,}"
        )
    else:
        st.info("CustomerID column is not available.")

# -------------------------------
# 5. Monthly charges outliers
# -------------------------------
st.header("3. Outlier Detection — Monthly Charges")

if "MonthlyCharges" in df.columns:
    q1 = df["MonthlyCharges"].quantile(0.25)
    q3 = df["MonthlyCharges"].quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    outliers = (
        (df["MonthlyCharges"] < lower_limit) |
        (df["MonthlyCharges"] > upper_limit)
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Q1", f"{q1:.2f}")
    col2.metric("Q3", f"{q3:.2f}")
    col3.metric("IQR", f"{iqr:.2f}")
    col4.metric("Number of Outliers", f"{outliers.sum():,}")

    st.write(
        f"Lower limit: {lower_limit:.2f} | "
        f"Upper limit: {upper_limit:.2f}"
    )

    outlier_columns = [
        column for column in [
            "CustomerID",
            "MonthlyCharges",
            "ContractType",
            "DiscountApplied",
            "InternetService",
            "TenureMonths",
            "Churn"
        ]
        if column in df.columns
    ]

    with st.expander("View outlier customer details"):
        st.dataframe(
            df.loc[outliers, outlier_columns],
            use_container_width=True
        )

    if "Churn" in df.columns:
        st.subheader("Churn Status Among Outliers")
        st.dataframe(
            df.loc[outliers, "Churn"]
            .value_counts()
            .rename_axis("Churn Status")
            .to_frame("Customer Count")
        )

# -------------------------------
# 6. Overall churn distribution
# -------------------------------
st.header("4. Customer Churn Analysis")

if "Churn" in df.columns:
    churn_counts = df["Churn"].value_counts()
    churn_percentages = df["Churn"].value_counts(normalize=True) * 100

    col1, col2, col3 = st.columns(3)

    total_customers = len(df)
    churned_customers_count = int(df["Churn"].eq("Yes").sum())
    churn_rate = (
        churned_customers_count / total_customers * 100
        if total_customers > 0 else 0
    )

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Churned Customers", f"{churned_customers_count:,}")
    col3.metric("Overall Churn Rate", f"{churn_rate:.2f}%")

    fig, ax = plt.subplots()
    ax.bar(churn_percentages.index.astype(str), churn_percentages.values)
    ax.set_title("Customer Churn Distribution")
    ax.set_xlabel("Churn Status")
    ax.set_ylabel("Percentage of Customers")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("View churn percentages"):
        st.dataframe(
            churn_percentages.rename("Percentage").to_frame().round(2)
        )

# -------------------------------
# 7. Churn by contract type
# -------------------------------
if "ContractType" in df.columns and "Churn" in df.columns:
    st.subheader("Churn Rate by Contract Type")

    contract_churn = pd.crosstab(
        df["ContractType"],
        df["Churn"],
        normalize="index"
    ) * 100

    if "Yes" in contract_churn.columns:
        fig, ax = plt.subplots()
        ax.bar(
            contract_churn.index.astype(str),
            contract_churn["Yes"]
        )
        ax.set_title("Churn Rate by Contract Type")
        ax.set_xlabel("Contract Type")
        ax.set_ylabel("Churn Rate (%)")
        ax.tick_params(axis="x", rotation=15)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.dataframe(contract_churn.round(2), use_container_width=True)

# -------------------------------
# 8. Satisfaction by churn status
# -------------------------------
if "SatisfactionScore" in df.columns and "Churn" in df.columns:
    st.subheader("Average Satisfaction by Churn Status")

    satisfaction_by_churn = df.groupby("Churn")[
        "SatisfactionScore"
    ].mean()

    fig, ax = plt.subplots()
    ax.bar(
        satisfaction_by_churn.index.astype(str),
        satisfaction_by_churn.values
    )
    ax.set_title("Average Satisfaction Score by Churn Status")
    ax.set_xlabel("Churn Status")
    ax.set_ylabel("Average Satisfaction Score")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(
        satisfaction_by_churn.rename("Average Satisfaction").to_frame()
    )

# -------------------------------
# 9. Churn by payment method
# -------------------------------
if "PaymentMethod" in df.columns and "Churn" in df.columns:
    st.subheader("Churn Rate by Payment Method")

    payment_churn = pd.crosstab(
        df["PaymentMethod"],
        df["Churn"],
        normalize="index"
    ) * 100

    if "Yes" in payment_churn.columns:
        fig, ax = plt.subplots()
        ax.bar(
            payment_churn.index.astype(str),
            payment_churn["Yes"]
        )
        ax.set_title("Churn Rate by Payment Method")
        ax.set_xlabel("Payment Method")
        ax.set_ylabel("Churn Rate (%)")
        ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.dataframe(payment_churn.round(2), use_container_width=True)

# -------------------------------
# 10. Churned customers by contract
# -------------------------------
if "ContractType" in df.columns and "Churn" in df.columns:
    st.subheader("Contract Types Among Churned Customers")

    churned_df = df[df["Churn"].eq("Yes")]
    contract_counts = churned_df["ContractType"].value_counts()

    if not contract_counts.empty:
        fig, ax = plt.subplots()
        ax.pie(
            contract_counts.values,
            labels=contract_counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Distribution of Churned Customers by Contract Type")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No churned customers found.")

# -------------------------------
# 11. Satisfaction among churned customers
# -------------------------------
if "SatisfactionScore" in df.columns and "Churn" in df.columns:
    st.subheader("Satisfaction Scores Among Churned Customers")

    churned_df = df[df["Churn"].eq("Yes")]
    satisfaction_counts = (
        churned_df["SatisfactionScore"].value_counts().sort_index()
    )

    if not satisfaction_counts.empty:
        fig, ax = plt.subplots()
        ax.pie(
            satisfaction_counts.values,
            labels=satisfaction_counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Satisfaction Scores Among Churned Customers")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No satisfaction data available for churned customers.")

# -------------------------------
# 12. High-risk customer segment
# -------------------------------
if all(
    column in df.columns
    for column in ["ContractType", "SatisfactionScore", "Churn"]
):
    st.header("5. Customer Segment Analysis")

    high_risk = df[
        (df["ContractType"] == "Month-to-month") &
        (df["SatisfactionScore"] <= 2)
    ]

    st.subheader(
        "Month-to-Month Customers with Satisfaction Score 2 or Below"
    )
    st.metric("Customers in Segment", f"{len(high_risk):,}")

    st.dataframe(
        high_risk["Churn"]
        .value_counts()
        .rename_axis("Churn Status")
        .to_frame("Customer Count"),
        use_container_width=True
    )

# -------------------------------
# 13. Churn by discount
# -------------------------------
if "DiscountApplied" in df.columns and "Churn" in df.columns:
    st.subheader("Churn by Discount Applied")

    discount_churn = pd.crosstab(
        df["DiscountApplied"],
        df["Churn"],
        normalize="index"
    ) * 100

    st.dataframe(discount_churn.round(2), use_container_width=True)

# -------------------------------
# 14. Churn by support tickets
# -------------------------------
if "SupportTickets" in df.columns and "Churn" in df.columns:
    st.subheader("Churn Rate by Number of Support Tickets")

    support_churn = pd.crosstab(
        df["SupportTickets"],
        df["Churn"],
        normalize="index"
    ) * 100

    if "Yes" in support_churn.columns:
        fig, ax = plt.subplots()
        ax.bar(
            support_churn.index.astype(str),
            support_churn["Yes"]
        )
        ax.plot(
            support_churn.index.astype(str),
            support_churn["Yes"],
            marker="o",
            linestyle="--"
        )
        ax.set_title("Churn Rate by Number of Support Tickets")
        ax.set_xlabel("Number of Support Tickets")
        ax.set_ylabel("Churn Rate (%)")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.dataframe(support_churn.round(2), use_container_width=True)

# -------------------------------
# 15. Age and monthly charges
# -------------------------------
if "Age" in df.columns and "MonthlyCharges" in df.columns:
    st.header("6. Customer Demographics")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.scatter(df["Age"], df["MonthlyCharges"], alpha=0.7)
        ax.set_title("Relationship Between Age and Monthly Charges")
        ax.set_xlabel("Customer Age")
        ax.set_ylabel("Monthly Charges")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.hist(df["Age"].dropna(), bins=20)
        ax.set_title("Distribution of Customer Ages")
        ax.set_xlabel("Customer Age")
        ax.set_ylabel("Number of Customers")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    if "ContractType" in df.columns:
        st.subheader("Contract Type by Age")
        age_contract = pd.crosstab(
            df["Age"],
            df["ContractType"],
            normalize="index"
        ) * 100
        st.dataframe(age_contract.round(2), use_container_width=True)

    if "Churn" in df.columns:
        st.subheader("Churn Distribution by Age")
        age_churn = pd.crosstab(
            df["Age"],
            df["Churn"],
            normalize="index"
        ) * 100
        st.dataframe(age_churn.round(2), use_container_width=True)

# -------------------------------
# 16. Churn date missing values
# -------------------------------
if "ChurnDate" in df.columns:
    st.header("7. Churn Date Data")
    st.metric(
        "Missing Churn Dates",
        f"{df['ChurnDate'].isna().sum():,}"
    )
    st.caption(
        "Missing dates are reported without replacing them with text, "
        "so the original column remains suitable for analysis."
    )

# -------------------------------
# 17. Key observations
# -------------------------------
st.header("Key Observations")

st.markdown(
    """
    - Compare churn rates across contract types and payment methods.
    - Examine satisfaction scores and support ticket patterns for customer segments
      with higher observed churn.
    - Review monthly charge outliers to understand unusual values.
    - Use these findings to investigate possible retention opportunities.
    
    **Note:** These analyses identify associations in the dataset; they do not
    prove that any factor causes customer churn.
    """
)

st.caption("Customer Churn EDA | Built with Python, Pandas, Matplotlib and Streamlit")
