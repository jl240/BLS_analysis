import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df0 = pd.read_excel('all_data_M_2024.xlsx', sheet_name='filtered')

# region df

df = df0[['OCC_TITLE', 'TOT_EMP', 'A_MEAN', 'A_PCT10', 'A_PCT25', 'A_MEDIAN', 'A_PCT75', 'A_PCT90', 'H_MEAN', 'H_PCT10', 'H_PCT25',	'H_MEDIAN',	'H_PCT75', 'H_PCT90']]
df.columns = ['Occupation', 'Estimated Total Employment', 'Mean Annual Wage', '10th Percentile Annual Wage', '25th Percentile Annual Wage', 'Median Annual Wage', '75th Percentile Annual Wage', '90th Percentile Annual Wage', 'Mean Hourly Wage', '10th Percentile Hourly Wage', '25th Percentile Hourly Wage', 'Median Hourly Wage', '75th Percentile Hourly Wage', '90th Percentile Hourly Wage']
df = df.replace('*', np.nan)
df['Mean Annual Wage'] = df['Mean Annual Wage'].replace('#', 239220)
df['10th Percentile Annual Wage'] = df['10th Percentile Annual Wage'].replace('#', 239220)
df['25th Percentile Annual Wage'] = df['25th Percentile Annual Wage'].replace('#', 239220)
df['Median Annual Wage'] = df['Median Annual Wage'].replace('#', 239220)
df['75th Percentile Annual Wage'] = df['75th Percentile Annual Wage'].replace('#', 239220)
df['90th Percentile Annual Wage'] = df['90th Percentile Annual Wage'].replace('#', 239220)
df['Mean Hourly Wage'] = df['Mean Hourly Wage'].replace('#', 115)
df['10th Percentile Hourly Wage'] = df['10th Percentile Hourly Wage'].replace('#', 115)
df['25th Percentile Hourly Wage'] = df['25th Percentile Hourly Wage'].replace('#', 115)
df['Median Hourly Wage'] = df['Median Hourly Wage'].replace('#', 115)
df['75th Percentile Hourly Wage'] = df['75th Percentile Hourly Wage'].replace('#', 115)
df['90th Percentile Hourly Wage'] = df['90th Percentile Hourly Wage'].replace('#', 115)

# endregion

# region df2
df2 = df0[['OCC_TITLE', 'TOT_EMP', 'A_MEAN', 'A_MEDIAN', 'H_MEAN', 'H_MEDIAN']]
df2.columns = ['Occupation', 'Estimated Total Employment', 'Mean Annual Wage', 'Median Annual Wage', 'Mean Hourly Wage', 'Median Hourly Wage']
df2 = df2.replace('*', np.nan)
df2['Mean Annual Wage'] = df2['Mean Annual Wage'].replace('#', 239220)
df2['Median Annual Wage'] = df2['Median Annual Wage'].replace('#', 239220)
df2['Mean Hourly Wage'] = df2['Mean Hourly Wage'].replace('#', 115)
df2['Median Hourly Wage'] = df2['Median Hourly Wage'].replace('#', 115)
df2 = df2.sort_values('Occupation')
# endregion

st.set_page_config(layout="wide")
st.title('U.S. Bureau of Labor Statistics 2024 Data')
tab1, tab2, tab3, tab4 = st.tabs(['Table', 'Summary', 'Search', 'Filter'])

with st.sidebar:
    st.title('Notes About the Data')
    st.markdown("""
                - The data is from the [U.S. Bureau of Labor Statistics website](https://www.bls.gov/oes/). Occupational Employment and Wage Statistics are made available for public use every year.
                - The data has been filtered to look at SOC-detailed-level occupations across all of the United States.
                - **Occupation titles** use Standard Occupational Classification (SOC) titles or OEWS-specific titles.
                - **Estimated total employment** rounded to the nearest 10 (excludes self-employed).
                - An **median annual wage** greater than $239,220 is just shown as 239,220.
                - An **hourly wage** greater than $115 is just shown as 115.
                """)


with tab1:
    st.dataframe(df2, height=500, use_container_width=True)


with tab2:
    st.markdown("""
                <div style='text-align: center; font-size: 24px;'>
                Top 10 Highest Paid Occupations
                </div>
                <br>
                """,
                unsafe_allow_html=True)

    st.dataframe(df2.sort_values('Mean Annual Wage', ascending=False).iloc[0:10,0:4], use_container_width=True)

    st.markdown("""
                <div style='text-align: center; font-size: 24px;'>
                Top 10 Highest Total Employed Occupations
                </div>
                <br>
                """,
                unsafe_allow_html=True)

    st.dataframe(df2.sort_values('Estimated Total Employment', ascending=False).iloc[0:10,0:4], use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        fig, ax = plt.subplots()
        ax.hist(df2['Mean Annual Wage'], bins=40)
        ax.set_xlim(0, 500000)
        ax.set_title("Mean Annual Wages")
        ax.set_xlabel("Mean Annual Wage")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        x = df2['Estimated Total Employment']
        y = df2['Mean Annual Wage']
        fig, ax = plt.subplots()
        ax.scatter(x, y, marker='o', edgecolor='blue', facecolor='none', s=25)
        ax.set_title("Relationship between Employment and Mean Wage")
        ax.set_xlabel("Estimated Total Employment (in millions)")
        ax.set_ylabel("Mean Annual Wage")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.hist(df2['Median Annual Wage'], bins=20)
        ax.set_xlim(0, 500000)
        ax.set_title("Median Annual Wages")
        ax.set_xlabel("Median Annual Wage")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        x = df2['Estimated Total Employment']
        y = df2['Median Annual Wage']
        fig, ax = plt.subplots()
        ax.scatter(x, y, marker='o', edgecolor='blue', facecolor='none', s=25)
        ax.set_title("Relationship between Employment and Median Wage")
        ax.set_xlabel("Estimated Total Employment (in millions)")
        ax.set_ylabel("Median Annual Wage")
        st.pyplot(fig)
    

with tab3:
    options = df2['Occupation']

    option = st.selectbox("Select an occupation", options)

    display_df0 = df[df['Occupation'] == option]

    display_df = pd.DataFrame(np.nan, index=range(6), columns=['Statistic', 'Annual Wage', 'Hourly Wage'])
    display_df.loc[0, 'Statistic'] = 'Mean'
    display_df.loc[1, 'Statistic'] = '10th Percentile'
    display_df.loc[2, 'Statistic'] = '25th Percentile'
    display_df.loc[3, 'Statistic'] = 'Median'
    display_df.loc[4, 'Statistic'] = '75th Percentile'
    display_df.loc[5, 'Statistic'] = '90th Percentile'
    display_df.loc[0, 'Annual Wage'] = display_df0['Mean Annual Wage'].iloc[0]
    display_df.loc[1, 'Annual Wage'] = display_df0['10th Percentile Annual Wage'].iloc[0]
    display_df.loc[2, 'Annual Wage'] = display_df0['25th Percentile Annual Wage'].iloc[0]
    display_df.loc[3, 'Annual Wage'] = display_df0['Median Annual Wage'].iloc[0]
    display_df.loc[4, 'Annual Wage'] = display_df0['75th Percentile Annual Wage'].iloc[0]
    display_df.loc[5, 'Annual Wage'] = display_df0['90th Percentile Annual Wage'].iloc[0]
    display_df.loc[0, 'Hourly Wage'] = display_df0['Mean Hourly Wage'].iloc[0]
    display_df.loc[1, 'Hourly Wage'] = display_df0['10th Percentile Hourly Wage'].iloc[0]
    display_df.loc[2, 'Hourly Wage'] = display_df0['25th Percentile Hourly Wage'].iloc[0]
    display_df.loc[3, 'Hourly Wage'] = display_df0['Median Hourly Wage'].iloc[0]
    display_df.loc[4, 'Hourly Wage'] = display_df0['75th Percentile Hourly Wage'].iloc[0]
    display_df.loc[5, 'Hourly Wage'] = display_df0['90th Percentile Hourly Wage'].iloc[0]

    st.write(f'Estimated Total Employment: {display_df0['Estimated Total Employment'].iloc[0]:,}')

    st.dataframe(display_df)


with tab4:
    # region mean annual wage
    st.markdown("""
                <div style='font-size: 20px;'>
                Select a range for mean annual wage
                </div>
                """,
                unsafe_allow_html=True)
    
    range1 = st.slider('', 
                      df2['Mean Annual Wage'].min(), 
                      df2['Mean Annual Wage'].max(), 
                      value=(df2['Mean Annual Wage'].min(), df2['Mean Annual Wage'].max()))

    col1, col2 = st.columns(2)
    with col1:
        min1 = float(st.text_input("Min", value=range1[0]))
    with col2:
        max1 = float(st.text_input("Max", value=range1[1]))

    if min1 > max1:
        st.markdown("""
                <div style='text-align: center; font-size: 24px;'>
                Please enter a valid range
                </div>
                """,
                unsafe_allow_html=True)
    
    df3 = df2[(min1 <= df2['Mean Annual Wage']) & (df2['Mean Annual Wage'] <= max1)]
    st.dataframe(df3, use_container_width=True)
    # endregion

    st.markdown("---")

    # region median annual wage
    st.markdown("""
                <div style='font-size: 20px;'>
                Select a range for median annual wage
                </div>
                """,
                unsafe_allow_html=True)

    range2 = st.slider('', 
                      df2['Median Annual Wage'].min(), 
                      df2['Median Annual Wage'].max(), 
                      value=(df2['Median Annual Wage'].min(), df2['Median Annual Wage'].max()))
    
    col1, col2 = st.columns(2)
    with col1:
        min2 = float(st.text_input("Min", value=range2[0]))
    with col2:
        max2 = float(st.text_input("Max", value=range2[1]))

    if min2 > max2:
        st.markdown("""
                <div style='text-align: center; font-size: 24px;'>
                Please enter a valid range
                </div>
                """,
                unsafe_allow_html=True)
    
    df3 = df2[(min2 <= df2['Median Annual Wage']) & (df2['Median Annual Wage'] <= max2)]
    st.dataframe(df3, use_container_width=True)
    # endregion

    st.markdown("---")

    # region estimated total employment
    st.markdown("""
                <div style='font-size: 20px;'>
                Select a range for estimated total employment
                </div>
                """,
                unsafe_allow_html=True)

    range3 = st.slider('', 
                      df2['Estimated Total Employment'].min(), 
                      df2['Estimated Total Employment'].max(), 
                      value=(df2['Estimated Total Employment'].min(), df2['Estimated Total Employment'].max()))
    
    col1, col2 = st.columns(2)
    with col1:
        min3 = float(st.text_input("Min", value=range3[0]))
    with col2:
        max3 = float(st.text_input("Max", value=range3[1]))

    if min3 > max3:
        st.markdown("""
                <div style='text-align: center; font-size: 24px;'>
                Please enter a valid range
                </div>
                """,
                unsafe_allow_html=True)
    
    df3 = df2[(min3 <= df2['Estimated Total Employment']) & (df2['Estimated Total Employment'] <= max3)]
    st.dataframe(df3, use_container_width=True)
    # endregion
