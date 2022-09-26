import numpy as np
import plotly.express as px
import pandas as pd
import streamlit as st
import json


st.set_page_config(layout = 'wide')

st.title('World Happiness Case Study 2022 - Edward Huang')
st.markdown(' This data is from a survey conducted by the sustainable goals group. The survey data gathered from respondents in various nations determines the countrys ladder score, or happiness rate, which is proportional to how happy we are in our daily lives. Based on a Cantril ladder poll, the national happiness rankings are shown. Respondents from nationally representative samples are asked to visualise a ladder, with a 10 representing their ideal life and a 0 representing their worst scenario. Then, using same 0–10 scale, they are asked to score their own current lifestyles. The GDP per capita, social support, life expectancy, freedom to make decisions, generosity, and sense of corruption are the six criteria that go into determining happiness.')

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
st.markdown('Created a new column called regions which replaced the old column "regional indicator" ')
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
st.header('Relationships between variables and happiness')
st.subheader('Heat Map')
col7,col8 = st.columns([2,5])
corrdf = merged_table.corr()
code7 = px.imshow(corrdf)
col8.write(code7)
col7.markdown('Using variations in colour hue or colour intensity, this heat map shows the relationship between several elements that affect happiness. The correlation between the variables is higher when the colour is lighter and lower when the colour is darker.')
col7.markdown('Since the subject of this case study is happiness, we shall concentrate on the life ladder. Aside from the life ladder itself, we can see that the three boxes with the lowest weights are log GDP per capita, healthy life expectancy at birth, and social support. The three coloured boxes with the darkest backgrounds are year, opinions of corruption, and generosity.')

st.subheader('Plotly Scatter Plot')
col5,col6 = st.columns([2,5])
xscatter = col5.selectbox('Selectable Factors',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
yscatter = col5.selectbox('Select each factor to happiness',('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
scatterfig = px.scatter(merged_table, x= xscatter, y = yscatter, color = 'Region', hover_name = 'Country name', height = 550, width = 1000)
col6.plotly_chart(scatterfig)
col5.markdown('You may evaluate the association between many aspects of happiness using this scatter plot. Additionally, we can see from this plot that social support, healthy life expectancy at birth, and log GDP per capita are the three elements most closely related to the life ladder (to reach this conclusion, set "ladder score" on one axis and try assigning other variables to the other axis). Similarly, we may deduce that generosity, views of corruption, and year are the three factors that are most adversely connected with the life ladder. These outcomes support the inferences we formed from the heat map even more.')

st.header('Regional Comparasons')
st.subheader('Choropleth Map')
col9,col10 = st.columns([2,5])
col9.markdown('You may have observed that the various locations indicated through the various coloured dots appear to be focused in addition to learning which factors are most and least related to life ladder score. I made a globe-shaped choropleth map to better represent the life ladder by area.')
col9.caption('Drag to selected year')
code8 = px.choropleth(merged_table, locations = 'Country name', color = 'Life Ladder', locationmode = 'country names', 
             animation_frame = 'year', category_orders = {'year':np.arange(2005,2022)}, projection = 'orthographic',
             hover_name = "Country name", hover_data = ['Region'],color_continuous_scale= px.colors.sequential.Bluered, width = 800, height = 550
            )
col10.write(code8)
st.subheader('Regional Comparasions')
col11,col12 = st.columns([2,5])
col11.markdown('Box charts are another another tool for comparing locations. In a box plot divided into regions, we may not only look for outliers but also assess happiness by region and compare medians, maximums, and minimums.')
fake_d = pd.DataFrame([['A', 2005, -1, -1, -1, -1, -1, -1, -1, r] for r in ['Southeast Asia',
                                                       'Commonwealth of Independent States', 'Sub-Saharan Africa']], 
                      columns = merged_table.columns)

ani_data = pd.concat([merged_table, fake_d]).sort_values(['year','Region']).reset_index(drop = True)

code9 = px.box(ani_data, y = 'Region', x = 'Life Ladder',hover_name = 'Country name',  
       animation_frame = 'year', category_orders = {'year':np.arange(2005,2022)}, height = 600, width = 850, range_x = [0,9])
col12.write(code9)
col11.caption('(Select year.)')
col11.markdown('We can observe from this box plot that there are just a few outliers—roughly 0–3 every year from 2005–2021. Furthermore, "North America and ANZ" has always been a rather tiny region that has advanced relative to most other regions. This likely indicates the regions nations are generally happy than the majority of other nations in the globe. Additionally, we can observe that Western Europe had a high ladder score between 2005 and 2021, whereas Sub-Saharan Africa and South Asia had very low ladder scores.')


st.subheader('Pltly bar chat')
def by_year(x):
       tempdf = merged_table[merged_table['year'] == x].copy()
       return tempdf.sort_values(by = ['Life Ladder'], ascending= False).head(10).reset_index(drop=True)
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
    temp_fig.update_layout(yaxis = {'tickvals':x.index, 'ticktext':x['Country name']})
    top_10_life_ladder.update({year_num[i]:temp_fig})
col3,col4 = st.columns([2,5])
yearoption = col3.selectbox('Select the year',year_num)
col4.write(top_10_life_ladder[yearoption])
col3.markdown('It was challenging to see how the happiness scores changed over time for both countries from the prior charts. The top 10 nations for each year are shown in this bar graph, which is color-coded by area.')
col3.markdown("This bar graph demonstrates that there was a greater diversity of nations from various areas in the initial years, with 10 countries. But as time goes on, more Western European nations make up the top 10. Nine of the ten nations by 2021 will be in western Europe. The top 10 list is dominated by nations from western Europe, but certain nations, including Israel, Canada, and New Zealand, are still able to make it there, albeit they frequently change positions throughout the years.")


