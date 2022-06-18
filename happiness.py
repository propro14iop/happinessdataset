import numpy as np
import plotly.express as px
import pandas as pd
import streamlit as st
import json


st.set_page_config(layout = 'wide')

st.title('World Happiness Case Study')
st.markdown('Happiness is related to our day to day lives, and the survey results collected from people of different countries determine the ladder score of the country, in other words, the happiness rate. The rankings of national happiness are based on a Cantril ladder survey. Nationally representative samples of respondents are asked to think of a ladder, with the best possible life for them being a 10, and the worst possible life being a 0. They are then asked to rate their own current lives on that 0 to 10 scale. 6 factors that contribute to the happiness score are GDP per capita, social support, life expectancy, freedom to make choices, generosity, and perception of corruption.')
st.markdown('In this case study, we will look at the relationsip of each happiness factor to the happiness ladder score, observe changes in the happiness ranking from 2005 - 2021, and make comparisons between countries and regions. We will use a series of graphs and plots to visualize data, with the addition of some verbal analysis. We will also look for explainations for some eccentric happiness score fluctuations of certain countries by researching on their history.')

st.header('Data Sets')
st.markdown('For this case study, I used 2 data sets and combined them into one.')
st.markdown('Source: ')
df = pd.read_csv("world-happiness-report-2021.csv")
st.dataframe(df)
st.markdown('Source: ')
df2 = pd.read_csv("world-happiness-report.csv")
st.dataframe(df2)
st.header('Data Cleaning')
st.markdown('To combine the happiness data of 2021 and happiness data from 2005-2020, I renamed and added some columns the 2021 dataset to match the other dataset. Then I found the countries which both datasets included and combined the data.')

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
st.markdown('Notice in the column "Regional indicator", there are a lot of "<NA>" instead of a region. After looking into this problem, I found out that for the 2021 dataset, they include a regional indicaator, whereas the other dataset does not. To solve this problem, I created a dictionary using a for loop:')
code3 = '''region_dict = {k:v for k,v in zip(world_happiness_21['Country name'],world_happiness_21['Regional indicator'])}
region_dict'''
code4 = region_dict = {k:v for k,v in zip(world_happiness_21['Country name'],world_happiness_21['Regional indicator'])}
st.code(code3,language = 'python')
st.code(code4,language = 'python')
st.markdown('Using this dictionary, created a new column called "Regions" to replace the "Regional indicator"')
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
st.header('Exploring correlations between variables')
st.subheader('Heat Map')
col7,col8 = st.columns([2,5])
corrdf = merged_table.corr()
code7 = px.imshow(corrdf)
col8.write(code7)
col7.markdown('This heat map visualizes the correlation between different happiness factors using the variation of color hue or color intensity. The lighter the color, the more correlated the factors are; the darker the color is the less correlated those variables are.')
col7.markdown('Because this case study is about happiness, we will focus on life ladder. We can tell that apart from life ladder itself, the three lightest boxes are log GDP per capita, healthy life expectancy at birth, and social support. On the other hand, the three darkest colored boxes are generosity, perceptions of corruption, and year.')

st.subheader('Interactive Scatter Plot')
col5,col6 = st.columns([2,5])
xscatter = col5.selectbox('Select the happiness factor to display on the x axis',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
yscatter = col5.selectbox('Select the happiness factor to display on the y axis',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
scatterfig = px.scatter(merged_table, x= xscatter, y = yscatter, color = 'Region', hover_name = 'Country name', height = 550, width = 1000)
col6.plotly_chart(scatterfig)
col5.markdown('This scatter plot allows you to compare the correlation between different happiness factors. We can also observe from this plot that 3 factors most associated with the life ladder are Log GDP per capita, healthy life expectancy at birth, and social support (to reach this conclusion, set "ladder score" on one axis and try assigning other variables to the other axis). Similarly, we can infer that the three variables that are most negatively correlated with the life ladder are generosity, perceptions of corruption, and year. These results further validate the conclusions we made from the heat map.')

st.subheader('Interactive Choropleth Map')
col9,col10 = st.columns([2,5])
col9.markdown('Besides finding out the most associated variables to life ladder score and the least associated, you might also noticed that the different regions shown through the different colored dots seem to be concentrated. To better visualize the life ladder by region, I created a choropleth map in the shape of a globe.')
col9.caption('(Drag or click on the bar to see the ladder score of different countries around the world over time (blank spaces are due to missing data))')
code8 = px.choropleth(merged_table, locations = 'Country name', color = 'Life Ladder', locationmode = 'country names', 
             animation_frame = 'year', category_orders = {'year':np.arange(2005,2022)}, projection = 'orthographic',
             hover_name = "Country name", hover_data = ['Region'],color_continuous_scale= px.colors.sequential.Bluered, width = 800, height = 550
            )
col10.write(code8)
st.subheader('Comparing Regions Box Plot')
col11,col12 = st.columns([2,5])
col11.markdown('Another way to compare regions is through box plots. In a box plot grouped by regions, not only can we observe outliers, we can also analyze happiness in terms of region and compare medians, max, and mins.')
fake_d = pd.DataFrame([['A', 2005, -1, -1, -1, -1, -1, -1, -1, r] for r in ['Southeast Asia',
                                                       'Commonwealth of Independent States', 'Sub-Saharan Africa']], 
                      columns = merged_table.columns)

ani_data = pd.concat([merged_table, fake_d]).sort_values(['year','Region']).reset_index(drop = True)

code9 = px.box(ani_data, y = 'Region', x = 'Life Ladder',hover_name = 'Country name',  
       animation_frame = 'year', category_orders = {'year':np.arange(2005,2022)}, height = 600, width = 850, range_x = [0,9])
col12.write(code9)
col11.caption('(Drag or click on the animation bar to select the year.)')
col11.markdown('From this box plot, we can see that there are not many outliers, about 0-3 per year from 2005-2021. Also, the region "North America and ANZ" has always been very small and ahead of most other regions. This probably suggests that the countries in that region are collectively happier than most other countries in the world. We can also see that Western Europe is a region that has had high ladder score from 2005 to 2021, whereas Sub-Saharan Africa and South Asia are two regions that had a relatively low ladder score.')


st.subheader('Interactive Bar Chart (top 10 countries of each year)')
def by_year(x):
    return merged_table[merged_table['year'] == x].sort_values(by = ['Life Ladder'], ascending= False).head(10)
y05 = by_year(2005)
y06 = by_year(2006)
y07 = by_year(2007)
y08 = by_year(2008)
y09 = by_year(2009)
y10 = by_year(2010)
y11 = by_year(2011)
y12 = by_year(2012)
y13 = by_year(2013)
y14 = by_year(2014)
y15 = by_year(2015)
y16 = by_year(2016)
y17 = by_year(2017)
y18 = by_year(2018)
y19 = by_year(2019)
y20 = by_year(2020)
y21 = by_year(2021)
years = [y05,y06,y07,y08,y09,y10,y11,y12,y13,y14,y15,y16,y17,y18,y19,y20,y21]
year_num = np.arange(2005,2022)
titles = [f'Top 10 Countries With The Highest Ladder Score In {year}' for year in year_num]
top_10_life_ladder = {}
for i,x in enumerate(years):
    temp_fig = px.bar(x, x="Life Ladder", y="Country name", orientation='h',
           color ='Region', hover_name = 'Country name', title = titles[i], height = 600, width = 800)
    top_10_life_ladder.update({year_num[i]:temp_fig})
col3,col4 = st.columns([2,5])
yearoption = col3.selectbox('Select the year',year_num)
col4.write(top_10_life_ladder[yearoption])
col3.markdown('From the previous charts, it was difficult to observe the change of happiness score over time in terms of both country. This bar chart displays the top 10 countries of each year, colored by region.')
col3.markdown("From this bar chart, we can see that in the first years, there was a bigger variety of countries from different regions. But as time progresses, ")


col,col2 = st.columns([2,5])
xoption = col.selectbox('Select the happiness factor to display on the X axis',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
yoption = col.selectbox('Select the happiness factor to display on the Y axis',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
figscatter = px.scatter(merged_table, x= xoption, y = yoption, color = 'Region', hover_name = 'Country name', height = 600, width = 900)
col2.plotly_chart(figscatter)
col.markdown('')





