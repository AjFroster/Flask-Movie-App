from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

import requests

# App setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap5(app)

# DataBase setup
db = SQLAlchemy(app)





class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    ranking = db.Column(db.Integer, default=0, nullable=False)
    review = db.Column(db.String(250), default='', nullable=False)
    img_url = db.Column(db.String(500), default='', nullable=False)


class RateMovieForm(FlaskForm):
    rating = FloatField('Your Rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit')    


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


# Function to add dummy data to the database
def add_dummy_movies():
    with app.app_context():
        movies_data =  [
    {
        "title": "The Dark Knight",
        "year": 2008,
        "description": "A caped crusader defends Gotham City from the menacing Joker.",
        "rating": 9.0,
        "ranking": 1,
        "review": "A masterpiece of superhero cinema.",
        "img_url": "https://example.com/dark_knight.jpg"
    },
    {
        "title": "Inception",
        "year": 2010,
        "description": "A thief enters the dreams of others to steal their secrets.",
        "rating": 8.8,
        "ranking": 2,
        "review": "Mind-bending and visually stunning.",
        "img_url": "https://example.com/inception.jpg"
    },
    {
        "title": "Avengers: Endgame",
        "year": 2019,
        "description": "The Avengers assemble one last time to defeat Thanos.",
        "rating": 8.4,
        "ranking": 3,
        "review": "Epic conclusion to the Marvel saga.",
        "img_url": "https://example.com/endgame.jpg"
    },
    {
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "description": "A post-apocalyptic road warrior battles tyrants in the wasteland.",
        "rating": 8.1,
        "ranking": 4,
        "review": "A relentless, high-octane thrill ride.",
        "img_url": "https://example.com/mad_max.jpg"
    },
    {
        "title": "The Social Network",
        "year": 2010,
        "description": "The story of the creation of Facebook and the legal battles that followed.",
        "rating": 7.7,
        "ranking": 5,
        "review": "Compelling portrayal of tech entrepreneurship.",
        "img_url": "https://example.com/social_network.jpg"
    },
    {
        "title": "Get Out",
        "year": 2017,
        "description": "A young African American man visits his white girlfriend's family estate and uncovers dark secrets.",
        "rating": 7.7,
        "ranking": 6,
        "review": "A thought-provoking and suspenseful horror-thriller.",
        "img_url": "https://example.com/get_out.jpg"
    },
    {
        "title": "The Revenant",
        "year": 2015,
        "description": "A frontiersman on a fur trading expedition in the 1820s fights for survival.",
        "rating": 8.0,
        "ranking": 7,
        "review": "Visually stunning and intense.",
        "img_url": "https://example.com/revenant.jpg"
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "description": "A group of astronauts embarks on a journey through a wormhole to save humanity.",
        "rating": 8.6,
        "ranking": 8,
        "review": "A mind-bending space epic.",
        "img_url": "https://example.com/interstellar.jpg"
    },
    {
        "title": "Joker",
        "year": 2019,
        "description": "A mentally troubled comedian becomes a criminal mastermind.",
        "rating": 8.4,
        "ranking": 9,
        "review": "A dark and disturbing character study.",
        "img_url": "https://example.com/joker.jpg"
    },
    {
        "title": "La La Land",
        "year": 2016,
        "description": "A jazz musician and an aspiring actress fall in love in Los Angeles.",
        "rating": 8.0,
        "ranking": 10,
        "review": "A dazzling and enchanting musical.",
        "img_url": "https://example.com/la_la_land.jpg"
    }
]

        for movie_data in movies_data:
            movie = Movie(**movie_data)
            db.session.add(movie)

        db.session.commit()
        

with app.app_context():
    db.session.query(Movie).delete()
    db.session.commit()



@app.route("/")
def home():
    # Retrieve movies from the database and sort by rating
    movies = Movie.query.order_by(Movie.rating.desc()).limit(10).all()
    
    # Assign rankings to the sorted movies
    for index, movie in enumerate(movies, start=1):
        movie.ranking = index

    return render_template('index.html', movies=movies)


@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    form = RateMovieForm()
    movie = Movie.query.get(movie_id)

    if form.validate_on_submit():
        # Process the form data, e.g., update movie rating and review
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=form, movie=movie)


@app.route('/delete/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(movie_id):
    # Fetch the movie by its ID
    movie_to_delete = Movie.query.get(movie_id)

    if movie_to_delete:
        # If the movie exists, delete it from the database
        db.session.delete(movie_to_delete)
        db.session.commit()

    # Redirect to the home page after deletion
    return redirect(url_for('home'))


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = FindMovieForm()

    if form.validate_on_submit():
        search_query = form.title.data  
        # Movie API Credentials
        API_KEY = 'b3cfdfe0f5957c343b3016aa841504e6'  
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}")
        # print(response.json()['results'])
        if response.status_code == 200:
            search_results = response.json()['results']
            return render_template('select.html', form=form, movies=search_results)
        else:
            # Handle errors or no results
            return render_template('add.html', form=form, error='No results found')

    return render_template('add.html', form=form)


@app.route("/select", methods=["GET", "POST"])
def select_movie():
    if request.method == "POST":
        # Step 1: Get the selected movie's ID from the form submission
        selected_movie_id = int(request.form["movie_selection"])
        
        # Step 2: Make an API request to get movie details
        api_key = 'b3cfdfe0f5957c343b3016aa841504e6'
        api_url = f'https://api.themoviedb.org/3/movie/{selected_movie_id}?api_key={api_key}'
        response = requests.get(api_url)
        movie_data = response.json()

        # Step 3: Extract properties from API response
        print(f"movie_data = {movie_data}")
        title = movie_data['title']
        
        img_url = f'https://image.tmdb.org/t/p/w500/{movie_data["poster_path"]}'  # Construct the complete poster image URL
        year = movie_data['release_date'][:4]  # Extract the year from the release date
        description = movie_data['overview']

        # Step 4: Create a new Movie object and add it to the database
        new_movie = Movie(title=title, img_url=img_url, year=year, description=description)
        db.session.add(new_movie)
        db.session.commit()

        # Step 5: Redirect to the home page
        return redirect(url_for('home'))

    # If it's a GET request, render the select.html template with the movie options
    movies = Movie.query.all()  # Replace with your query to retrieve all movies
    return render_template('select.html', movies=movies)


if __name__ == '__main__':
    print("Running Top 10 Movies")

    # add_dummy_movies()
    # Run application
    app.run(debug=True)
