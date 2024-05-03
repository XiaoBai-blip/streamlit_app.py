import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import altair as alt
import seaborn as sns
import numpy as np
import plotly.express as px

st.title("Quantitative Analysis of Consumer Feedback and Its Relation with the Perceived Effectiveness of Pharmaceutical Products: A Regression Analysis Approach")
st.divider()
st.header("Xiao Bai (1862548450)")
st.divider()
st.subheader("Research Objective and Webapp Guidance")
st.write("The aim of this research is to investigate the wide array of FDA-regulated drugs available in the market and to examine consumer experiences with these drugs. I will analyze various consumer rating metrics to understand how they relate to each other. Specifically, my study employs  regression analysis to explore the relationship between drug effectiveness and other factors, such as consumer ratings of usability, satisfaction, and drug prices. I intend to determine whether drugs classified as 'effective' by consumers are perceived as such because they are cost-effective or because consumers are satisfied with their use. This research offer actionable insights for pharmaceutical companies to refine their product development and marketing strategies based on consumer feedback, potentially leading to improved user satisfaction and better market performance.")
st.write("This web app is organized into three main pages: The first page provides a fundamental introduction to the three data sources utilized and includes some exploratory data analysis. It features static histograms that depict the distribution density of characteristics critical to subsequent analyses. For a more detailed, interactive examination of each characteristic, users can employ the filter options available on the sidebar. Additionally, this page displays three tables that enumerate the counts of drugs by various characteristics such as condition, type, and form, and lastly there are violin plots visualizing the distribution of different forms of drugs. The second page is dedicated to statistical analysis, outlining the steps taken to develop our linear regression model. The final page includes questions about the overall project, fostering a deeper reflection on the research findings. Explanations for all visualizing figures are provided below each plot or chart to enhance understanding.")
st.write("The research finding shows that the linear regression model constructed and validated for statistical significance indicates that the characteristics 'Satisfaction' and 'Ease of Use' significantly influence the effectiveness rating of a drug. Specifically, a one-unit increase in 'Ease of Use' is associated with an increase of 0.1502 units in the predicted effectiveness. Similarly, a one-unit increase in 'Satisfaction' leads to an increase of 0.7141 units in the predicted effectiveness. Conversely, 'Price' does not appear to affect the effectiveness rating significantly.")
st.subheader("Things that Could Be Improved...")
st.write("One aspect of the dataset that requires attention is the time-intensive process of extracting 'Description' for FDA-regulated drugs via web scraping. As a result, some drug descriptions are currently missing in this dataset. Future improvements could include using more advanced data extraction algorithms beyond BeautifulSoup to enhance the completeness of our data. However, it is advisable to directly visit the official website for accurate descriptions of specific drugs when they are not available in our descriptive table.")



