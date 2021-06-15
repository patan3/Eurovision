import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from pylab import *

st.set_page_config(page_title='Eurovision 2021 Explorer ', page_icon=':flag-eu:', layout='wide', initial_sidebar_state='auto')

st.markdown('# Eurovision 2021 Explorer\n This web application illustrates several interactive graphs of the Eurovision 2021.\n Python and Streamlit are used, data is scraped from [Wikipedia](https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2021) and pre-processed with Pandas and NumPy.')
st.markdown('You can choose your country of interest and the vote type at any time by using the widgets in the sidebar.')
st.markdown('Moreover, you can set how to display the web app, either in one or two columns depending on which device you are using.')
columns = st.radio('Number of Columns', ['1', '2'])

st.markdown('## **Plots**')
st.markdown('- **Bar Plots**: display the Total and Jury/Televoting score for a certain amount of countries depending on your choice, \n - **Map Plots**: display the Jury/Televoting votes for a particular country depending on your choice. Please note that some countries (e.g., Cyprus, Israel, etc.) do not fit into the map. Please refer to the Sankey Diagrams if you are curious about them. \n - **Sankey Diagrams**: display the Jury/Televoting votes for a particular country depending on your choice, \n - **Raw Data**: display the raw data before and after data pre-processing.')

st.sidebar.markdown('# Select Type of Vote')
vote = st.sidebar.radio('Type of Vote', ['Jury', 'Televoting'])

if vote == 'Televoting':
    boole = True
elif vote == 'Jury':
    boole = False

@st.cache
def load_data(boole):
    if boole == True:
        data = pd.read_csv(r'https://raw.githubusercontent.com/patan3/Eurovision/main/df_televoting.csv')
    else:
        data = pd.read_csv(r'https://raw.githubusercontent.com/patan3/Eurovision/main/df_jury.csv')
    return data


data = load_data(boole)

df_votes = load_data(True)
df_votes = df_votes.iloc[:, 0:3].copy()
df_votes['Televoting score'] = df_votes['Total score'] - pd.to_numeric(df_votes['Jury score'])



    
#st.header('Select Contestant')
st.sidebar.markdown('# Select Contestant')
nation = st.sidebar.selectbox('Contestant', data['Contestant'])

st.sidebar.markdown(" # About the Author ")
st.sidebar.markdown("Angelo Patane'  \n angelpatane9@gmail.com")
st.sidebar.markdown("[Linkedin](https://www.linkedin.com/in/angelopatane/)    \n [Twitter](https://twitter.com/angel_patane3)")


df_televoting_backup = data.copy()
data = data[data['Contestant'] == nation]



#st.dataframe(data.iloc[:, 3:].style.highlight_max(axis=1))



how_many = st.slider('How many contestants to display in the bar plots?', min_value = 10, max_value = 26)

#%% LAYOUT
if columns == '2':
    col1, col2 = st.beta_columns(2)

#%% Barplot1

fig01 = px.bar(df_votes.sort_values(by = 'Total score', ascending = False)[0:how_many], y='Total score', x='Contestant', text='Total score', color='Total score', color_continuous_scale=px.colors.sequential.YlOrRd,
            template = 'plotly_white', height = 550)
fig01.update_traces(textposition='outside')

if columns == '2':
    col1.subheader('Total score of the first '+ str(how_many) +' contestants')
    col1.plotly_chart(fig01, use_container_width=True)
else:
    st.subheader('Total score of the first '+ str(how_many) +' contestants')
    st.plotly_chart(fig01, use_container_width=True)
    
fig02 = px.bar(df_votes.sort_values(by = vote + ' score', ascending = False)[0:how_many], y= vote + ' score', x='Contestant', text=vote + ' score', color=vote + ' score', color_continuous_scale=px.colors.sequential.YlOrRd,
            template = 'plotly_white', height = 550)
fig02.update_traces(textposition='outside')
if columns == '2':
    col2.subheader(vote +' score of the first '+ str(how_many) +' contestants')
    col2.plotly_chart(fig02, use_container_width=True)
else:
    st.subheader(vote +' score of the first '+ str(how_many) +' contestants')
    st.plotly_chart(fig02, use_container_width=True)


#%% Map 1
df_televoting = data.copy()
df_Contestant_tele = df_televoting.loc[df_televoting['Contestant'] == nation]
df_Contestant_tele = df_Contestant_tele.set_index('Contestant').T[2:]
df_Contestant = df_Contestant_tele.reset_index().rename(columns = {'index': 'Country'}).copy()
df_Contestant['Vote'] = pd.to_numeric(df_Contestant[nation], errors ='coerce')


fig = px.choropleth(df_Contestant, locations='Country', locationmode="country names", color = 'Vote', 
                    scope="europe",
                    hover_name = 'Country',
                    hover_data = ['Vote'],
                    color_continuous_scale=px.colors.sequential.YlOrRd)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# fig.show()

if columns == '2':
    col1.subheader('Map of {Vote} score for {Country}'.format(Vote = vote, Country = nation))
    col1.plotly_chart(fig, use_container_width=True)
else:
    st.subheader('Map of {Vote} score for {Country}'.format(Vote = vote, Country = nation))
    st.plotly_chart(fig, use_container_width=True)
#st.subheader('Map of {Vote} Votes for {Country}'.format(Vote = vote, Country = nation))
#st.plotly_chart(fig, use_container_width=True)

#%% Map 2
df_televoting_2 = df_televoting_backup.copy()
df_Contestant_tele_gives = df_televoting_2[['Contestant', nation]].copy()
df_Contestant_tele_gives['Vote'] = pd.to_numeric(df_Contestant_tele_gives[nation], errors ='coerce')


fig2 = px.choropleth(df_Contestant_tele_gives, locations='Contestant', locationmode="country names", color= 'Vote', 
                    scope="europe",
                    hover_name = 'Contestant',
                    hover_data = ['Vote'],
                    color_continuous_scale=px.colors.sequential.YlOrRd)
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

if columns == '2':
    col2.subheader('Map of {Vote} score from {Country}'.format(Vote = vote, Country = nation))
    col2.plotly_chart(fig2, use_container_width=True)
else:
    st.subheader('Map of {Vote} score from {Country}'.format(Vote = vote, Country = nation))
    st.plotly_chart(fig2, use_container_width=True)
#st.subheader('Map of {Vote} Votes from {Country}'.format(Vote = vote, Country = nation))
#st.plotly_chart(fig2, use_container_width=True)

#%% Sankey from Country

# Import
df_chord = df_televoting_backup.drop(df_televoting_backup.columns[[1, 2]], axis = 1).copy()
df_chord = df_chord.sort_values('Contestant')
df_chord = df_chord.reindex(sorted(df_chord.columns), axis=1)
df_chord = df_chord.set_index('Contestant')
names = df_chord.columns.tolist()

## Preprocessing ##
msource = []
mtarget = []
mvalue = []
for column in df_chord.columns:
    
    df_column = df_chord[column].reset_index()
    df_column = df_column[df_column[column].notnull()]
    
    for index, row in df_column.iterrows():
        msource.append(df_chord.columns.get_loc(column))
        mtarget.append(df_chord.columns.get_loc(row['Contestant']))
        mvalue.append(int(row[column]))

## Get Colors ##
# See https://matplotlib.org/stable/tutorials/colors/colormaps.html for other palettes
# cmap = cm.get_cmap('Set3', 10)    # PiYG
# color_links = []
# for i in range(cmap.N):
#     rgba = cmap(i)
#     # rgb2hex accepts rgb or rgba
#     color_links.append(matplotlib.colors.rgb2hex(rgba))

## Plot ##
index_nation = df_chord.columns.get_loc(nation)
fig3 = go.Figure(data=[go.Sankey(
    node = dict(
      label = names,
      color = "blue"
    ),
    link = dict(
      source = msource[index_nation*10:index_nation*10+10], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = mtarget[index_nation*10:index_nation*10+10],
      value = mvalue[index_nation*10:index_nation*10+10]
      #color = color_links
  ))])

# fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
#col2.subheader('Sankey Diagram of {Vote} Votes from {Country}'.format(Vote = vote, Country = nation))
#col2.plotly_chart(fig3, use_container_width=True)


#%% Sankey for Country

## Preprocessing ##
msource_rec = []
mtarget_rec = []
mvalue_rec = []
mcountry_rec = []
for column in df_chord.index:
    
    df_column_rec = df_chord.loc[column].reset_index()
    df_column_rec = df_column_rec[df_column_rec[column].notnull()]
    
    for index, row in df_column_rec.iterrows():
        mcountry_rec.append(column)
        msource_rec.append(df_chord.columns.get_loc(row['index']))
        mtarget_rec.append(df_chord.columns.get_loc(column))
        mvalue_rec.append(int(row[column]))

## Plot ##
if nation in list(set(mcountry_rec)):
    ind_min = min([index for index,value in enumerate(mcountry_rec) if value == nation])
    ind_max = max([index for index,value in enumerate(mcountry_rec) if value == nation])
    
    fig4 = go.Figure(data=[go.Sankey(
        node = dict(
          label = names,
          color = 'blue'
        ),
        link = dict(
          source = msource_rec[ind_min:ind_max+1], # indices correspond to labels, eg A1, A2, A1, B1, ...
          target = mtarget_rec[ind_min:ind_max+1],
          value = mvalue_rec[ind_min:ind_max+1]
      ))])
    
    #st.subheader('Sankey Diagram of {Vote} Votes for {Country}'.format(Vote = vote, Country = nation))
    #st.plotly_chart(fig4, use_container_width=True)
    
    #st.subheader('Sankey Diagram of {Vote} Votes from {Country}'.format(Vote = vote, Country = nation))
    #st.plotly_chart(fig3, use_container_width=True)
    
    if columns == '2':
        col1.subheader('Sankey Diagram of {Vote} score for {Country}'.format(Vote = vote, Country = nation))
        col1.plotly_chart(fig4, use_container_width=True)
    
        col2.subheader('Sankey Diagram of {Vote} score from {Country}'.format(Vote = vote, Country = nation))
        col2.plotly_chart(fig3, use_container_width=True)
    else:
        st.subheader('Sankey Diagram of {Vote} score for {Country}'.format(Vote = vote, Country = nation))
        st.plotly_chart(fig4, use_container_width=True)
    
        st.subheader('Sankey Diagram of {Vote} score from {Country}'.format(Vote = vote, Country = nation))
        st.plotly_chart(fig3, use_container_width=True)
    
else:
    #st.subheader('Sankey Diagram of {Vote} Votes for {Country}'.format(Vote = vote, Country = nation))
    #st.warning('{Nation} received 0 {Vote} Votes.'.format(Nation = nation, Vote = vote))
    
    #st.subheader('Sankey Diagram of {Vote} Votes from {Country}'.format(Vote = vote, Country = nation))
    #st.plotly_chart(fig3, use_container_width=True)
    
    if columns == '2':
        col1.subheader('Sankey Diagram of {Vote} score for {Country}'.format(Vote = vote, Country = nation))
        col1.warning('{Nation} received 0 {Vote} score.'.format(Nation = nation, Vote = vote))
        
        col2.subheader('Sankey Diagram of {Vote} score from {Country}'.format(Vote = vote, Country = nation))
        col2.plotly_chart(fig3, use_container_width=True)
    else:
        st.subheader('Sankey Diagram of {Vote} score for {Country}'.format(Vote = vote, Country = nation))
        st.warning('{Nation} received 0 {Vote} score.'.format(Nation = nation, Vote = vote))
        
        st.subheader('Sankey Diagram of {Vote} score from {Country}'.format(Vote = vote, Country = nation))
        st.plotly_chart(fig3, use_container_width=True)
        
#%%
if st.checkbox('Raw  %s Data for All Contestants' % vote):
    st.subheader('Raw %s Data for All Contestants' % vote)
    st.write(df_televoting_backup)
    
if st.checkbox('Raw  {Vote} Data for {Country}'.format(Vote = vote, Country = nation)):
    st.subheader('Raw {Vote} Data for {Country}'.format(Vote = vote, Country = nation))
    st.write(data)
    
    st.subheader('Raw {Vote} Data from {Country}'.format(Vote = vote, Country = nation))
    st.write(df_televoting_backup[['Contestant', nation]])
