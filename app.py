import streamlit as st
import pickle as pk
import requests
import webbrowser

movies_list1 = pk.load(open('movies.pkl','rb'))
similarity = pk.load(open('similarity.pkl','rb'))
movies_list = movies_list1['title'].values




def searched_movie_info(movie_id):
     url = requests.get('https://api.themoviedb.org/3/movie/{'
                  '}?api_key=8f751536f063e2d20775c864233e80b1&language=en-US'.format(movie_id))
     data = url.json()
     poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
     genre = data['genres']
     genre = ", ".join([ x['name'] for x in genre ])
     # url2 = requests.get('https://imdb-api.com/en/API/Title/k_h74l1sul/{''}/Ratings'.format(data['imdb_id']))
     # data1 = url2.json()
     tmdb_rating = data['vote_average']
     total_votes = data['vote_count']
     total_votes = "{:,}".format(int(total_votes))


     col1, col2 = st.columns([1,2])
     with col1:
          st.image(poster)

     with col2:
          st.subheader(data['title'])
          st.caption(f"Genre: {genre}")
          st.caption(f"Release Date: {data['release_date']}")
          st.markdown(data['overview'])
          st.write('\n')
          st.success(f"TMDb Ratings: **{tmdb_rating}** out of **_{total_votes}_** votes")
          speak = '<p style="font-family:verdana; color:blue; font-size: 15px;">Click for more info</p>'

          link = f'[{speak}](https://www.themoviedb.org/movie/{movie_id})'
          st.markdown(link, unsafe_allow_html=True)



def fetch_poster(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{'
                  '}?api_key=8f751536f063e2d20775c864233e80b1&language=en-US'.format(movie_id))
     data = response.json()
     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie, value):
     movie_index = movies_list1[movies_list1['title'] == movie].index[0]
     distances = similarity[movie_index]
     movies_list_recom = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:value+1]
     recommended_movies = []
     recommended_posters = []


     for i in movies_list_recom:
          movie_id = movies_list1.iloc[i[0]].movie_id
          recommended_posters.append(fetch_poster(movie_id))
          recommended_movies.append(movies_list1.iloc[i[0]].title)

     return recommended_movies, recommended_posters

# st.title('Movie Recommender System')

st.markdown("<h1 style='text-align: center; color: red;'>Movie Recommender System</h1>", unsafe_allow_html=True)
st.write("\n")

selected_option = st.selectbox(
     'List of 5000 TMDB movies',
     (movies_list))

value = st.slider(
     'Select a range of recommending movies',
     1, 10,)


if st.button('Recommend'):

     st.write("\n")

     movie_id = movies_list1[movies_list1['title'] == selected_option].iat[0, 0]
     searched_movie_info(movie_id)

     names,posters = recommend(selected_option, value)

     st.write("\n")
     st.write("\n")
     st.write("\n")
     st.write("\n")
     st.write("\n")
     st.write("\n")
     st.subheader('Top {} recommended movies for you:'.format(value))
     cols = st.columns(len(st.columns(value)))
     count=0

     for i in cols:
          with i:
               movie_id_tmdb = movies_list1[movies_list1['title'] == names[count]].iat[0, 0]
               link = f'[{names[count]}](https://www.themoviedb.org/movie/{movie_id_tmdb})'
               st.markdown(link, unsafe_allow_html=True)
               # st.markdown(names[count])
               st.image(posters[count], use_column_width=True)
               count += 1
