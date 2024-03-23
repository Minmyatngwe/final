import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import pickle
from datetime import datetime, time
import plotly.express as px
import plotly.graph_objects as go

with open(r"movie_data_plotting",'rb')as f:

      data= pickle.load(f)

data.Year=data.Year.astype(int)
data.Released=pd.to_datetime(data.Released)
start_date=pd.to_datetime(data.Released).min()

end_date=pd.to_datetime(data.Released).max()
st.subheader('Movie production by countries')

date1, date2 = st.columns((2))

plot1, plot2 = st.columns((2))
plot_column, pie_plot_column = st.columns((2))

with date1:
      selected_date1=st.date_input('Starting Date',start_date)
with date2:
      selected_date2=st.date_input('Ending Date',end_date)


selected_datetime1 = datetime.combine(selected_date1, time.min)
selected_datetime2 = datetime.combine(selected_date2, time.max)


df = data[(data["Released"] >= selected_datetime1) & (data["Released"] <= selected_datetime2)]
if st.button('Show Plot'):
        with plot_column:
            st.subheader('Top 10 movie production countries')
            counted_values=df.Country.value_counts()[:10]
          
            fig= px.bar(x=counted_values.index,y=counted_values)
            fig.update_xaxes(title_text='Country')
            fig.update_yaxes(title_text='Number of Movies')
            fig.update_layout(width=900,height=600)
            st.plotly_chart(fig,use_container_width=False)
selected_country = st.selectbox("Select the country", data.Country.unique())
md_selected_country = data.loc[data['Country'] == selected_country]
selected_country_df = pd.DataFrame(md_selected_country.groupby('Genre')['imdbRating'].mean())
selected_country_df.reset_index(inplace=True)
selected_rows = selected_country_df.iloc[[0, 1,2, -1, -2,-3]]
st.subheader('Average rating of genres')


if st.button('Show Genre-wise Ratings'):
    st.subheader(f'Genre-wise average rating for {selected_country}')
    fig1 = px.bar(x=selected_rows['Genre'], y=selected_rows['imdbRating'])

    fig1.update_layout(width=900,height=600)


    st.plotly_chart(fig1)
movie_by_year=data.groupby('Year')['Type'].count()
st.subheader('Movie production by year')
fig3=px.line(movie_by_year[-15:])
fig3.update_layout(width=900,height=600)

st.plotly_chart(fig3)



language=data.groupby('Language')['Language'].count().sort_values(ascending=False)
st.header('Languages')
fig4=px.pie(values=language[:5],names=language[:5].index)
fig4.update_layout(width=900,height=600)

st.plotly_chart(fig4)
