import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency
sns.set(style='dark')


def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
    "order_approved_at": "max", # latest order date
    "order_id": "count", # order count
    "payment_value": "sum" # total revenue sum
    })
    rfm_df.columns = ["customer_id", "max_order_approved_at", "frequency", "monetary"]

    # determine when customer last order date in days
    rfm_df["max_order_approved_at"] = rfm_df["max_order_approved_at"].dt.date
    recent_date = df["order_approved_at"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_approved_at"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_approved_at", axis=1, inplace=True)

    return rfm_df

# Load cleaned data
main_df = pd.read_csv("main_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at"]
main_df.sort_values(by="order_approved_at", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column], format='%Y-%m-%d %H:%M:%S')
    main_df[column] = main_df[column].dt.date
    main_df[column] = pd.to_datetime(main_df[column], format='%Y-%m-%d')


# Filter data
min_date = main_df["order_approved_at"].min()
max_date = main_df["order_approved_at"].max()

with st.sidebar:
    st.subheader("Filter Data By Date")
    # Take the start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_df[(main_df["order_approved_at"] >= str(start_date)) &
                (main_df["order_approved_at"] <= str(end_date))]

# Creating RFM dataframe
rfm_df = create_rfm_df(main_df)


# ======================DASHBOARD===========================================

# RFM Analysis on Brazilian E-Commerce
row0_space1, row0_1, row0_space2 = st.columns(
    (0.1, 3.5, 0.1)
)

row0_1.title("Brazilian E-Commerce RFM Analysis Dashboard")


row1_space1, row1_1, row1_space2 = st.columns((0.1, 3.5, 0.1))

with row1_1:
    st.markdown(
        """
        Brazilian e-commerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. Below are the dashboard of Recency, Frequency, and Monetary that can be filter by dates using sidebar on the left side. 
        Feel free to explore!
        """
    )
    # Best Customer Based on RFM Parameters
    st.subheader("Best Customer Based on RFM Parameters")

row2_space1, row2_1, row2_space2 = st.columns((0.1, 2.5, 0.1))

tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

with row2_1:

    with tab1:
        avg_recency = round(rfm_df["recency"].mean(), 1)
        st.metric("Average Recency (days)", value=avg_recency)

        tab_row1_space1, tab_row1_1, tab_row1_space2 = st.columns((0.1, 0.7, 0.1))

        with tab_row1_1:         
            fig1, ax1 = plt.subplots(figsize=(15, 10))
            sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), orient='h')
            ax1.set_xlabel('Days', fontsize=11)
            ax1.set_ylabel("customer_id", fontsize=11)
            ax1.bar_label(ax1.containers[0], rotation=0, fontsize=11)
            ax1.set_title("By Recency (days)", loc="center", fontsize=20)
            ax1.tick_params(axis='y', labelsize=11)
            ax1.tick_params(axis='x', labelsize=11)
    
            st.pyplot(fig1, use_container_width=True)

 
    with tab2:
        avg_frequency = round(rfm_df.frequency.mean(), 2)
        st.metric("Average Frequency", value=avg_frequency)

        tab_row2_space1, tab_row2_1, tab_row2_space2 = st.columns((0.1, 0.7, 0.1))

        with tab_row2_1:

            fig2, ax2 = plt.subplots(figsize=(15, 10))

            sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), orient='h')
            ax2.set_xlabel('Frequency', fontsize=11)
            ax2.set_ylabel("customer_id", fontsize=11)
            ax2.bar_label(ax2.containers[0], rotation=0, fontsize=11)
            ax2.set_title("By Frequency", loc="center", fontsize=20)
            ax2.tick_params(axis='y', labelsize=11)
            ax2.tick_params(axis='x', labelsize=11)
    
            st.pyplot(fig2, use_container_width=True)

 
    with tab3:
        avg_monetary = format_currency(rfm_df.monetary.mean(), 'BRL', locale='pt_BR')
        st.metric("Average Monetary", value=avg_monetary)

        tab_row3_space1, tab_row3_1, tab_row3_space2 = st.columns((0.1, 0.7, 0.1))

        with tab_row3_1:

            fig3, ax3 = plt.subplots(figsize=(15, 10))

            sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), orient='h')
            ax3.set_xlabel('Transaction Value', fontsize=11)
            ax3.set_ylabel("customer_id", fontsize=11)
            ax3.bar_label(ax3.containers[0], rotation=0, fontsize=11)
            ax3.set_title("By Monetary", loc="center", fontsize=20)
            ax3.tick_params(axis='y', labelsize=11)
            ax3.tick_params(axis='x', labelsize=11)
    
            st.pyplot(fig3, use_container_width=True)


# Exploratory Data Analysis

row3_space1, row3_1, row3_space2 = st.columns((0.1, 3.5, 0.1))

with row3_1:
    st.subheader('Exploratory Data Analysis')
    st.markdown(
        """
        Next is to explore other interesting variable that may give more insight about this dataset!
        """
    )
    # Best Customer Based on RFM Parameters

row4_space1, row4_1, row4_space2 = st.columns((0.1, 3.5, 0.1))

with row4_1:
    st.subheader('Histogram Recency')
    st.markdown(
        """
        To know the distribution of days that customer last order in the e-commerce.
        """
    )

row5_space1, row5_1, row5_space2 = st.columns((0.1, 0.8, 0.1))

with row5_1:
    
    # Recency for histogram
    recent_date = main_df["order_approved_at"].dt.date.max()
    main_df["recency"] = main_df["order_approved_at"].apply(lambda x: (recent_date - x.date()).days)

    fig4, ax4 = plt.subplots(figsize=(20,15))
    sns.histplot(main_df["recency"])
    ax4.set_xlabel('Days', fontsize=15)
    ax4.set_ylabel('Total Customer', fontsize=15)
    ax4.set_title('Histogram of Recency by Customer', loc='center', fontsize=25)
    ax4.tick_params(axis='y', labelsize=15)
    ax4.tick_params(axis='x', labelsize=15)
    st.pyplot(fig4)

row6_space1, row6_1, row6_space2 = st.columns((0.1, 3.5, 0.1))

with row6_1:
    st.subheader('Total Order by State')
    st.markdown(
        """
        We can also to know the total order in every state.
        """
    )


row7_space1, row7_1, row7_space2 = st.columns((0.1, 0.8, 0.1))

with row7_1:
    
    fig5, ax5 = plt.subplots(figsize=(20,15))
    sns.barplot(y= main_df['customer_state'].value_counts().index, x= main_df['customer_state'].value_counts(), orient='h')
    ax5.set_xlabel('Total Order', fontsize=15)
    ax5.set_ylabel("State", fontsize=15)
    ax5.bar_label(ax5.containers[0], rotation=0, fontsize=15)
    ax5.set_title("Bar Chart by State", loc="center", fontsize=25)
    ax5.tick_params(axis='y', labelsize=15)
    ax5.tick_params(axis='x', labelsize=15)
    st.pyplot(fig5)


row8_space1, row8_1, row8_space2 = st.columns((0.1, 3.5, 0.1))

with row8_1:
    st.subheader('Transaction Value')
    st.markdown(
        """
        Transaction value is interesting to look at, we can know total transaction value and average transaction value by states and months.
        """
    )
    st.markdown('By State')

# transaction value

## state sum
state_payment = main_df['payment_value'].groupby(main_df['customer_state']).sum()
state_payment.sort_values(ascending=False)

## state avg
state_avg_payment = main_df['payment_value'].groupby(main_df['customer_state']).mean()
state_avg_payment.sort_values(ascending=False)

## month sum

# Create a new DataFrame with the month column
main_df['month'] = main_df['order_approved_at'].dt.strftime('%Y-%m')  # Extract the month and year as 'YYYY-MM' format

# Count the number of items per month
sum_per_month = main_df.groupby('month')['payment_value'].sum()

## month avg
# Count the number of items per month
avg_per_month = main_df.groupby('month')['payment_value'].mean()


row9_space1, row9_1, row9_space2, row9_2, row9_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row9_1:
    fig6, ax6 = plt.subplots(figsize=(40, 25))
    sns.barplot(y= state_payment.sort_values(ascending=False).index, x= state_payment.sort_values(ascending=False), orient='h')
    ax6.set_xlabel('Transaction Value', fontsize=30)
    ax6.set_ylabel("State", fontsize=30)
    ax6.bar_label(ax6.containers[0], rotation=0, fontsize=30)
    ax6.set_title("Total Transaction Value per State", loc="center", fontsize=50)
    ax6.tick_params(axis='y', labelsize=30)
    ax6.tick_params(axis='x', labelsize=30)
    st.pyplot(fig6)

with row9_2:
    fig7, ax7 = plt.subplots(figsize=(40, 25))
    sns.barplot(y= state_avg_payment.sort_values(ascending=False).index, x= state_avg_payment.sort_values(ascending=False), orient='h')
    ax7.set_xlabel('Transaction Value', fontsize=30)
    ax7.set_ylabel("State", fontsize=30)
    ax7.bar_label(ax7.containers[0], rotation=0, fontsize=30)
    ax7.set_title("Average Transaction Value per State", loc="center", fontsize=50)
    ax7.tick_params(axis='y', labelsize=30)
    ax7.tick_params(axis='x', labelsize=30)
    st.pyplot(fig7)


row10_space1, row10_1, row10_space2 = st.columns((0.1, 3.5, 0.1))

with row10_1:
    st.markdown('By Month')

row11_space1, row11_1, row11_space2, row11_2, row11_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row11_1:
    fig8, ax8 = plt.subplots(figsize=(40,25))
    sns.lineplot(x= sum_per_month.index, y= sum_per_month, marker='o')
    ax8.set_xlabel('Months', fontsize=30)
    ax8.set_ylabel("Transaction Value", fontsize=30)
    ax8.set_title("Total Transaction Per Months", loc="center", fontsize=50)
    ax8.tick_params(axis='y', labelsize=30)
    ax8.tick_params(axis='x', labelsize=30, rotation=45)
    for i, txt in enumerate(sum_per_month):
        plt.text(sum_per_month.index[i], y=txt+40000, s = f'{txt:.2f}'.format(txt), ha='center', va='top',  fontsize=25)
    
    st.pyplot(fig8)
with row11_2:
    fig9, ax9 = plt.subplots(figsize=(40,25))
    sns.lineplot(x= avg_per_month.index, y= avg_per_month, marker='o')
    ax9.set_xlabel('Months', fontsize=30)
    ax9.set_ylabel("Transaction Value", fontsize=30)
    ax9.set_title("Average Transaction Per Months", loc="center", fontsize=50)
    ax9.tick_params(axis='y', labelsize=30)
    ax9.tick_params(axis='x', labelsize=30, rotation=45)
    for i, txt in enumerate(avg_per_month):
        plt.text(avg_per_month.index[i], y=txt+2, s = f'{txt:.2f}'.format(txt), ha='center', va='top',  fontsize=25)

    st.pyplot(fig9)

row12_space1, row12_1, row12_space2 = st.columns((0.1, 3.5, 0.1))

with row12_1:
    st.subheader('Percentage of Payment Types')
    st.markdown(
        """
        There are several payment types that had been used by customer presented in percentage with donut chart below.
        """
    )

row13_space1, row13_1, row13_space2 = st.columns((0.1, 0.3, 0.1))

with row13_1:
    # Your data
    payment_counts = main_df['payment_type'].value_counts()

    label = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']

    
    fig10, ax10 = plt.subplots(figsize=(18,13))

    _, _, autotexts = ax10.pie(payment_counts, labels=label, autopct='%.0f%%', pctdistance=0.9, 
                               textprops={'fontsize': 16}, startangle=230)

    for autotext in autotexts:
        autotext.set_color('white')

    centre_circle = plt.Circle((0,0), 0.7, fc='white')
    fig10 = plt.gcf()
    fig10.gca().add_artist(centre_circle)
    ax10.set_title('Donut Chart of Payment Types', fontsize = 20)

    st.pyplot(fig10)


st.markdown(
        """
        \n
        \n
        \n
        """
    )


row14_space1, row14_1, row14_space2 = st.columns((0.1, 3.5, 0.1))

with row14_1:
    st.write("")
    st.markdown("***")
    st.markdown(
        """
        Thank you for visiting and exploring my dashboard. If you have any further discussion or suggestion you can reach me on:\n
        E-mail      : yafie345@gmail.com \n
        LinkedIn    : [Haris Yafie]('https://www.linkedin.com/in/haris-yafie/')
        """
    )
    st.caption('Copyright © Haris Yafie 2023')



