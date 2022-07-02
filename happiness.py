import numpy as np
import plotly.express as px
import pandas as pd
import streamlit as st
import json


st.set_page_config(layout = 'wide')

st.title('World Happiness Case Study')
st.markdown('The survey data gathered from respondents in various nations determines the countrys ladder score, or happiness rate, which is proportional to how happy we are in our daily lives. Based on a Cantril ladder poll, the national happiness rankings are shown. Respondents from nationally representative samples are asked to visualise a ladder, with a 10 representing their ideal life and a 0 representing their worst scenario. Then, using same 0–10 scale, they are asked to score their own current lifestyles. The GDP per capita, social support, life expectancy, freedom to make decisions, generosity, and sense of corruption are the six criteria that go into determining happiness.')

st.markdown('Source of Data: ')
df = pd.read_csv("world-happiness-report-2021.csv")
st.dataframe(df)
st.markdown('Source of Data: ')
df2 = pd.read_csv("world-happiness-report.csv")
st.dataframe(df2)
st.header('Data Cleaning')
st.markdown('I renamed the 2021 dataset and added a few fields to make it consistent with the other dataset in order to merge it with the happiness data from 2005 to 2020. The data was then integrated once I identified the nations that each databases covered.')

code = '''world_happiness_21.rename({'Ladder score':'Life Ladder','Logged GDP per capita':'Log GDP per capita',"Healthy life expectancy":"Healthy life expectancy at birth"},axis=1,inplace=True)
world_happiness_21["year"] = 2021
happiness_revised = world_happiness.loc[world_happiness['Country name'].isin(world_happiness_21['Country name'])].copy()
happiness_revised.drop(['Positive affect','Negative affect'],axis = 1,inplace=True)'''
st.code(code,language = 'python')

world_happiness = pd.read_csv('world-happiness-report.csv')
world_happiness_21 = pd.read_csv('world-happiness-report-2021.csv')
world_happiness_21.rename({'Ladder score':'Life Ladder',
                    'Logged GDP per capita':'Log GDP per capita',
                     'Healthy life expectancy':'Healthy life expectancy at birth'},axis=1,inplace=True)
world_happiness_21['year'] = 2021
happiness_revised = world_happiness.loc[world_happiness['Country name'].isin(world_happiness_21['Country name'])].copy()
happiness_revised.drop(['Positive affect','Negative affect'],axis = 1,inplace=True)
merged_table = pd.concat([happiness_revised,world_happiness_21[list(happiness_revised.columns)+['Regional indicator']]])

st.dataframe(happiness_revised)
code2 = '''merged_table = pd.concat([happiness_revised,world_happiness_21[list(happiness_revised.columns)+['Regional indicator']]])'''
st.code(code2, language = 'python')
st.dataframe(merged_table)
code3 = '''region_dict = {k:v for k,v in zip(world_happiness_21['Country name'],world_happiness_21['Regional indicator'])}
region_dict'''
code4 = region_dict = {k:v for k,v in zip(world_happiness_21['Country name'],world_happiness_21['Regional indicator'])}
st.code(code3,language = 'python')
st.code(code4,language = 'python')
st.markdown('New column "regions" created to replace indicator')
code5 = '''merged_table['Region'] = merged_table['Country name'].replace(region_dict)
merged_table.drop('Regional indicator',axis = 1,inplace = True)
merged_table'''

merged_table['Region'] = merged_table['Country name'].replace(region_dict)
merged_table.drop('Regional indicator',axis = 1,inplace = True)
merged_table

st.code(code5, language = 'python')
st.dataframe(merged_table)
st.markdown('Description of dataset')
code6 = merged_table.describe()
st.write(code6)

st.title('Data Analysis')
st.header('Correlations and Relationships between different variables')

st.subheader('Interactive Scatter Plot')
col5,col6 = st.columns([2,5])
xscatter = col5.selectbox('Adjustable',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
yscatter = col5.selectbox('Adjustable',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
scatterfig = px.scatter(merged_table, x= xscatter, y = yscatter, color = 'Region', hover_name = 'Country name', height = 550, width = 1000)
col6.plotly_chart(scatterfig)
col5.markdown('You may evaluate the association between many aspects of happiness using this scatter plot. Additionally, we can see from this plot that social support, healthy life expectancy at birth, and log GDP per capita are the three elements most closely related to the life ladder (to reach this conclusion, set "ladder score" on one axis and try assigning other variables to the other axis). Similarly, we may deduce that generosity, views of corruption, and year are the three factors that are most adversely connected with the life ladder. These outcomes support the inferences we formed from the heat map even more.')

st.header('Using Chlorepleth to Compare differne regins')
st.subheader('Interactive Choropleth Map')
col9,col10 = st.columns([2,5])
col9.markdown('You may have observed that the various locations indicated through the various coloured dots appear to be focused in addition to learning which factors are most and least related to life ladder score. I made a globe-shaped choropleth map to better represent the life ladder by area.')
col9.caption('(Draggable buttons, (blank spaces are due to missing data))')
code8 = px.choropleth(merged_table, locations = 'Country name', color = 'Life Ladder', locationmode = 'country names', 
             animation_frame = 'year', category_orders = {'year':np.arange(2005,2022)}, projection = 'orthographic',
             hover_name = "Country name", hover_data = ['Region'],color_continuous_scale= px.colors.sequential.Bluered, width = 800, height = 550
            )
col10.write(code8)
st.subheader('Comparing Regions Box Plot')
col11,col12 = st.columns([2,5])
col11.markdown('Box charts are another another tool for comparing locations. We may examine outliers in a box plot that is divided into regions, as well as compare medians, maximums, and minimums to measure happiness in terms of region.')
fake_d = pd.DataFrame([['A', 2005, -1, -1, -1, -1, -1, -1, -1, r] for r in ['Southeast Asia',
                                                       'Commonwealth of Independent States', 'Sub-Saharan Africa']], 
                      columns = merged_table.columns)
