# Movie Watchlist
A Flask web application that allows users to create and manage a watchlist of movies. It has the following functionality:

- User registration
- Login
- Viewing and adding movies to the user's watchlist
- Logout

The application uses a MongoDB database to store the user data and movie information. The routes for the application are defined in the Flask Blueprint "pages". The templates for the pages are stored in the "templates" folder and the static files (e.g. CSS, images) are stored in the "static" folder. The application uses the following modules and libraries:

- Flask
- functools
- uuid
- datetime
- dataclasses
- passlib
- MongoDB (pymongo)

The user's password is hashed using the pbkdf2_sha256 algorithm from the passlib library before being stored in the database. A user must be logged in to access the main page, which displays the movies in their watchlist. Access to routes that require login is managed using a login_required decorator.
