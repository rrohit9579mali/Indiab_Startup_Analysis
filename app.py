import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Load data
st.title('Indian Startup Analysis')
df = pd.read_csv('Startup_Funding_Analysis1.csv')
st.sidebar.title("Indian Startup")
df['date']=pd.to_datetime(df['date'],errors='coerce')
# Clean data
df = df[~df['investors'].str.match(r'^\d')]
df['date'] = df['date'].fillna('2019-01-05')

# Extract unique investors
all_investors = df['investors'].str.split(',').sum()
all_investors = sorted(set(i.strip() for i in all_investors if i.strip()))
# st.set_page_config(page_title='Startup Analysis')
# st.dataframe(df)
# Investor detail loader
def load_investors(investor):
    df['date']=pd.to_datetime(df['date'],errors='coerce')
    st.header(f"Investor Name: {investor}")
    st.subheader('Recent Investments:-')
    recent_investments=df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','investors','amount']]
    st.dataframe(recent_investments)

    #bigest investments
    st.subheader('Bigest Investement :- ')
    bigest_investment=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    st.dataframe(bigest_investment)

    # graphican analysis
    c11, c22 = st.columns(2)
    with c11:
      st.subheader('Bigest investment')
    with c22:
        st.subheader('General Investements')
    c1,c2=st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.bar(bigest_investment.index, bigest_investment.values)
        st.pyplot(fig)
#      general Analysis

    with c2:
       general_nalaysis=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
       fig1,ax1=plt.subplots()
       ax1.pie(general_nalaysis,labels=general_nalaysis.index)
       st.pyplot(fig1)

    # city
    cl1,cl2=st.columns(2)
    with cl1:
     st.subheader('Locations of Compony')
    with cl2:
        st.subheader('year wise Invesment')
    c3,c4=st.columns(2)
    with c3:
        city=df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        fig2,ax2=plt.subplots()
        ax2.pie(city,labels=city.index)
        st.pyplot(fig2)

    with c4:
        df['Year']=df['date'].dt.year
        year_wise_investement=df[df['investors'].str.contains(investor)].groupby('Year')['amount'].sum()
        fig3,ax3=plt.subplots()
        ax3.plot(year_wise_investement.index,year_wise_investement.values)
        st.pyplot(fig3)

    st.subheader('similer invester')
    sequoia_df = df[df['investors'].str.contains(investor, na=False)]

    # Step 2: Group by startup and extract all investors
    startup_investors = sequoia_df.groupby('startup')['investors'].apply(lambda x: ','.join(x)).str.split(',')

    # Step 3: Remove whitespace and deduplicate investor names
    startup_investors = startup_investors.apply(lambda investors: list(set(i.strip() for i in investors if i.strip())))
    similar_investors_df = startup_investors.reset_index().rename(columns={'investors': 'similar_investors'}).head(10)
    st.dataframe(similar_investors_df)


#  overall_Analysis



def load_overall_Analysis(x):
    st.title('Overall_Analysis')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # convert to datetime
    df['Year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Total Invested Amount:-")
    with c2:
         Total_invest_amount=round(df['amount'].sum())
         st.subheader(str(Total_invest_amount)+' CR')
    col1,col2=st.columns(2)
    with col1:
         st.subheader('Maximum Funding :- ')
         x = df.groupby('startup')['amount'].max().sort_values(ascending=False)
         x=x.reset_index()[['startup', 'amount']]
         st.dataframe(x)
    with col2:
        st.subheader("Avarage Funding :- ")
        Avg = df.groupby('startup')['amount'].mean().sort_values(ascending=False)
        AVG=Avg.reset_index()[['startup','amount']]
        st.dataframe(AVG)
    # cl4,cl5=st.columns(2)
    st.header('📈 Month-over-Month (MoM) Funding Graph')

        # Dropdown to select Total amount or Count of deals
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

        # Group data by Year and Month
    if selected_option == 'Total':
            temp_df = df.groupby(['Year', 'month'])['amount'].sum().reset_index()
    else:
            temp_df = df.groupby(['Year', 'month'])['amount'].count().reset_index()

        # Create a combined x-axis label
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['Year'].astype(str)

        # Plotting
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(temp_df['x_axis'], temp_df['amount'], marker='o', color='teal')

        # Add titles and labels
    ax3.set_title(f'{selected_option} of Startup Funding MoM', fontsize=14)
    ax3.set_xlabel('Month-Year', fontsize=12)
    ax3.set_ylabel('Amount (in Cr)' if selected_option == 'Total' else 'Deal Count', fontsize=12)

        # Improve readability
    plt.xticks(rotation=90)
    plt.tight_layout()

        # Show in Streamlit
    st.pyplot(fig3)


# Sidebar Options
option = st.sidebar.selectbox('Select Option', ['Overall analysis', 'Startup', 'Investor'])

if option == 'Overall analysis':
    overall_analysis=st.sidebar.selectbox('Sub-option', ['a', 'b', 'c'])  # Placeholder
    btn=st.sidebar.button('Find Overall Analysis')
    load_overall_Analysis(overall_analysis)
elif option == 'Startup':
    startup_name = st.sidebar.selectbox('Select Startup', sorted(df['startup'].dropna().unique().tolist()))
    btn1 = st.sidebar.button('Find Startup')
    if btn1:
        st.subheader('Startup Analysis')
        st.write(df[df['startup'] == startup_name])
else:
    select_investor = st.sidebar.selectbox('Investor', all_investors)
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investors(select_investor)
