#improting required libraries
import numpy as np
import pandas as pd
import pickle
from flask import Flask, render_template, request

# unpickling and loading data and similarity matrix

saved_data = open('saved_data.pickle', 'rb')
data = pickle.load(saved_data)
saved_data.close()

similarity_matrix = open('similarity_matrix.pickle', 'rb')
similarity = pickle.load(similarity_matrix)
similarity_matrix.close()


#function returning 5 similar movies
def similar_movies(m):
    m = m.lower()
    
    if m not in data.movie_title.unique():
        return ('string')
    else:
        index = data.loc[data.movie_title == m].index[0]
        movie_list = list(enumerate(similarity[index]))
        movie_list = sorted(movie_list, key = lambda x : x[1], reverse = True)
        movie_list = movie_list[1:10]
        
        final_list = []
        for i in range(len(movie_list)):
            a = movie_list[i][0]
            final_list.append(data.movie_title[a])
        return final_list
    
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend')
def recommend():
    movie = request.args.get('movie')
    movies = similar_movies(movie)
    movie = movie.upper()
    
    if type(movies) == type('string'):
        return render_template('recommend.html', movie = movie, r = movies, t = 'unavailable' )
    
    else:
        return render_template('recommend.html', movie = movie, r = movies, t = 'final_list')
    
if __name__ == '__main__':
    app.run()