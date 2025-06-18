#sales data analaysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("large_sales_data_with_nans.csv")

# data cleaning and handling nan values
df.columns = df.columns.str.strip().str.lower()
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print()
print(df.columns)
print()
print(df)
print()
duplicated_rows = df[df.duplicated()]
print("duplicated rows")
print(duplicated_rows)
print("total duplicate values--> ",df.duplicated().sum())
print()
df.drop_duplicates(keep="first",inplace=True)
print()
check_duplicatevalues = df.duplicated().sum()
print("after removing duplicates-> ",check_duplicatevalues)
print()
print(df)
print()

print("Nan values")
print(df.isnull().sum())
print()
Filling_nan_values = df.fillna({'product':df['product'].mode(),'category':df['category'].mode(),'quantity sold':df['quantity sold'].median(),
                                'total sales':df['total sales'].median(),'customer age':df['customer age'].median()},inplace=True)
print("after filling nan values")
check_nanvalues = df.isnull().sum()
print(check_nanvalues)
print(df)


#top performing products
products_sales = df.groupby(['product','category'])[['quantity sold','total sales']].sum().reset_index()
top_products = products_sales.sort_values(by="total sales",ascending=False)
print(top_products)
print()

#top performing category(niche)
category_sales = df.groupby('category')[['quantity sold','total sales']].sum().reset_index()
top_category = category_sales.sort_values(by="total sales", ascending=False)
print(top_category)
print()

#avg consumer age grp acc. to product
avg_people = df.groupby("product")['customer age'].median().reset_index()
avg_group = avg_people.sort_values(by="product")
print(avg_group)
print()


#peak sales trend

date_groupedby = df.groupby('date')['total sales'].sum().reset_index()
peak_sales_day = date_groupedby.sort_values(by="total sales",ascending=False).head()
print(peak_sales_day)


#data visualization

#customer age distribution
plt.figure(figsize=(10,5))
sns.histplot(df["customer age"], bins= np.arange(20,70,5),kde =True, color="blue")
plt.title("customer age distribution")
plt.xlabel('Age')
plt.ylabel('Number of customer')
plt.xticks(np.arange(20,70,5))
plt.show()

# #customer age distribution acc. to products
plt.figure(figsize=(12,5))
product_customer_counts = df.groupby("product")['customer age'].count().reset_index()
sns.barplot(x= 'product',y= 'customer age',data=product_customer_counts, palette="viridis")
plt.title("Customer Distribution by product")
plt.xlabel('Products')
plt.ylabel('Number of customers ')
plt.xticks(rotation=40)
plt.show()


# #sales trend over time (lineplot)

plt.figure(figsize=(12,5))
sns.lineplot(x= 'date',y= 'total sales',data= date_groupedby, color = "yellow")
plt.title("Sales trend over time")
plt.xlabel('Date')
plt.ylabel('Sales')
plt.xticks(rotation = 40)
plt.show()


# #sales trend (scatterplot)

plt.figure(figsize=(12,5))
sns.scatterplot(x= 'date',y= 'total sales',data= date_groupedby, color = "yellow")
plt.title("Sales trend over time")
plt.xlabel('Date')
plt.ylabel('Sales')
plt.xticks(rotation = 40)
plt.show()



# Plotly Visualizations

# Customer Age Distribution

import plotly.express as px
import plotly.graph_objects as go

fig1 = px.histogram(df, x="customer age", nbins=5, title="Customer Age Distribution",
                    labels={'customer age': 'Age'}, color_discrete_sequence=['red'])
fig1.show()

# Customer Distribution by Product
fig2 = px.bar(df.groupby("product")['customer age'].count().reset_index(), x='product', y='customer age',
              title="Customer Distribution by Product", labels={'customer age': 'Number of Customers'},
              color='product', color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.show()

# Sales Trend Over Time (Line Chart)
fig3 = px.line(date_groupedby, x='date', y='total sales', title="Sales Trend Over Time",
               labels={'total sales': 'Sales', 'date': 'Date'}, line_shape='spline',
               color_discrete_sequence=['gold'])
fig3.show()

# Sales Trend (Scatter Plot)
fig4 = px.scatter(date_groupedby, x='date', y='total sales', title="Sales Trend Over Time (Scatter)",
                  labels={'total sales': 'Sales', 'date': 'Date'}, color_discrete_sequence=['red'])
fig4.show()


