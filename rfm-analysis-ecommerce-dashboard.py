# Data Manipulation Library
import pandas as pd

# Data Visualization Library
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Streamlit Library
import streamlit as st
from streamlit_option_menu import option_menu

# Aesthethical Library
from babel.numbers import format_currency


def main():
    # Set the plot to dark theme
    sns.set(style='dark')

    # Load cleaned data
    main_df = pd.read_csv("main_data.csv")

    datetime_columns = ["order_purchase_timestamp", "order_approved_at"]
    main_df.sort_values(by="order_approved_at", inplace=True)
    main_df.reset_index(inplace=True)

    for column in datetime_columns:
        main_df[column] = pd.to_datetime(main_df[column], format='%Y-%m-%d %H:%M:%S')
        main_df[column] = main_df[column].dt.date
        main_df[column] = pd.to_datetime(main_df[column], format='%Y-%m-%d')

    # Visualization Plot Function

    # Bar Plot Function
    def barplotfunc(x, y, xlabel=str, ylabel=str, title=str):
        fig, ax = plt.subplots(figsize=(14,8))
       
        sns.barplot(x=x, y=y, orient='h')
        ax.set_xlabel(xlabel, fontsize=13)
        ax.set_ylabel(ylabel, fontsize=13)
        ax.bar_label(ax.containers[0], rotation=0, fontsize=13)
        ax.set_title(title, loc="center", fontsize=20)
        ax.tick_params(axis='y', labelsize=13)
        ax.tick_params(axis='x', labelsize=13)

        return fig

    def barplotfunc2(df, min_date_filter, max_date_filter, xlabel=str, ylabel=str, title=str, method=str):
        fig, ax = plt.subplots(figsize=(16,14))

        df_filter= df[
            (df['order_approved_at'] >= pd.to_datetime(min_date_filter)) & (df['order_approved_at'] <= pd.to_datetime(max_date_filter))
        ]

        if(method == 'sum'):
            df_group_filter = df_filter.groupby(by= ['customer_state'])['payment_value'].sum()
        if(method == 'mean'):
            df_group_filter = df_filter.groupby(by= ['customer_state'])['payment_value'].mean()

        df_group_filter = df_group_filter.sort_values(ascending=False)
        
        sns.barplot(x=df_group_filter.index, y=df_group_filter, orient='v')
        ax.set_xlabel(xlabel, fontsize=30)
        ax.set_ylabel(ylabel, fontsize=30)
        ax.bar_label(ax.containers[0], rotation=0, fontsize=20)
        ax.set_title(title, loc="center", fontsize=36)
        ax.tick_params(axis='y', labelsize=27)
        ax.tick_params(axis='x', labelsize=27)

        return fig
        
    # Histogram Plot Function
    def histplotfunc(df, start=None, end=None, xlabel=str, ylabel=str, title=str):
        df_filter = df[(df >= start) & (df <= end)]

        fig, ax = plt.subplots(figsize=(18,8))
        sns.histplot(df_filter)
        ax.set_xlabel(xlabel, fontsize=13)
        ax.set_ylabel(ylabel, fontsize=13)
        ax.set_title(title, loc='center', fontsize=20)
        ax.tick_params(axis='y', labelsize=13)
        ax.tick_params(axis='x', labelsize=13)

        return fig

    # Line Plot Function

    def lineplotfunct1(df, min_date_filter, max_date_filter, xlabel=str, ylabel=str, title=str, freq=str, method=str):
        
        df_filter= df[
            (df['order_approved_at'] >= pd.to_datetime(min_date_filter)) & (df['order_approved_at'] <= pd.to_datetime(max_date_filter))
        ]

        if(method == 'sum'):
            df_group_filter = df_filter.groupby(
                by= pd.Grouper(key='order_approved_at', freq=freq))['payment_value'].sum()
        if(method == 'mean'):
            df_group_filter = df_filter.groupby(
                by= pd.Grouper(key='order_approved_at', freq=freq))['payment_value'].mean()
        if(method == 'count'):
            df_group_filter = df_filter.groupby(
                by= pd.Grouper(key='order_approved_at', freq=freq))['order_approved_at'].count()

        fig, ax= plt.subplots(figsize=(18,8))
        
        sns.lineplot(x= df_group_filter.index, y= df_group_filter, marker='o')
        ax.set_xlabel(xlabel, fontsize=15)
        ax.set_ylabel(ylabel, fontsize=15)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
        ax.set_title(title, loc="center", fontsize=20)
        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=15, rotation=45)

        return fig

    # lineplotfunct_two (this function specific for Customer State Analysis)
    def lineplotfunct2(df, min_date_filter, max_date_filter, hue=str, xlabel=str, ylabel=str, title=str, freq=str, method=str):
        
        df_filter= df[
            (df['order_approved_at'] >= pd.to_datetime(min_date_filter)) & (df['order_approved_at'] <= pd.to_datetime(max_date_filter))
        ]

        if(method == 'sum'):
            df_group_filter = df_filter.groupby(
                by= ['customer_state', pd.Grouper(key='order_approved_at', freq=freq)])['payment_value'].sum()
            df_group_filter =  pd.DataFrame(df_group_filter).reset_index()
        if(method == 'mean'):
            df_group_filter = df_filter.groupby(
                by= ['customer_state', pd.Grouper(key='order_approved_at', freq=freq)])['payment_value'].mean()
        df_group_filter =  pd.DataFrame(df_group_filter).reset_index()
        if(method == 'count'):
            df_group_filter = df_filter.groupby(
                by= ['customer_state', pd.Grouper(key='order_approved_at', freq=freq)])['order_approved_at'].count()
        df_group_filter =  pd.DataFrame(df_group_filter).reset_index()

        
        fig, ax= plt.subplots(figsize=(18,8))
        
        sns.lineplot(x= df_group_filter['order_approved_at'], y= df_group_filter['payment_value'], marker='o', hue=df_group_filter[hue])
        ax.set_xlabel(xlabel, fontsize=15)
        ax.set_ylabel(ylabel, fontsize=15)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
        ax.set_title(title, loc="center", fontsize=20)
        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=15, rotation=45)

        return fig

    # Pie Chart Function
    def donutchartfunc(df, label,title=str):       
        fig, ax = plt.subplots(figsize=(18,13))

        _, _, autotexts = ax.pie(df, labels=label, autopct='%.0f%%', pctdistance=0.9, 
                                textprops={'fontsize': 16}, startangle=230)

        for autotext in autotexts:
            autotext.set_color('white')

        centre_circle = plt.Circle((0,0), 0.7, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        ax.set_title(title, fontsize = 20)

        return fig

    
    # Filter data
    min_date = main_df["order_approved_at"].min()
    max_date = main_df["order_approved_at"].max()

    
    # ======================DASHBOARD===========================================

    # RFM Analysis on Brazilian E-Commerce
    with st.sidebar:
        selected= option_menu(
            menu_title="Main menu",
            options= ['Introduction', 'RFM Analysis', 'Exploratory Data Analysis']
    )
    
    if selected == 'Introduction':
        row0_space1, row0_1, row0_space2 = st.columns(
        (0.1, 3.5, 0.1)
    )
        row0_1.title("RFM Analysis on Brazilian E-Commerce Dashboard")

        row1_space1, row1_1, row1_space2 = st.columns((0.1, 3.5, 0.1))

        with row1_1:
            st.header(f'{selected}')
            st.markdown(
                '<div style="text-align: justify;">Brazilian e-commerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. You can choose what to see in the menu on the sidebar. Feel free to explore!</div>', unsafe_allow_html=True)
            
            st.markdown(
                """
                \n
                \n
                \n
                """
            )

        row2_space1, row2_1, row2_space2 = st.columns((0.1, 3.5, 0.1))

        with row2_1:
            st.markdown(
                '<div style="text-align: justify;">You can see the snippet of dataset used in this analysis below in the table.</div>', unsafe_allow_html=True)
            st.markdown("***")
            
            st.dataframe(data=main_df, width=1000, height=200)


        row2_space1, row2_1, row2_space2 = st.columns((0.1, 3.5, 0.1))

        with row2_1:
            st.write("")
            st.markdown("***")
            st.markdown(
                """
                Thank you for visiting my dashboard. If you have any further discussion or suggestion you can reach me on:\n
                E-mail      : yafie345@gmail.com \n
                LinkedIn    : [Haris Yafie]('https://www.linkedin.com/in/haris-yafie/')
                """
            )
            st.caption('Copyright © Haris Yafie 2023')
  
    if selected == 'RFM Analysis':

        # Create RFM Dataset
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
        
        with st.sidebar:
            st.subheader("Filter Data By Date")
            # Take the start_date & end_date from date_input
            start_date, end_date = st.date_input(
                label='Time Span',
                min_value=min_date,
                max_value=max_date,
                value=[min_date, max_date]
                )
        main_df = main_df[(main_df["order_approved_at"] >= str(start_date)) &
                (main_df["order_approved_at"] <= str(end_date))]
        
        # Creating RFM dataframe
        rfm_df = create_rfm_df(main_df)

        row3_space1, row3_1, row3_space2 = st.columns((0.1, 3.5, 0.1))

        with row3_1:
            st.header(f'{selected}')
            st.markdown(
                """
                Here you can explore the dataset by looking at Recency, Frequency, and Monetary. Go check it out!
                """
            )
            # Best Customer Based on RFM Parameters
            st.subheader("Best Customer Based on RFM Parameters")

        row4_space1, row4_1, row4_space2 = st.columns((0.1, 2.5, 0.1))

        tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

        # Slider Function
        def myslider(FilterData):
                start, end = st.select_slider(
                    'Filter Your Data',
                    options=range(int(FilterData.min()), int(FilterData.max()) + 1),
                    value=(int(FilterData.min()), int(FilterData.max()))
                )
                st.write('You selected values between', start, 'and', end)
                return start, end

        with row4_1:

            with tab1:
                avg_recency = round(rfm_df["recency"].mean(), 1)
                st.metric("Average Recency (days)", value=avg_recency)

                tab_row1_space1, tab_row1_1, tab_row1_space2 = st.columns((0.1, 0.7, 0.1))

                with tab_row1_1:
                    st.pyplot(histplotfunc(rfm_df['recency'], start=rfm_df['recency'].min(), end=rfm_df['recency'].max(), 
                                        xlabel='Days', ylabel='Total Customer', title='Histogram of Recency by Customer'), use_container_width=True)
                    
                    recency_rank = rfm_df.sort_values(by="recency", ascending=True).head(5)

                    st.markdown("#")
                    st.markdown("Below is a bar plot to see the top customer IDs")

                    st.pyplot(barplotfunc(
                        x=recency_rank['recency'], y=recency_rank['customer_id'], xlabel='Days', ylabel="customer_id", title="By Recency (days)"
                    ), use_container_width=True)  

                    st.markdown("#")           
                            
            with tab2:
                avg_frequency = round(rfm_df.frequency.mean(), 2)
                st.metric("Average Frequency", value=avg_frequency)

                tab_row2_space1, tab_row2_1, tab_row2_space2 = st.columns((0.1, 0.7, 0.1))

                with tab_row2_1:
                    st.markdown("Due to the sparse distribution of data, you have the option to filter it by selecting your preferred value using the slider located below.")
                    start, end = myslider(rfm_df['frequency'])
                    st.pyplot(histplotfunc(rfm_df['frequency'], start=start, end=end, 
                                        xlabel='Frequency', ylabel='Total Customer', title='Histogram of Frequency by Customer'), use_container_width=True)
                    
                    st.markdown("#")
                    st.markdown("Below is a bar plot to see the top customer IDs")

                    frequency_rank = rfm_df.sort_values(by="frequency", ascending=False).head(5)
        
                    st.pyplot(barplotfunc(x=frequency_rank['frequency'], y=frequency_rank['customer_id'], 
                                          xlabel='Frequency', ylabel="customer_id", title="By Frequency"), use_container_width=True)

                    st.markdown("#")
        
            with tab3:
                avg_monetary = format_currency(rfm_df.monetary.mean(), 'BRL', locale='pt_BR')
                st.metric("Average Monetary", value=avg_monetary)

                tab_row3_space1, tab_row3_1, tab_row3_space2 = st.columns((0.1, 0.7, 0.1))

                with tab_row3_1:
                    st.markdown("Due to the sparse distribution of data, you have the option to filter it by selecting your preferred value using the slider located below.")
                    start, end = myslider(rfm_df['monetary'])
                    st.pyplot(histplotfunc(rfm_df['monetary'], start=start, end=end, 
                                        xlabel='Monetary', ylabel='Total Customer', title='Histogram of Monetary by Customer'), use_container_width=True)
                    
                    st.markdown("#")
                    st.markdown("Below is a bar plot to see the top customer IDs")
                    
                    monetary_rank = rfm_df.sort_values(by="monetary", ascending=False).head(5)
        
                    st.pyplot(barplotfunc(
                        x=monetary_rank['monetary'], y=monetary_rank['customer_id'], xlabel='Monetary', ylabel="customer_id", title="By Monetary"
                    ), use_container_width=True)

                    st.markdown("#")
                    
                    

        row5_space1, row5_1, row5_space2 = st.columns((0.1, 3.5, 0.1))

        with row5_1:
            st.markdown(
                '<div style="text-align: justify;">You can see the snippet of RFM dataframe used in this analysis below in the table.</div>', unsafe_allow_html=True)
                        
            st.dataframe(data=rfm_df, width=1000, height=200)

            st.markdown("#")

            st.caption('Copyright © Haris Yafie 2023')
                  


    # Exploratory Data Analysis

    if selected == 'Exploratory Data Analysis':

        with st.sidebar:
            st.subheader("Filter Data By Date")
            # Take the start_date & end_date from date_input
            start_date, end_date = st.date_input(
                label='Time Span',
                min_value=min_date,
                max_value=max_date,
                value=[min_date, max_date]
                )
            
            st.subheader("Select Time Interval")
            select_freq= st.selectbox(
            "Choose Freq (1 Quartile - 1 Day)",
            options= ['1Q', '1M', '1W', '1D']
            )

        main_df = main_df[(main_df["order_approved_at"] >= str(start_date)) &
                (main_df["order_approved_at"] <= str(end_date))]

        row6_space1, row6_1, row6_space2 = st.columns((0.1, 3.5, 0.1))

        with row6_1:
            st.header(f'{selected}')
            st.markdown(
                """
                Next is to explore other interesting variable that may give us more insight about this dataset!
                """
            )       

        # trend analysis
        row7_space1, row7_1, row7_space2 = st.columns((0.1, 3.5, 0.1))

        with row7_1:
            st.subheader('Transaction Value Trend')
            st.markdown(
                """
                Examining transaction values provides valuable insights into the overall trend when combining data from all states. Additionally, you have the flexibility to customize the time intervals, including quartiles, monthly, weekly, and daily, easily adjustable through the sidebar menu.
                """
            )
       
        row8_space1, row8_1, row8_space2 = st.columns(
            (0.1, 3.5, 0.1)
        )

        with row8_1:

            st.pyplot(lineplotfunct1(main_df, start_date, end_date, xlabel='Dates', ylabel='Transaction Value', title='Total Transaction Trend', 
                                     freq=select_freq, method='sum'), 
                                     use_container_width=True)
        
        row9_space1, row9_1, row9_space2 = st.columns((0.1, 3.5, 0.1))
        
        with row9_1:
            st.pyplot(lineplotfunct1(main_df, start_date, end_date, xlabel='Dates', ylabel='Transaction Value', title='Average Transaction Trend', 
                                     freq=select_freq, method='mean'), 
                                     use_container_width=True)

        # state analysis  
        row10_space1, row10_1, row10_space2 = st.columns((0.1, 3.5, 0.1))        

        with row10_1:
            st.subheader('State Analysis')
            st.markdown(
                """
                In this section, the visualization is based on the state(s) of your choice. To initiate the visualization, please select at least one state initially. Any error encountered is simply a prompt for your input, ensuring you receive insights into all states you wish to explore.
                """
            )
            
            state= st.multiselect(
                'Select Customer State',
                options= main_df['customer_state'].unique(),
            )

            Selection_state= main_df.query(
                "customer_state == @state"
            )

        row11_space1, row11_1, row11_space2 = st.columns((0.1, 3.5, 0.1))

        with row11_1:
            st.write("")
            st.markdown("Bar Plot to see the total order made by customer per state(s)")   
            st.pyplot(barplotfunc(
                        x=Selection_state['customer_state'].value_counts(), y=Selection_state['customer_state'].value_counts().index, xlabel='Total Order', ylabel='State', title='Total Order by State'
                    ), use_container_width=True)
            st.write("")
            st.markdown("Bar Plot to see the total transaction value and average transaction value in state(s), you can compare between states in this plot.")


        row12_space1, row12_1, row12_3, row12_2, row12_space3 = st.columns(
            (0.1, 1.7, 0.1, 1.7, 0.1)
        )

        with row12_1:
            st.pyplot(barplotfunc2(df=Selection_state, min_date_filter=start_date, max_date_filter=end_date, xlabel='Transaction Value', ylabel='State', title='Total Transaction Value by State', method='sum'), use_container_width=True)
            
        with row12_2:
            st.pyplot(barplotfunc2(df=Selection_state, min_date_filter=start_date, max_date_filter=end_date, xlabel='Transaction Value', ylabel='State', title='Average Transaction Value by State', method='mean'), use_container_width=True)
                    

        row13_space1, row13_1, row13_space2 = st.columns((0.1, 3.5, 0.1))
        with row13_1:
            st.write("")
            st.markdown("Line Plot to see the total transaction value by designed time interval, you also can compare between states with this plot.")
            st.pyplot(lineplotfunct2(Selection_state, start_date, end_date, hue='customer_state', xlabel='Dates', ylabel='Transaction Value', title='Total Transaction Value By States', 
                                     freq=select_freq, method='sum'), 
                                     use_container_width=True)
            st.write("")
        
        row14_space1, row14_1, row14_space2 = st.columns((0.1, 3.5, 0.1))

        with row14_1:
            st.markdown('**Percentage of Payment Types**')
            st.markdown(
                """
                There are several payment types that had been used by customer presented in percentage with donut chart below.
                """
            )

        row15_space1, row15_1, row15_space2 = st.columns((0.1, 0.3, 0.1))

        with row15_1:
            # Your data
            payment_counts = Selection_state['payment_type'].value_counts()

            label = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']

            st.pyplot(donutchartfunc(payment_counts, label=label, title='Donut Chart of Payment Types'), use_container_width=True)

        st.caption('Copyright © Haris Yafie 2023')

        



if __name__ == "__main__":
    main()

