# this is the statistical analysis page
import streamlit_shadcn_ui as ui
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import altair as alt
import seaborn as sns
import statsmodels.api as sm
data = pd.read_csv("./merged_d2_d3_left_store.csv")

st.title("Statistical Analysis")

st.write("In this section, I applied statistical methods to gain a fresh perspective on our data. Specifically, I used regression analysis to deeply explore our dataset and investigate how factors like 'Ease of Use,' 'Satisfaction,' and 'Price' influence 'Effectiveness.' This method allows us to pinpoint which variables significantly affect the outcome and provides a quantitative foundation for our insights.")

st.write("First, let's examine the scatterplots, where 'Ease of Use,' 'Satisfaction,' and 'Price' are the independent variables, and 'Effectiveness' is the dependent variable.")
# First part: Interactive Scatter Plot Analysis
filtered_data = data
st.subheader("👉 Interactive Scatter Plot Analysis")
tab1, tab2 = st.tabs(["Effectiveness VS. EaseOfUse & Satisfaction ", "Effectiveness VS. Price"])
with tab1:
    st.scatter_chart(
        filtered_data,
        x='Effective',
        y=['EaseOfUse','Satisfaction'],
        color=['#7FFF00', '#DDA0DD'])
    st.write("This graph explores the relationship between 'Ease of Use' and 'Satisfaction' in relation to 'Effectiveness.' On this graph, the x-axis represents the rating range for 'Effectiveness,' while the y-axis displays the rating ranges for both 'Ease of Use' and 'Satisfaction.' Each dot on the scatterplot represents a single observation in our dataset. From the graph, we observe a trend where the 'Effectiveness' score increases as the scores for 'Ease of Use' and 'Satisfaction' increase. The data points are closely clustered, indicating that these two factors likely have a strong positive linear relationship with 'Effectiveness.' By visualizing these relationships through scatterplots, we can infer that there may be a significant correlation between 'Ease of Use,' 'Satisfaction,' and 'Effectiveness.' This visualization effectively supports the notion that higher satisfaction and ease of use are associated with higher effectiveness ratings, suggesting that improving these aspects could enhance the overall effectiveness of a drug.")
with tab2:
    filtered_data4 = filtered_data[filtered_data['Price'] <= 400]
    chart = alt.Chart(filtered_data4).mark_circle().encode(
        x='Price',
        y='Effective', color=alt.value('#FF7F50') ).interactive()
    st.altair_chart(chart, theme=None, use_container_width=True)
    st.write("This plot illustrates the relationship between the price of drugs and their effectiveness as rated on a scale from 0 to 5. From the plot, it is evident that there is a wide range of prices, extending up to about $350, with most of the data points clustered under 300. As for effectiveness, while there is a concentration of ratings between 3.0 and 4.5, indicating that many drugs are perceived as quite effective, there is a noticeable spread across all levels of effectiveness. A key observation is the lack of a clear trend or correlation between price and effectiveness. Drugs priced both low and high show a wide range of effectiveness, suggesting that higher prices do not necessarily correlate with higher effectiveness. This distribution raises questions about the factors that influence drug pricing, given that cost is not consistently reflective of user-rated effectiveness. This plot is valuable for stakeholders in the pharmaceutical industry or healthcare policy makers who are analyzing the cost-effectiveness of drugs, as it visually represents the disconnect that can exist between the price of a medication and its perceived effectiveness.")
    
# Second Part: Heat Plot
st.subheader("👉 Heatmap")
filtered_data5 = filtered_data[['EaseOfUse', 'Effective', 'Satisfaction', 'Price']]
# Create a heatmap using Seaborn and Matplotlib
fig, ax = plt.subplots()  # Create a matplotlib figure and axes
sns.heatmap(filtered_data5.corr(), cmap='Pastel1', annot=True, ax=ax, annot_kws={"size": 8})  # Draw the heatmap
ax.set_title('Correlation Matrix', fontsize=10)
# Display the figure in the Streamlit app
st.pyplot(fig)
st.write("Here, we can see a correlation heatmap that efficiently helps us understand the strength and direction of relationships between multiple variables in a quantitative manner. The correlation coefficients range from -1 to 1, where higher absolute values indicate stronger correlations between two variables. Focusing on 'Effectiveness' as the predicted variable, it is evident from the heatmap that 'Satisfaction' and 'Ease of Use' exhibit strong correlations, with coefficients of 0.86 and 0.63, respectively, suggesting a robust positive relationship with 'Effectiveness.' These values, being closer to 1, indicate that as 'Satisfaction' and 'Ease of Use' increase, 'Effectiveness' tends to increase significantly. In contrast, 'Price' shows virtually no correlation with 'Effectiveness,' as indicated by a very low coefficient of -0.024. This suggests that 'Price' has little to no linear relationship with how effective the drugs are perceived, implying that variations in 'Price' do not reliably predict changes in 'Effectiveness.'")


# Third Part: build Linear Regression Model
st.subheader("👉 Build a Linear Regression Model")
st.write("So far, we’ve visualized the relationship between these variables using both scatterplot and heat map, and we’ve already gained insights about how they correlated to each other. Now, let’s build a regression model to have deeper insights that a heatmap cannot provide on its own. Specifically, even though heatmap and scatterplot displays the strength and direction of the correlation between variables, it does not provide information about the dependency of one variable on another or the specific impact of one unit change in a predictor on the response variable. However, a regression model quantifies how one or more predictor variables influence a dependent variable. It provides coefficients that we will know how much the effectiveness level is expected to increase or decrease when combine the change of ease of use,  satisfaction, and price by one unit. ")
st.latex(r'''
    \textcolor{skyblue}{\text{Effective}} = \beta_0 + \beta_1 \textcolor{orange}{\text{EaseOfUse}} + \beta_2 \textcolor{orange}{\text{Satisfaction}} + \beta_3 \textcolor{orange}{\text{Price}} + \epsilon
''')
html_content = """
Here is our multiple regression model framework with: 
<span style='color: orange;'>EaseOfUse</span>, 
<span style='color: orange;'>Satisfaction</span> and 
<span style='color: orange;'>Price</span> as predictors and 
<span style='color: skyblue;'>Effective</span> as the dependent variable.
"""
# Display the HTML content in Streamlit
st.markdown(html_content, unsafe_allow_html=True)

# Forth Part: Result for regression model
# Button to trigger the display of the regression model results

if ui.button(text="Click to See the Regression Model Results!", key="styled_btn_tailwind", className="bg-purple-400 text-white"):
    st.session_state.regression_model = True

# Conditionally display the regression results
if st.session_state.get('regression_model', False):
    # Defining the dependent and independent variables
    X = filtered_data[['EaseOfUse', 'Satisfaction', 'Price']]  # Independent variables
    y = filtered_data['Effective']  # Dependent variable

    # Adding a constant term to the independent variables (for the intercept)
    X = sm.add_constant(X)

    # Create a linear regression model
    model = sm.OLS(y, X)

    # Fitting the model to the data
    results = model.fit()
    regression_result = results.summary()

    # Display the results in Streamlit
    st.subheader("Regression Analysis Summary:")
    st.text(str(regression_result))
    st.write("Here comes to the result of our regression model. For the model fit results, the R-square equals to 0.752 indicates that approximately 75.2% of the variability in 'Effective' can be explained by the model's predictors ('EaseOfUse', 'Satisfaction', 'Price'). This is a strong level of explanatory power, suggesting the model fits the data well. Moreover, the F-statistics that tests whether at least one predictor variable has a significant effect. The high F-statistic value (908.8), along with the very low Prob (F-statistic), strongly rejects the null hypothesis that all regression coefficients are zero (i.e., no effect). That also means that the model is statistically significant. In addition, both AIC and BIC are used to compare models; lower values are generally better. These criteria penalize the model for the number of predictors, balancing model complexity and goodness of fit. ")
    st.write("According to the regression coefficients and statistics results, the coefficient of EaseOfUse is 0.1502, which means that for a one-unit increase in EaseOfUse, the predicted Effectiveness will increase by 0.1502 units, holding Satisfaction and Price constant. Similarly, the coefficient of Satisfaction is 0.7141, which means that for a one-unit increase in Satisfaction, the predicted Effectiveness will increase by 0.7141 units, holding EaseOfUse and Price constant. The coefficient of Price is not statistically significant (with a very high p-value of 0.468), which means that we cannot conclude that it has a significant effect on the effectiveness. The constant coefficient of 0.6526 represents the predicted value of Effectiveness when all the independent variables are zero.")
    st.write("However, one consideration needs to be addressed is that the condition number which is 3.14e+03 is relatively high, and this situation often arises when one or more independent variables are nearly linearly dependent with others. This condition can inflate the variances of the coefficient estimates, leading to large standard errors and thus less reliable statistical tests.  While multicollinearity does not bias prediction, it makes some individual predictors' effects on the dependent variable statistically insignificant when they might be significant.")

    # Button to display the final model
    if ui.button(text="Click to See Our Final Model ", key="model_a_btn", className="bg-purple-400 text-white"):
        st.write("Incorporating the coefficient values obtained from a regression analysis into the final predictive model, we can get the final model:")
        st.session_state.final_model = True

# Conditionally display the final model equation
if st.session_state.get('final_model', False):
    st.latex(r'''
    \text{Effective} = 0.6526 + 0.1502 \text{EaseOfUse} + 0.7141 \text{Satisfaction} + 0.0000181\text{Price}
    ''')
    