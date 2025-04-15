import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MaxNLocator

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
tab1, tab2, tab3, tab4 = st.tabs(['Table', 'Summary', 'Search & Compare', 'Filter'])

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
    n = st.slider('Select the number of occupations to compare', min_value=1, max_value=10)

    options = df2['Occupation']

    result = []

    if n > 0:
        option0 = st.selectbox("Select an occupation", options, key=0)
        job0 = df[df['Occupation'] == option0].squeeze()
        result.append(job0)
    if n > 1:
        option1 = st.selectbox("Select an occupation", options, key=1)
        job1 = df[df['Occupation'] == option1].squeeze()
        result.append(job1)
    if n > 2:
        option2 = st.selectbox("Select an occupation", options, key=2)
        job2 = df[df['Occupation'] == option2].squeeze()
        result.append(job2)
    if n > 3:
        option3 = st.selectbox("Select an occupation", options, key=3)
        job3 = df[df['Occupation'] == option3].squeeze()
        result.append(job3)
    if n > 4:
        option4 = st.selectbox("Select an occupation", options, key=4)
        job4 = df[df['Occupation'] == option4].squeeze()
        result.append(job4)
    if n > 5:
        option5 = st.selectbox("Select an occupation", options, key=5)
        job5 = df[df['Occupation'] == option5].squeeze()
        result.append(job5)

    if n > 6:
        option6 = st.selectbox("Select an occupation", options, key=6)
        job6 = df[df['Occupation'] == option6].squeeze()
        result.append(job6)

    if n > 7:
        option7 = st.selectbox("Select an occupation", options, key=7)
        job7 = df[df['Occupation'] == option7].squeeze()
        result.append(job7)

    if n > 8:
        option8 = st.selectbox("Select an occupation", options, key=8)
        job8 = df[df['Occupation'] == option8].squeeze()
        result.append(job8)

    if n > 9:
        option9 = st.selectbox("Select an occupation", options, key=9)
        job9 = df[df['Occupation'] == option9].squeeze()
        result.append(job9)

    testdf = pd.DataFrame(result)

    display = testdf.reset_index(drop=True).T.iloc[0:8]

    def try_convert_to_float(x):
        try:
            return float(x)
        except (ValueError, TypeError):
            return x

    # Example usage
    display = display.applymap(try_convert_to_float)

    # Create a Styler that formats floats with commas and no decimals
    styled_df = display.style.format(
        lambda x: f"{int(x):,}" if isinstance(x, float) and x.is_integer() else x,
        na_rep="",  # Optional: control how NaNs are displayed
    ).set_properties(**{'text-align': 'right'})

    # Center-align column headers (optional)
    styled_df = styled_df.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}]
    )

    display = styled_df

    st.dataframe(display, use_container_width=True)

    df = testdf.reset_index(drop=True).T.iloc[0:8].T

    col1, col2, col3 = st.columns([1, 2.5, 1])

    with col2:
        categories = df.index
        medians = df['Median Annual Wage']
        lower = medians - df['25th Percentile Annual Wage']
        upper = df['75th Percentile Annual Wage'] - medians
        # Create Matplotlib figure
        fig, ax = plt.subplots()
        # Median with IQR (25th to 75th)
        x_labels = df['Occupation']        # Use this for tick labels
        x_pos = range(len(df))       # Positions to plot

        ax.errorbar(x_pos, medians, yerr=[lower, upper], fmt='o', capsize=5,
                    label='Median ± IQR', color='tab:blue')
        # Optional: Add lighter bars for 10th to 90th
        low_range = medians - df['10th Percentile Annual Wage']
        high_range = df['90th Percentile Annual Wage'] - medians
        ax.errorbar(x_pos, medians, yerr=[low_range, high_range], fmt='o', capsize=5,
                    color='tab:blue', alpha=0.3, label='Median ± (10th–90th)')
        # Labels and legend
        ax.set_title("Quantile Summary")
        ax.set_ylabel("Wage")
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels, rotation=90)
        # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        

        means = df['Mean Annual Wage']
        ax.scatter(categories, means, marker='D', color='orange', label='Mean')
        ax.legend()

        st.pyplot(fig)


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
