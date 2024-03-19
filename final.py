import pickle
import requests
import pandas 
import numpy as np
import streamlit as st
with open(r'C:\Users\minmy\md_data_final','rb') as f:
    md_data= pickle.load(f)


with open(r"C:\Users\minmy\cos_final", 'rb') as b:
    cos = pickle.load(b)

md_data[['id_1','id_2','id_3']]=md_data[['id_1','id_2','id_3']].astype(int)
def get_image(x):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(x)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def get_person(x):
    url = "https://api.themoviedb.org/3/person/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(x)
    data = requests.get(url)
    data = data.json()
    poster_path = data['profile_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommending_system(movie):
    image=[]
    a = []
    g = []
    actor_image=[]
    if movie not in md_data['title'].values:
        return "Movie not found"
    
    c = md_data[md_data['title'] == movie].index[0]

    for j, i in enumerate(cos[c]):
        a.append([j, i])
    
    b = sorted(a, reverse=True, key=lambda x: x[1])
    
    for i in b[0:11]:
        image.append(get_image(md_data.loc[i[0],'movie_id']))
        g.append(md_data.loc[i[0], 'title'])
    return g,image

def get_overview(movie_name):
    index=md_data.loc[md_data.title==movie_name,'movie_id'].index[0]
    id=md_data.loc[index,'movie_id']
    
    test=requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US').json()
    
    release_date=test['release_date']
    runtime=test['runtime']
    overview=test['overview']
    for i in test['production_countries']:
        production_country=i['name']
    rating=test['vote_average']
    return release_date,runtime,overview,production_country,rating
st.header('Movie Recommendation system')
select = st.selectbox('select', md_data['title'].values)
if st.button("Show recommendation"):
    selected_movies,selected_image = recommending_system(select)
    to_show_actor=md_data.loc[md_data.title==selected_movies[0],['name_1','id_1','name_2','id_2','name_3','id_3']]
    array=np.array(to_show_actor)
    movie0,movie11=st.columns(2)
    recommend1,recommend2=st.columns(2)

    movie1, movie2, movie3, movie4, movie5 = st.columns(5)
    movie6,movie7,movie8,movie9,movie10=st.columns(5)
    actor_header1,actor_header2=st.columns(2)
    actor1,actor2,actor3=st.columns(3)
    with movie0:
        overview=np.array([get_overview(selected_movies[0])])
        st.text(selected_movies[0])
        st.write(f"""
        <div style="display: flex;">
        <div style="flex: 1;">
            <img src={selected_image[0]} alt="Image" width="600"/>
        </div>
        <div style="padding-left: 50px;">
            <h1>OverView</h1>
            <p1>Release Date-{overview[0][2]}</p1>
        </div>
        </div>""", unsafe_allow_html=True)

        st.text('Released Date-' + overview[0][0])
        st.text('Run Time ' + overview[0][1]+ 'min ')
        st.text(' Production Country ' + overview[0][3])
        st.text(' Rating ' + overview[0][4])
      
    with recommend1:
        st.subheader('Recommending movies')

    with movie1:
        st.text(selected_movies[1])
        st.image(selected_image[1])

    with movie2:
        st.text(selected_movies[2])
        st.image(selected_image[2])

    with movie3:
        st.text(selected_movies[3])
        st.image(selected_image[3])
    with movie4:
        st.text(selected_movies[4])
        st.image(selected_image[4])
    with movie5:
        st.text(selected_movies[5])
        st.image(selected_image[5])
    with movie6:
        st.text(selected_movies[6])
        st.image(selected_image[6])  
    with movie7:
        st.text(selected_movies[7])
        st.image(selected_image[7])  
    with movie8:
        st.text(selected_movies[8])
        st.image(selected_image[8])  
    with movie9:
        st.text(selected_movies[9])
        st.image(selected_image[9])  
    with movie10:
        st.text(selected_movies[10])
        st.image(selected_image[10]) 
    with actor_header1:
        st.header('The actor of ' + selected_movies[0])

    with actor1:
        st.text(array[0][0])
        st.image(get_person(array[0][1]))
    with actor2:
        st.text(array[0][2])
        st.image(get_person(array[0][3]))
    with actor3:
        st.text(array[0][4])
        st.image(get_person(array[0][5]))