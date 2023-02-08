from dataclasses import dataclass, field
from datetime import datetime


# Define the Movie dataclass
@dataclass
class Movie:
    # Unique identifier for the movie
    _id: str
    # Title of the movie
    title: str
    # Director of the movie
    director: str
    # Year the movie was released
    year: int
    # List of actors in the movie
    cast: list[str] = field(default_factory=list)
    # List of series the movie belongs to
    series: list[str] = field(default_factory=list)
    # The date the movie was last watched
    last_watched: datetime = None
    # User-assigned rating for the movie
    rating: int = 0
    # List of tags to categorize the movie
    tags: list[str] = field(default_factory=list)
    # A brief description of the movie
    description: str = None
    # Link to the video for the movie
    video_link: str = None


# Define the User dataclass
@dataclass
class User:
    # Unique identifier for the user
    _id: str
    # Email address of the user
    email: str
    # Hashed password for the user
    password: str
    # List of movies in the user's watchlist
    movies: list[str] = field(default_factory=list)
