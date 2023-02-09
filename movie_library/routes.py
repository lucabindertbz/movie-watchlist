# This code defines a Flask Blueprint to create a web application for movie watchlist.
# It contains routes for registering a new user, logging in, viewing and adding movies to the user's watchlist, and
# logging out.

# Importing necessary modules
import functools
import uuid
import datetime
from dataclasses import asdict
from flask import Blueprint, current_app, flash, redirect, render_template, session, url_for, request, app
# Importing form and model classes from the movie_library module
from movie_library.forms import LoginForm, RegisterForm, MovieForm, ExtendedMovieForm
from movie_library.models import User, Movie
# Importing the password hashing library
from passlib.hash import pbkdf2_sha256

# Creating a Blueprint object for the pages module
# The "pages" blueprint will use the templates and static folders in the same directory as this file
pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


# Defining a decorator for routes that require login
def login_required(route):
    # Wrapping the original route with the additional functionality to check for a valid login
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            # If there is no email in the session, redirect to the login page
            return redirect(url_for(".login"))
        # If the email is in the session, call the original route
        # elif # check if user is in database with email and if not session destroy and then redirect to login
        else:
            return route(*args, **kwargs)

    return route_wrapper


# Route for the main page, requires login
@pages.route("/")
@login_required
def index():
    # Fetch the user data from the database using the email stored in the session
    user_data = current_app.db.user.find_one({"email": session["email"]})
    # Create a User object from the fetched data
    user = User(**user_data)

    # Fetch the movie data
    movie_data = current_app.db.movie.find({"_id": {"$in": user.movies}})
    movies = [Movie(**movie) for movie in movie_data]

    # Render the index template with the title and the list of movies
    return render_template(
        "index.html",
        title="Movies Watchlist",
        movies_data=movies,
    )


# Route for registering a new user
@pages.route("/register", methods=["POST", "GET"])
def register():
    # Redirect to the main page if the user is already logged in
    if session.get("email"):
        return redirect(url_for(".index"))

    # Create a form object for registering a new user
    form = RegisterForm()

    if form.validate_on_submit():  # Check if the form has been submitted and all required fields are valid
        # Create a new User object with the form data
        user = User(
            _id=uuid.uuid4().hex,  # Generate a unique identifier for the user using UUID
            email=form.email.data,  # Get the email from the form data
            password=pbkdf2_sha256.hash(form.password.data),  # Hash the password using pbkdf2_sha256
        )
        # Insert the user object into the "user" collection in the database
        current_app.db.user.insert_one(asdict(user))

        # Display a success message to the user
        flash("User registered successfully", "success")

        # Redirect the user to the login page
        return redirect(url_for(".login"))

    # If the form is not valid or has not been submitted yet, render the register template
    return render_template(
        "register.html", title="Movies Watchlist - Register", form=form
    )


# This is a Flask route for handling the login functionality
@pages.route("/login", methods=["GET", "POST"])
def login():
    # If a user is already logged in, redirect them to the index page
    if session.get("email"):
        return redirect(url_for(".index"))

    # Create a form instance for handling login credentials
    form = LoginForm()

    # If the form is submitted and passes validation
    if form.validate_on_submit():
        # Search for the user in the database
        user_data = current_app.db.user.find_one({"email": form.email.data})
        # If the user is not found, display an error message
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))

        # Create a user object from the data retrieved from the database
        user = User(**user_data)

        # Verify the user password
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            # Store the user ID and email in the session
            session["user_id"] = user._id
            session["email"] = user.email

            # Redirect the user to the index page
            return redirect(url_for(".index"))

        # If the password is incorrect, display an error message
        flash("Login credentials not correct", category="danger")

    # Render the login template
    return render_template("login.html", title="Movies Watchlist - Login", form=form)


# This is a Flask route for adding a new movie

@pages.route("/add", methods=["GET", "POST"])
# Require a user to be logged in to access this route
@login_required
def add_movie():
    # Create a form instance for adding movie information
    form = MovieForm()

    # If the form is submitted and passes validation
    if form.validate_on_submit():
        # Create a movie object from the form data
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
        )

        # Insert the movie into the database
        current_app.db.movie.insert_one(asdict(movie))

        # Add the movie to the list of movies for the current user
        current_app.db.user.update_one(
            {"_id": session["user_id"]}, {"$push": {"movies": movie._id}}
        )

        # Redirect the user to the movie's detail page
        return redirect(url_for(".movie", _id=movie._id))

    # Render the template for adding a new movie
    return render_template(
        "new_movie.html", title="Movies Watchlist - Add Movie", form=form
    )


# This is a Flask route for logging out a user

@pages.route("/logout/")
def logout():
    # Save the current theme, so it can be restored after the session is cleared
    current_theme = session.get("theme")

    # Clear the session data
    session.clear()

    # Restore the current theme to the session
    session["theme"] = current_theme

    # Redirect the user to the login page
    return redirect(url_for(".login"))


# This is a Flask route for displaying movie details

@pages.get("/movie/<string:_id>")
def movie(_id: str):
    # Retrieve the movie data from the database
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))

    # Render the template for displaying movie details
    return render_template("movie_details.html", movie=movie)


# This is a Flask route for editing a movie

@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required
def edit_movie(_id: str):
    # Retrieve the movie data from the database
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))

    # Create an instance of the extended movie form with the movie data
    form = ExtendedMovieForm(obj=movie)

    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # Update the movie data with the form data
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.cast = form.cast.data
        movie.series = form.series.data
        movie.tags = form.tags.data
        movie.description = form.description.data
        movie.video_link = form.video_link.data

        # Update the movie data in the database
        current_app.db.movie.update_one({"_id": movie._id}, {"$set": asdict(movie)})

        # Redirect the user to the movie details page
        return redirect(url_for(".movie", _id=movie._id))

    # Render the template for the movie form with the movie data and form
    # If the form has not been submitted or is not valid, the function renders the "movie_form.html" template
    # with the movie data and form, allowing the user to edit the movie details.
    return render_template("movie_form.html", movie=movie, form=form)


# Route to set when you watched a movie
@pages.get("/movie/<string:_id>/watch")
@login_required  # User must be logged in to access this route
def watch_today(_id):
    # Update the movie document in the database to set the last_watched field to the current date
    current_app.db.movie.update_one(
        {"_id": _id}, {"$set": {"last_watched": datetime.datetime.today()}}
    )

    # Redirect to the movie page
    return redirect(url_for(".movie", _id=_id))


# Route to rate a movie
@pages.get("/movie/<string:_id>/rate")  # This route is triggered on a GET request to the endpoint "/movie/<_id>/rate"
@login_required  # Require that the user is logged in to access this route
def rate_movie(_id):  # The view function takes a single argument, the movie _id
    # Get the rating value from the query parameters of the GET request
    # The view function, named rate_movie, takes a single argument _id, which is a string passed as a part of the URL.
    # The <string:_id> syntax in the route is a template variable, and it tells Flask to capture the value of the string
    # that appears in that position in the URL and pass it to the view function as an argument.
    rating = int(request.args.get("rating"))

    # Update the movie document in the database with the matching _id
    current_app.db.movie.update_one({"_id": _id}, {"$set": {"rating": rating}})

    # Redirect the user to the movie page for the movie with the given _id
    return redirect(url_for(".movie", _id=_id))


# Route to toggle the theme
@pages.get("/toggle-theme")
def toggle_theme():
    # Get the current theme from the session
    current_theme = session.get("theme")
    # If the theme is currently "dark", set it to "light"
    if current_theme == "dark":
        session["theme"] = "light"
    # Otherwise, set it to "dark"
    else:
        session["theme"] = "dark"

    # Redirect to the current page
    return redirect(request.args.get("current_page"))

# @app.errorhandler(404)
# def page_not_found(error):
#     # Renders the 404.html template and returns a 404 status code
#     return render_template("404.html"), 404
