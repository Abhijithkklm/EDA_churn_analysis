
# Customer Churn Analysis – Exploratory Data Analysis (EDA)

## 📌 Project Overview

This project focuses on exploring customer churn data using Python to understand customer behavior and identify patterns associated with customer attrition. Exploratory Data Analysis (EDA) was performed to examine data quality, customer characteristics, and churn rates across different customer segments.

The analysis uses statistical techniques and data visualizations to communicate findings that may help businesses develop customer retention strategies.

## 🎯 Objectives

- Understand the overall customer churn distribution.
- Identify missing values and duplicate records.
- Detect outliers in monthly customer charges using the IQR method.
- Analyze churn across different contract types and payment methods.
- Explore the relationship between customer satisfaction and churn.
- Investigate churn patterns based on support tickets and customer age.
- Present findings through visualizations.

## 🛠️ Tools & Technologies

- **Python** – Data analysis
- **Pandas** – Data manipulation and analysis
- **Matplotlib** – Data visualization
- **Jupyter Notebook / Python** – Analysis workflow

## 📊 Analysis Performed

### 1. Data Quality Analysis
- Inspected dataset structure, columns, and data types.
- Checked missing values.
- Checked duplicate records and duplicate customer IDs.
- Generated descriptive statistics.

### 2. Outlier Detection
- Calculated Q1, Q3, and the Interquartile Range (IQR).
- Identified potential outliers in monthly charges.
- Examined outlier customers across selected attributes.

### 3. Customer Churn Analysis
- Examined the distribution of churned and retained customers.
- Compared churn rates across contract types.
- Analyzed churn in relation to payment methods.
- Compared average satisfaction scores by churn status.
- Investigated churn among month-to-month customers with lower satisfaction scores.

### 4. Customer Behavior Analysis
- Explored churn patterns across age groups.
- Examined churn rates by the number of support tickets.
- Visualized the relationship between customer age and monthly charges.
- Analyzed satisfaction scores among churned customers.

## 📈 Key Findings

- The overall churn rate in the analyzed dataset was approximately **26.2%**.
- Month-to-month customers showed a higher churn rate than customers with longer-term contracts.
- Customers on two-year contracts had a lower observed churn rate than customers on one-year or month-to-month contracts.
- Monthly charges were examined for potential outliers using the IQR method.
- Customer satisfaction, payment methods, and support ticket counts were explored to identify patterns associated with churn.

*Note: Findings describe patterns in the dataset and do not establish that any individual factor causes customer churn.*

## 💡 Business Recommendations

- Investigate the reasons for higher churn among month-to-month customers.
- Consider targeted retention strategies for customer segments with higher observed churn rates.
- Review customer satisfaction and support ticket patterns to identify possible service improvement opportunities.
- Evaluate payment-related issues that may be associated with customer attrition.
- Monitor churn trends regularly to support data-driven retention decisions.

## 📂 Project Structure

```text
customer-churn-eda/
│
├── churn.py
├── README.md
├── requirements.txt
└── data/
    └── customer_churn_analysis_2000.csv
```

*The dataset folder is optional if the data cannot be redistributed. Update this structure to match the files actually uploaded to your repository.*

## ⚙️ How to Run the Project

### Prerequisites
Install Python and the required libraries.

### Install dependencies

```bash
pip install pandas matplotlib
```

### Run the analysis

1. Clone or download this repository.
2. Place the dataset in the appropriate location.
3. Update the CSV file path in `churn.py` if necessary.
4. Run the script:

```bash
python churn.py
```

The script prints data-quality checks and statistical results and displays visualizations for the analyses performed.

## 🚀 Future Improvements

- Develop an interactive dashboard using Streamlit.
- Add interactive filters for customer segments.
- Improve visualization formatting and dashboard presentation.
- Explore additional customer characteristics to understand churn patterns.

## 👤 Author

**Data Analytics Portfolio Project**

This project
