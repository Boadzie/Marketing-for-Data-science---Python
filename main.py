import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def main():
    pages = ['Home', 'Conversion', 'Product Analytics']

    option = st.sidebar.selectbox('Data Science for Marketing Dashboards', options=pages)

    if option == 'Home':
        st.markdown('# Marketing Dashbaords')
        st.markdown('This is a series of Marketing Dashboards showing various marketing Key Performance Indicator(KPIs) for a marketing Firm.'\
            'The app is built by [Boadzie Daniel](https://boadzie.surge.sh/) and The Students of [Artificial Intelligence Movement(AIM)](https://www.aimovement.club/)')
        st.image('./img/Dan.jpg', width=200)
        st.image('./img/AIM.jpeg', width=700)
        st.markdown('---')
        st.markdown('## References')
        st.markdown('''
                    1. [https://www.amazon.com/Hands-Data-Science-Marketing-strategies/dp/1789346347](https://www.amazon.com/Hands-Data-Science-Marketing-strategies/dp/1789346347)
                    
                    ''')
    elif option == 'Conversion':
        st.markdown('## Customer Conversion Dashboard')
        st.markdown('#### Loading our Dataset - [https://archive.ics.uci.edu/ml/datasets/bank+marketing](https://archive.ics.uci.edu/ml/datasets/bank+marketing)')
        st.markdown('---')
        ##########################################################
        data = load_data()
        st.dataframe(data[:100])
        st.write(f'**The shape of the data is {data.shape[0]} Rows and {data.shape[1]} Columns**') 
        st.markdown('---')
        ########################################################
        st.markdown('#### Aggregation by Conversion Rate') 
        agg = aggregate(data)
        st.success(agg)
        st.markdown('---')
        #########################################################
        st.markdown('#### Conversion Rate by Age') 
        age = by_age(data)
        st.pyplot(age)
        st.markdown('---')
        #########################################################
        st.markdown('#### Conversion Rate by Age Group') 
        age_group = by_age_group(data)
        st.pyplot(age_group)
        st.markdown('---')
        #########################################################
        st.markdown('#### Conversions vs Non-conversions') 
        non = conv_non(data)
        st.pyplot(non)
        st.markdown('---')
        #########################################################
        st.markdown('#### Conversion rate by Age and Marital Status') 
        marital = by_agemarital(data)
        st.pyplot(marital) 
        
    elif option == 'Product Analytics':
        st.markdown('## Product Analytics Dahsboard') 
        st.markdown('#### Loading Data - The data is from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/online+retail)')
        st.markdown('---')
        ##########################################################
        data = load_prod_data()
        st.dataframe(data[:100])
        st.write(f'**The shape of the data is {data.shape[0]} Rows and {data.shape[1]} Columns**') 
        st.markdown('---')
        ##########################################################
        st.markdown('#### Monthly Orders Trend') 
        plot = orders(data)
        st.pyplot(plot)
        st.markdown('---')
        #########################################################
        st.markdown('#### Monthly Revenue Trend') 
        plot = revenue(data)
        st.pyplot(plot)
        st.markdown('---')
        #########################################################
        st.markdown('#### Repeat Sales') 
        plot = repeat_customers(data)
        st.pyplot(plot)
        st.markdown('---')
        #########################################################
        st.markdown('#### Monthly Repeat Revenue') 
        plot = monthly_repeat_rev(data)
        st.pyplot(plot)
        st.markdown('---')
        #########################################################
        st.markdown('#### Item Analysis') 
        plot = item_analsis(data)
        st.pyplot(plot)
        st.markdown('---')
        #########################################################
            



@st.cache
def load_data():
    df = pd.read_csv("./data/bank-additional-full.csv", sep=';')
    df['conversion'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)
    return df

################### FUNCTIONS FOR CONVERSION DASHBOARD#########################
def aggregate(df):
    # total number of conversions
    total_cov = df.conversion.sum()
    # total number of clients in the data (= number of rows in the data)
    clients = df.shape[0]
    percent = round(total_cov/clients * 100, 2)
    return f'Total conversion  is {total_cov} out of {clients} representing {percent}%  conversion rate'

def by_age(df):
    conversions_by_age = df.groupby(by='age')['conversion'].sum() / df.groupby( by='age')['conversion'].count() * 100.0  
    
    # the plot
    ax = conversions_by_age.plot(
    grid=True,
    figsize=(10, 7),
    title='Conversion Rates by Age'
    ) 
    ax.set_xlabel('age')
    ax.set_ylabel('conversion rate (%)')


def by_age_group(df):
    df['age_group'] = df['age'].apply(
        lambda x: '[18, 30)' if x < 30 else '[30, 40)' if x < 40 \
        else '[40, 50)' if x < 50 else '[50, 60)' if x < 60 \
        else '[60, 70)' if x < 70 else '70+'
        )
    
    conversions_by_age_group = df.groupby(
        by='age_group'
        )['conversion'].sum() / df.groupby(
        by='age_group'
        )['conversion'].count() * 100.0
    
    #    the bar plot
    ax = conversions_by_age_group.loc[
    ['[18, 30)', '[30, 40)', '[40, 50)', '[50, 60)', '[60, 70)', '70+']
    ].plot(
        kind='bar',
        color='skyblue',
        grid=True,
        figsize=(10, 7),
        title='Conversion Rates by Age Groups'
    ) 
    ax.set_xlabel('age group')
    ax.set_ylabel('conversion rate (%)')
    

def conv_non(df):
    conversions_by_marital_status_df = pd.pivot_table(df, values='y', index='marital', columns='conversion', aggfunc=len)
    conversions_by_marital_status_df.plot(
    kind='pie',
    figsize=(15, 7),
    startangle=90,
    subplots=True,
    autopct=lambda x: '%0.1f%%' % x
    ) 


def by_agemarital(df):
    age_marital_df = df.groupby(['age_group', 'marital'])['conversion'].sum().unstack('marital').fillna(0)
    age_marital_df = age_marital_df.divide(
    df.groupby(
    by='age_group'
    )['conversion'].count(),
    axis=0
    )
    
    # The plot
    ax = age_marital_df.loc[
    ['[18, 30)', '[30, 40)', '[40, 50)', '[50, 60)', '[60, 70)', '70+']
    ].plot(
    kind='bar',
    grid=True,
    figsize=(10,7)
    ) 
    ax.set_title('Conversion rates by Age & Marital Status')
    ax.set_xlabel('age group')
    ax.set_ylabel('conversion rate (%)')


################### FUNCTIONS FOR PRODUCTS DASHBOARD#########################

@st.cache()
def load_prod_data():
    df = pd.read_excel(io ="./data/Online-Retail.xlsx", sheet_name='Online Retail')
    # df['conversion'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)
    return df
    

# revenue trend
def orders(df):
    monthly_orders_df = df.set_index('InvoiceDate')['InvoiceNo'].resample('M').nunique()
    # the plot
    ax = pd.DataFrame(monthly_orders_df.values).plot(
        grid=True,
        figsize=(10,7),
        legend=False
    ) 
    ax.set_xlabel('date')
    ax.set_ylabel('number of orders/invoices')
    ax.set_title('Total Number of Orders Over Time')
    plt.xticks(range(len(monthly_orders_df.index)),
        [x.strftime('%m.%Y') for x in monthly_orders_df.index],
        rotation=45
    )
    
def revenue(df):
    df['Sales'] = df['Quantity'] * df['UnitPrice']
    monthly_revenue_df = df.set_index('InvoiceDate')['Sales'].resample('M').sum()
    # the plot
    ax = pd.DataFrame(monthly_revenue_df.values).plot(
        grid=True,
        figsize=(10,7),
        legend=False
    )
    ax.set_xlabel('date')
    ax.set_ylabel('sales')
    ax.set_title('Total Revenue Over Time')
    ax.set_ylim([0, max(monthly_revenue_df.values)+100000])
    plt.xticks(range(len(monthly_revenue_df.index)),
        [x.strftime('%m.%Y') for x in monthly_revenue_df.index],
        rotation=45
    )

def repeat_customers(df):
    # order by invoice
    invoice_customer_df = df.groupby(
        by=['InvoiceNo', 'InvoiceDate']
        ).agg({
        'Sales': sum,
        'CustomerID': max,
        'Country': max,
        }).reset_index()
        
    # agg per month and no of customers
    monthly_repeat_customers_df = invoice_customer_df.set_index('InvoiceDate').groupby([
    pd.Grouper(freq='M'), 'CustomerID'
    ]).filter(lambda x: len(x) > 1).resample('M').nunique()['CustomerID']
    
    # monthly unique customers
    monthly_unique_customers_df = df.set_index('InvoiceDate')['CustomerID'].resample('M').nunique()
    
    # repeat percentage
    monthly_repeat_percentage = monthly_repeat_customers_df/monthly_unique_customers_df*100
    
    # the plot 
    ax = pd.DataFrame(monthly_repeat_customers_df.values).plot(
    figsize=(10,7)
    ) 
    pd.DataFrame(monthly_unique_customers_df.values).plot(
        ax=ax,
        grid=True
    ) 
    ax2 = pd.DataFrame(monthly_repeat_percentage.values).plot.bar(
        ax=ax,
        grid=True,
        secondary_y=True,
        color='green',
        alpha=0.2
    ) 
    ax.set_xlabel('date')
    ax.set_ylabel('number of customers')
    ax.set_title('Customers vs. Repeat Customers Over Time')
    ax2.set_ylabel('percentage (%)')
    ax.legend(['Repeat Customers', 'All Customers'])
    ax2.legend(['Percentage of Repeat'], loc='upper right')
    ax.set_ylim([0, monthly_unique_customers_df.values.max()+100])
    ax2.set_ylim([0, 100])
    plt.xticks(
    range(len(monthly_repeat_customers_df.index)),
    [x.strftime('%m.%Y') for x in monthly_repeat_customers_df.index],
    rotation=45
    )

def monthly_repeat_rev(df):
    invoice_customer_df = df.groupby(
        by=['InvoiceNo', 'InvoiceDate']
        ).agg({
        'Sales': sum,
        'CustomerID': max,
        'Country': max,
        }).reset_index()
    
    # monthly rev df
    monthly_revenue_df = df.set_index('InvoiceDate')['Sales'].resample('M').sum()
        
    monthly_rev_repeat_customers_df = invoice_customer_df.set_index('InvoiceDate').groupby([
    pd.Grouper(freq='M'), 'CustomerID']).filter(lambda x: len(x) > 1).resample('M').sum()['Sales']
    monthly_rev_perc_repeat_customers_df = monthly_rev_repeat_customers_df/monthly_revenue_df
    
    # the plot
    ax = pd.DataFrame(monthly_revenue_df.values).plot(figsize=(12,9))
    pd.DataFrame(monthly_rev_repeat_customers_df.values).plot(
    ax=ax,
    grid=True,
    ) 
    ax.set_xlabel('date')
    ax.set_ylabel('sales')
    ax.set_title('Total Revenue vs. Revenue from Repeat Customers')
    ax.legend(['Total Revenue', 'Repeat Customer Revenue'])
    ax.set_ylim([0, max(monthly_revenue_df.values)+100000])
    ax2 = ax.twinx()
    pd.DataFrame(monthly_rev_perc_repeat_customers_df.values).plot(
        ax=ax2,
        kind='bar',
        color='g',
        alpha=0.2
    ) 
    ax2.set_ylim([0, max(monthly_rev_perc_repeat_customers_df.values)+30])
    ax2.set_ylabel('percentage (%)')
    ax2.legend(['Repeat Revenue Percentage'])
    ax2.set_xticklabels([
    x.strftime('%m.%Y') for x in monthly_rev_perc_repeat_customers_df.index])
 
# Item analysis
def item_analsis(df):
    # unique items sold
    date_item_df = df.set_index('InvoiceDate').groupby([
    pd.Grouper(freq='M'), 'StockCode'])['Quantity'].sum()  
    
    # aggregate monthly sales
    date_item_df = df.loc[df['StockCode'].isin([23084, 84826, 22197, 22086, '85099B'])
    ].set_index('InvoiceDate').groupby([pd.Grouper(freq='M'), 'StockCode'])['Quantity'].sum()
    
    # the pivot table
    trending_itmes_df = date_item_df.reset_index().pivot('InvoiceDate','StockCode').fillna(0)
    trending_itmes_df = trending_itmes_df.reset_index()
    trending_itmes_df = trending_itmes_df.set_index('InvoiceDate')
    trending_itmes_df.columns = trending_itmes_df.columns.droplevel(0)
    
    # the plot
    ax = pd.DataFrame(trending_itmes_df.values).plot(
        figsize=(10,7),
        grid=True,
    )
    ax.set_ylabel('number of purchases')
    ax.set_xlabel('date')
    ax.set_title('Item Trends over Time')
    ax.legend(trending_itmes_df.columns, loc='upper left')
    plt.xticks(
    range(len(trending_itmes_df.index)),
    [x.strftime('%m.%Y') for x in trending_itmes_df.index],
    rotation=45
    )
    
    
if __name__ == "__main__":
    main()