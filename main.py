import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    pages = ['Home', 'Conversion']

    option = st.sidebar.selectbox('Data Science for Marketing', options=pages)

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
        st.dataframe(data)
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



# @st.cache
def load_data():
    df = pd.read_csv("./data/bank-additional-full.csv", sep=';')
    df['conversion'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)
    return df
    
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



if __name__ == "__main__":
    main()