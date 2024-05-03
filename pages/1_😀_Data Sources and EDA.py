# this page for data source and eda

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import altair as alt
import seaborn as sns
import numpy as np
import plotly.express as px

# load the data
data = pd.read_csv("../merged_d2_d3_left_store.csv")

# this is sidebar section
st.sidebar.header("Filter options")

# sidebar: the distribution of all the numerical variables & range classfier

distribution = st.sidebar.selectbox(
'See the Distribution of Drug Performance',
('All', 'EaseOfUse', 'Effective', 'Price', 'Reviews', 'Satisfaction'))

filtered_data = data
if distribution == 'All':
    # Data sources and code
    st.title("Data Sources")
    with st.expander("Data Source 1"):# construct expander
        st.write("https://open.fda.gov/apis/drug/label/")
        st.write("This database offers comprehensive details on human drugs across various types and it provides each drug's brand name and genenic name. It encompasses 50+ variables, all in string type, providing intricate information about each drug category. For instance, it indicates whether the drug is a controlled substance, outlines the potential types of abuse associated with it, and delineates the relevant adverse reactions.")
    with st.expander("Data Source 2"):
        st.write("https://www.kaggle.com/datasets/thedevastator/drug-performance-evaluation/data")
        st.write("This dataset contains performance metrics for 37 common conditions, including drug name, type, form, average price, reviews, effectiveness, ease of use, and satisfaction. It also shows relevant information about the drug with a focus on the consumer experience aspect.")
    with st.expander("Data Source 3"):
        st.write("https://dailymed.nlm.nih.gov/dailymed/")
        st.write("The National Library of Medicine (NLM)’s DailyMed searchable database provides the most recent labeling submitted to the Food and Drug Administration (FDA) by companies and currently in use. DailyMed contains detailed descriptions of all drugs, labeling for prescription and nonprescription drugs for human and animal use, and for additional products such as medical gases, devices, cosmetics, dietary supplements, and medical foods.")
    with st.expander("Code for Obtaining Datasets"):       
        code = '''import pandas as pd
import requests
import pprint
import json
import sqlite3
from bs4 import BeautifulSoup
import bs4
import re
# Data Source 1: only get the first 1000 rows
rx = 'https://api.fda.gov/drug/label.json?search=(effective_time:[20090601+TO+20240413]+AND+openfda.product_type:prescription)&limit=1000'
json_rx = requests.get(rx, headers={"user-agent": "asdf"})
json_rx.url
r = [ { "generic_name": row["openfda"]["generic_name"][0].lower(), "FDA_brand_name": row["openfda"]["brand_name"][0], 'ndc': row["openfda"]["product_ndc"][0], "effective_time": row["effective_time"], "product_type": row["openfda"]["product_type"][0] } 
     for row in json_rx.json()["results"] if row["openfda"]]
dataset1 = pd.DataFrame(r)
# Data Source 2
base_url = "https://dailymed.nlm.nih.gov"
descriptions = []
search_factor = "FDA_brand_name"
# iterate each item in the first dataset('r')
for record in r:  
# Search result: get all items in 'brand_name' from first dataset and check if those can also be found from the website, use beautiful soup to save all matches
    processed_brand_name = record[search_factor].replace(" ", "+")
    result = requests.get(f"{base_url}/dailymed/search.cfm?labeltype=all&query={processed_brand_name}")
    soup = BeautifulSoup(result.content, 'html.parser')   
# Processing search results
    links = soup.find_all("a", class_="drug-info-link") 
# Handling no matches: if no matching results found on the website, return a dictionary with the drug name and a na description  
    if not links: # if true, append a dictionary and then skip to the next record in the loop
        descriptions.append({'FDA_brand_name': record[search_factor], 'dailymed_name': record[search_factor], 'description': 'N/A'})
        continue         
# Fetching Details of the Best Match
    link = links[0] # find the best match result, assuming the first result is the most relevant
    url = base_url + link.get('href')
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
# Tries to find <a> tags without a class that contain text matching "DESCRIPTION", if none are found, look for tags containing "Purposes". 
    title = soup.find_all('a', {"class": ""}, text=re.compile("DESCRIPTION")) if soup.find_all('a', {"class": ""}, text=re.compile("DESCRIPTION")) else soup.find_all('a', {"class": ""}, text=re.compile("Purposes"))   
    if not title:
        descriptions.append({'FDA_brand_name': record[search_factor], 'dailymed_name': record[search_factor], 'description': 'N/A'})
        continue
    title = title[0]
    paras = title.find_next_siblings("div", {"class": "Section toggle-content closed long-content"})    
    if not paras:
        descriptions.append({'FDA_brand_name': record[search_factor], 'dailymed_name': record[search_factor], 'description': 'N/A'})
        continue
    des = ''.join([ p.text.replace('\n', '') for p in paras ]) # get and sum up all the paragraphs    
    descriptions.append({'FDA_brand_name': record[search_factor], 'dailymed_name': link.text, 'description': des} if des else {'FDA_brand_name': record[search_factor], 'dailymed_name': link.text, 'description': 'N/A'})
dataset2 = pd.DataFrame(descriptions)
dataset2 = dataset2.rename(columns={'dailymed_name': 'brand_name'})
dataset2
# Data Source 3
dataset3 = pd.read_csv("Drug_clean.csv")
dataset3 = dataset3.rename(columns={'Drug': 'FDA_brand_name'})
dataset3'''
        st.code(code, language='python')
    
    st.title("Exploratory Data Analysis")
# This part is to build the 5 historgrams for review, satisfication, price, effective and easeofuse
    st.subheader("👉 Distributions of Various Rating Metrics")
    fig, axes = plt.subplots(2, 3, figsize=(15, 10),facecolor='white')  # Adjust the layout size as needed
    axes = axes.flatten()  # Flatten the array to make indexing easier

    # Plotting histograms on separate subplots
    filtered_data2 = filtered_data[filtered_data['Reviews'] <= 2000]
    filtered_data2['Reviews'].hist(ax=axes[0], color='#27F1FF', edgecolor='grey')
    axes[0].set_title('Distribution of Reviews', fontsize=16.5, fontweight='bold')
    axes[0].set_xlabel('Number of Reviews', fontsize=15)
    axes[0].set_ylabel('Frequency', fontsize=13)
    axes[0].grid(True, linestyle=':', linewidth=0.3, alpha=0.3, color='blue')
    axes[0].axvline(filtered_data2['Reviews'].mean(), color='#010CFD', linestyle='dashed', linewidth=1)

    filtered_data['EaseOfUse'].hist(ax=axes[1], color='#9AFD01', edgecolor='grey')
    axes[1].set_title('Distribution of EaseOfUse', fontsize=16.5, fontweight='bold')
    axes[1].set_xlabel('EaseOfUse Rating Score', fontsize=15)
    axes[1].set_ylabel('Frequency', fontsize=13)
    axes[1].grid(True, linestyle=':', linewidth=0.3, alpha=0.3, color='blue')
    axes[1].axvline(filtered_data2['EaseOfUse'].mean(), color='#010CFD', linestyle='dashed', linewidth=1)

    filtered_data['Effective'].hist(ax=axes[2], color='#C0C6F9', edgecolor='grey')
    axes[2].set_title('Distribution of Effectiveness', fontsize=16.5, fontweight='bold')
    axes[2].set_xlabel('Effectiveness Rating Score', fontsize=15)
    axes[2].set_ylabel('Frequency', fontsize=13)
    axes[2].grid(True, linestyle=':', linewidth=0.3, alpha=0.3, color='blue')
    axes[2].axvline(filtered_data2['Effective'].mean(), color='#010CFD', linestyle='dashed', linewidth=1)

    filtered_data3 = filtered_data[filtered_data['Price'] <= 4000]
    filtered_data3['Price'].hist(ax=axes[3], color='#FFD827', edgecolor='grey')
    axes[3].set_title('Distribution of Price', fontsize=16.5, fontweight='bold')
    axes[3].set_xlabel('Price (in $)', fontsize=15)
    axes[3].set_ylabel('Frequency', fontsize=13)
    axes[3].grid(True, linestyle=':', linewidth=0.3, alpha=0.3, color='blue')
    axes[3].axvline(filtered_data2['Price'].mean(), color='#010CFD', linestyle='dashed', linewidth=1)

    filtered_data['Satisfaction'].hist(ax=axes[4], color='#F6F9C0', edgecolor='grey')
    axes[4].set_title('Distribution of Satisfaction', fontsize=16.5, fontweight='bold')
    axes[4].set_xlabel('Satisfaction Rating Score', fontsize=15)
    axes[4].set_ylabel('Frequency', fontsize=13)
    axes[4].grid(True, linestyle=':', linewidth=0.3, alpha=0.3, color='blue')
    axes[4].axvline(filtered_data2['Satisfaction'].mean(), color='#010CFD', linestyle='dashed', linewidth=1)

    # Clear unused subplot (if number of plots is less than subplot grid)
    axes[5].axis('off')  # Hide the 6th subplot if no additional data

    # Adjust layout to prevent overlap
    plt.tight_layout()
    st.pyplot(fig)
    st.write("Let's examine the histograms of five rating metrics that we'll use for further analysis. The first metric, 'Reviews,' represents the number of reviews for each condition and drug type. The majority of the counts lie between 0 and 100. Similarly, most drug prices fall under $500, applicable to both prescription and over-the-counter drugs.")
    st.write("The other three factors—'EaseOfUse,' 'Effective,' and 'Satisfaction'—are rated on a scale from 0 to 5, based on consumer experience. In the 'Effectiveness' distribution, most ratings cluster around 3 to 4.5, indicating that people generally find the drugs effective for treating specific conditions. For 'Ease of Use,' the ratings predominantly range from 3.5 to 4.75, suggesting that most drugs are considered very easy to use. The 'Satisfaction' ratings mainly fall between 2.25 and 4, showing that people find the drugs partly satisfying.")
    st.write("The distributions for 'Ease of Use' and 'Effectiveness' are right-skewed, indicating that higher ratings are more common. In contrast, the 'Satisfaction' distribution is unimodal, with a single prominent peak, reflecting a more concentrated range of opinions.")
    st.write("Note: For a clearer view, you can access interactive histograms for each characteristic by using the filter options in the sidebar.")
    
# This part is to build the combined one histogram for EaseOfUse, Effective, and Satisfaction
    x1 = filtered_data['EaseOfUse']
    x2 = filtered_data['Effective']
    x3 = filtered_data['Satisfaction']
    # Group data together
    hist_data = [x1, x2, x3]
    colors = ['#F8B611', '#11B9F8', '#CF95FF']
    group_labels = ['EaseOfUse Distribution', 'Effectiveness Distribution', 'Satisfaction Distribution']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,bin_size=[.1, .25, .5], colors=colors, show_hist=False, show_rug=True)
    
    fig.update_layout(
        xaxis_title='Rating Score',
        yaxis_title='Density',
        template='plotly_white',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="RebeccaPurple"
        )
    )
  
    # Plot!
    st.plotly_chart(fig)
    st.write("You can explore the distribution density and values of each specific observation using this interactive graph. You can see the overlapping distributions more effectively. For a clearer view, you can access interactive histograms for each characteristic by using the filter options in the sidebar.")
    
# This part is to buid the three tables with three tabs: Condition, Type, Form
    st.subheader("👉 Display Drug Counts by Condition, Type, and Form")
    tab1, tab2, tab3 = st.tabs(["Condition", "Type", "Form"])
    with tab1:         
        # Display the value counts for the 'Condition' column
        condition_counts = filtered_data['Condition'].value_counts()
        st.write("Table shows different conditions with number of drugs in regards to treating the specific condition", condition_counts)
    with tab2:
        # Display the value counts for the 'Type' column
        filtered_data_non_empty = filtered_data[filtered_data['Type'].isin(['RX', 'OTC', 'RX/OTC'])]
        type_counts = filtered_data_non_empty['Type'].value_counts()
        st.write("Types of drugs based on how they can be purchased (Perscription/Over-the-Counter)", type_counts)
    with tab3:
        table = filtered_data['Form'].value_counts()
        st.write("Number of drugs of each form", table)
        
# This part is to buid the violinplot       
    st.subheader("👉 Price Distribution by Different Drug Forms")
    # Data filtering
    filtered_data6 = filtered_data[filtered_data['Price'] <= 400]

    # Dynamic sizing of the plot based on unique forms
    unique_forms = filtered_data6['Form'].nunique()
    figsize = (12, max(6, 1.2 * unique_forms))  # Ensure the plot is not too cramped

    # Setting up the figure
    plt.figure(figsize=figsize)
    palette = ['#9DDECF', '#9DAADE', '#DE9DC3','#DEC79D','#BEDE9D','#9DB7DE']
    sns.violinplot(
        data=filtered_data6,
        x='Price',
        y='Form',
        palette = palette,
        inner='box',
        scale='width',  # Adjusts the violin width to match the number of samples in each category
        linewidth=1.5  # Thicker lines for better visibility
    )

    # Enhancing plot aesthetics
    plt.title('Price Distribution by Drug Forms', fontsize=16, fontweight='bold')
    plt.xlabel('Price in Dollars', fontsize=14)
    plt.ylabel('Drug Form', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.2, color='blue')  # Slightly more visible grid lines
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Display the plot in Streamlit and clear the figure afterwards to prevent reuse
    st.pyplot(plt.gcf())  # plt.gcf() gets the current figure
    plt.clf()  # Clear the figure after rendering
    st.write("The six violin plots offer a detailed visualization of the distribution of drug prices across different forms. Each violin's shape represents the kernel density estimation (KDE), which helps estimate the probability density function for the price variable. Where the violin is wider, the data are more concentrated, indicating a higher probability density.")
    st.write("In the plots, the prices for drugs in liquid (drink), tablet, and cream forms typically cluster around $25. Conversely, the narrower sections of the violins above 100 dollars suggest that only a few drugs are priced higher than this amount. For the other three forms—capsule, liquid (inject), and other—the symmetry around the median (indicated by a white dot) suggests that the distribution of prices for these drug forms is balanced, with no significant skew toward higher or lower prices. There are also no notable outliers, indicating that the data points do not stray far from the median.")
    st.write("This symmetry implies that the prices for these forms of drugs are as likely to be above the median as they are below it, suggesting a balanced distribution without a tendency toward being predominantly cheaper or more expensive.")
    

# When it is 'EaseOfUse' option
elif distribution == 'EaseOfUse':
    # First part: chart and table
    tab1, tab2 = st.tabs(["Chart", "Descriptive Table"])
    with tab1:         
        interactive_data = pd.DataFrame(filtered_data, columns=['EaseOfUse'])
        # Widget to adjust the number of bins
        bin_size = st.slider('Select number of bins for histogram', min_value=5, max_value=50, value=10, step=5)

        # Create the histogram using Plotly Express
        fig = px.histogram(interactive_data, x='EaseOfUse',
                           nbins=bin_size,  # Number of bins based on slider
                           title='Ease of Use Distribution',
                           labels={'EaseOfUse': 'Ease of Use'}, 
                           color_discrete_sequence=['#9AFD01'],
                           hover_data=interactive_data.columns) # Ensures all columns data are shown on hover
        # Add plot styling
        fig.update_layout(
            xaxis_title_text='EaseOfUse Scores',  # x-axis label
            yaxis_title_text='Count',  # y-axis label
            plot_bgcolor='white',  # Background color
            bargap=0.2  # Gap between bars
        )

        # Display the interactive histogram in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        # Display the descriptive table
        table1 = filtered_data['EaseOfUse'].describe()
        st.write(table1)
        
    # Second part: slider and table
    # Display the subheader
    st.subheader("Select a Rating Range for EaseOfUse to See Corresponding Drugs with Other Information!")
    st.write("Here you can explore in-depth information about conditions, drug names, and other specifics with an adjustable range for 'EaseOfUse'. You now have access to descriptions for some drugs that were provided by the FDA, ensuring accuracy and detail. More interestingly, you can investigate the rating scores of other characteristics by setting a limit on the 'EaseOfUse' rating. For example, setting a rating limit between 4 and 5 allows you to see the corresponding Effective/Price/Reviews values for these highly usable drugs. This feature lets you pinpoint exactly how other aspects of the drugs perform when their usability is rated highly.")
    # Create a slider for selecting the range of 'EaseOfUse' ratings
    easeofuse = st.slider('EaseOfUse Rating', min_value=0, max_value=5, value=(0, 5))
    filtered_data = filtered_data[
    (filtered_data['EaseOfUse'] >= easeofuse[0]) & 
    (filtered_data['EaseOfUse'] <= easeofuse[1])
    ]
    st.write(filtered_data)
    
    # Third Part: the third table
    df_ease = filtered_data.groupby(['Drug Generic Name','Condition'])['EaseOfUse'].mean().reset_index()
    df_ease = df_ease.sort_values(by = 'EaseOfUse', ascending = False).iloc[:20]
    st.subheader("Top 20 Drugs that Have the Highest Average Ease Of Use Level And the Corresponding Conditions")
    # Display the DataFrame
    st.dataframe(df_ease)


# When it is 'Effective' option
elif distribution == 'Effective':
    # First part: chart and table
    tab1, tab2 = st.tabs(["Chart", "Descriptive Table"])
    with tab1:
        interactive_data2 = pd.DataFrame(filtered_data, columns=['Effective'])
        # Widget to adjust the number of bins
        bin_size = st.slider('Select number of bins for histogram', min_value=5, max_value=50, value=10, step=5)
        # Create the histogram using Plotly Express
        fig = px.histogram(interactive_data2, x='Effective',
                           nbins=bin_size,  # Number of bins based on slider
                           title='Effectiveness Distribution',
                           labels={'Effective': 'Effectiveness'}, 
                           color_discrete_sequence=['#C0C6F9'],
                           hover_data=interactive_data2.columns) # Ensures all columns data are shown on hover
        # Add plot styling
        fig.update_layout(
            xaxis_title_text='Effectiveness Scores',  # x-axis label
            yaxis_title_text='Count',  # y-axis label
            plot_bgcolor='white',  # Background color
            bargap=0.2  # Gap between bars
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        # Display the descriptive table
        table2 = filtered_data['Effective'].describe()
        st.write(table2)
    # Second part: slider and table
    # Display the subheader
    st.subheader("Select a Rating Range for Effectiveness to See Corresponding Drugs with Other Information!")
    st.write("Here you can explore in-depth information about conditions, drug names, and other specifics with an adjustable range for 'Effective'. You now have access to descriptions for some drugs that were provided by the FDA, ensuring accuracy and detail. More interestingly, you can investigate the rating scores of other characteristics by setting a limit on the Effectiveness Rating. For example, setting a rating limit between 4 and 5 allows you to see the corresponding EaseOfUse/Price/Reviews values for these highly usable drugs. This feature lets you pinpoint exactly how other aspects of the drugs perform when their effectiveness is rated highly.")
    # Create a slider for selecting the range of 'EaseOfUse' ratings
    effective = st.slider('Effectiveness Rating', min_value=0, max_value=5, value=(0, 5))
    filtered_data = filtered_data[
    (filtered_data['Effective'] >= effective[0]) & 
    (filtered_data['Effective'] <= effective[1])
    ]
    st.write(filtered_data)
    
    # Third Part: the third table
    df_eff = filtered_data.groupby(['Drug Generic Name','Condition'])['Effective'].mean().reset_index()
    df_eff = df_eff.sort_values(by = 'Effective', ascending = False).iloc[:20]
    st.subheader("Top 20 Drugs that Have the Highest Average Effectiveness Level And the Corresponding Conditions")
    # Display the DataFrame
    st.dataframe(df_eff)
    
# When it is 'Price' option
elif distribution == 'Price':
    # First part: chart and table
    tab1, tab2 = st.tabs(["Chart", "Descriptive Table"])
    with tab1:
        interactive_data3 = pd.DataFrame(filtered_data, columns=['Price'])
        # Widget to adjust the number of bins
        bin_size = st.slider('Select number of bins for histogram', min_value=5, max_value=50, value=10, step=5)
        # Create the histogram using Plotly Express
        fig = px.histogram(interactive_data3, x='Price',
                           nbins=bin_size,  # Number of bins based on slider
                           title='Price Distribution',
                           labels={'Price': 'Price in Dollars'}, 
                           color_discrete_sequence=['#FFD827'],
                           hover_data=interactive_data3.columns) # Ensures all columns data are shown on hover
        # Add plot styling
        fig.update_layout(
            xaxis_title_text='Price in Dollars',  # x-axis label
            yaxis_title_text='Count',  # y-axis label
            plot_bgcolor='white',  # Background color
            bargap=0.2  # Gap between bars
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        # Display the descriptive table
        table3 = filtered_data['Price'].describe()
        st.write(table3)
        
    # Second part: slider and table
    # Display the subheader
    st.subheader("Select a Price Range to See Corresponding Drugs with Other Information!")
    st.write("Here you can explore in-depth information about conditions, drug names, and other specifics with an adjustable range for 'Price'. You now have access to descriptions for some drugs that were provided by the FDA, ensuring accuracy and detail. More interestingly, you can investigate the rating scores of other characteristics by setting a limit on the Price range. For example, setting a range limit between 50 and 100 allows you to see the corresponding EaseOfUse/Effectiveness/Reviews values for these drugs that within this price range. This feature lets you pinpoint exactly how other aspects of the drugs perform when their price is set to be within this range.")
    price = st.slider('Price range', min_value=0, max_value=2000, value=(0, 2000))
    filtered_data = filtered_data[
    (filtered_data['Price'] >= price[0]) & 
    (filtered_data['Price'] <= price[1])
    ]
    st.write(filtered_data)
    
    # Third Part: the third table
    df_price = filtered_data.groupby(['Drug Generic Name','Condition'])['Price'].mean().reset_index()
    df_price = df_price.sort_values(by = 'Price', ascending = False).iloc[:20]
    st.subheader("Top 20 Drugs that Have the Highest Average Price And the Corresponding Conditions")
    # Display the DataFrame
    st.dataframe(df_price)

# When it is 'Reviews' option
elif distribution == 'Reviews':
    # First part: chart and table
    tab1, tab2 = st.tabs(["Chart", "Descriptive Table"])
    with tab1:
        interactive_data4 = pd.DataFrame(filtered_data, columns=['Reviews'])
        # Widget to adjust the number of bins
        bin_size = st.slider('Select number of bins for histogram', min_value=5, max_value=50, value=10, step=5)

        # Create the histogram using Plotly Express
        fig = px.histogram(interactive_data4, x='Reviews',
                           nbins=bin_size,  # Number of bins based on slider
                           title='Number of Reviews Distribution',
                           labels={'Reviews': 'Reviews'}, 
                           color_discrete_sequence=['#27F1FF'],
                           hover_data=interactive_data4.columns) # Ensures all columns data are shown on hover
        # Add plot styling
        fig.update_layout(
            xaxis_title_text='# of Reviews',  # x-axis label
            yaxis_title_text='Count',  # y-axis label
            plot_bgcolor='white',  # Background color
            bargap=0.2  # Gap between bars
        )
        # Display the interactive histogram in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        # Display the descriptive table
        table4 = filtered_data['Reviews'].describe()
        st.write(table4)
        
    # Second part: slider and table
    # Display the subheader
    st.subheader("Select a Range for the number of Reviews to See Corresponding Drugs with Other Information!")
    st.write("Here you can explore in-depth information about conditions, drug names, and other specifics with an adjustable range for 'Review'. You now have access to descriptions for some drugs that were provided by the FDA, ensuring accuracy and detail. More interestingly, you can investigate the rating scores of other characteristics by setting a limit on the the count of reviews. For example, setting a limit between 500 and 1000 allows you to see the corresponding EaseOfUse/Price/Satisfication values for these drugs. This feature lets you pinpoint exactly how other aspects of the drugs perform when their current number of reviews is within this range.")
    review = st.slider('# of Reviews', min_value=0, max_value=1000, value=(0, 1000))
    filtered_data = filtered_data[
    (filtered_data['Reviews'] >= review[0]) & 
    (filtered_data['Reviews'] <= review[1])
    ]
    st.write(filtered_data)
    
    # Third Part: the third table
    df_review = filtered_data.groupby(['Drug Generic Name','Condition'])['Reviews'].mean().reset_index()
    df_review = df_review.sort_values(by = 'Reviews', ascending = False).iloc[:20]
    st.subheader("Top 20 Drugs that Have the Highest Average Number of Reviews And the Corresponding Conditions")
    # Display the DataFrame
    st.dataframe(df_review)

# When it is 'Satisfication' option
else:  
    # First part: chart and table
    tab1, tab2 = st.tabs(["Chart", "Descriptive Table"])
    with tab1:
        interactive_data5 = pd.DataFrame(filtered_data, columns=['Satisfaction'])
        # Widget to adjust the number of bins
        bin_size = st.slider('Select number of bins for histogram', min_value=5, max_value=50, value=10, step=5)
        # Create the histogram using Plotly Express
        fig = px.histogram(interactive_data5, x='Satisfaction',
                           nbins=bin_size,  # Number of bins based on slider
                           title='Satisfaction Score',
                           labels={'Satisfaction': 'Satisfaction Score'}, 
                           color_discrete_sequence=['#F6F9C0'],
                           hover_data=interactive_data5.columns) # Ensures all columns data are shown on hover
        # Add plot styling
        fig.update_layout(
            xaxis_title_text='Satisfaction Score',  # x-axis label
            yaxis_title_text='Count',  # y-axis label
            plot_bgcolor='white',  # Background color
            bargap=0.2  # Gap between bars
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        # Display the descriptive table
        table5 = filtered_data['Satisfaction'].describe()
        st.write(table5)
    # Second part: slider and table
    # Display the subheader
    st.subheader("Select a Rating Range for Satisfaction to See Corresponding Drugs with Other Information!")
    st.write("Here you can explore in-depth information about conditions, drug names, and other specifics with an adjustable range for 'Satisfaction'. You now have access to descriptions for some drugs that were provided by the FDA, ensuring accuracy and detail. More interestingly, you can investigate the rating scores of other characteristics by setting a limit on the Satisfaction Rating. For example, setting a rating limit between 4 and 5 allows you to see the corresponding EaseOfUse/Price/Reviews values for these drugs. This feature lets you pinpoint exactly how other aspects of the drugs perform when their satisfaction is rated highly.")
    # Create a slider for selecting the range of 'EaseOfUse' ratings
    satisfaction = st.slider('Satisfaction Rating', min_value=0, max_value=5, value=(0, 5))
    filtered_data = filtered_data[
    (filtered_data['Satisfaction'] >= satisfaction[0]) & 
    (filtered_data['Satisfaction'] <= satisfaction[1])
    ]
    st.write(filtered_data)
    
    # Third Part: the third table
    df_sat = filtered_data.groupby(['Drug Generic Name','Condition'])['Satisfaction'].mean().reset_index()
    df_sat = df_sat.sort_values(by = 'Satisfaction', ascending = False).iloc[:20]
    st.subheader("Top 20 Drugs that Have the Highest Average Satisfaction Level And the Corresponding Conditions")
    # Display the DataFrame
    st.dataframe(df_sat)