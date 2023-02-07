# import necessary modules
import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

# import blueprint for routes
from movie_library.routes import pages

# load environment variables from .env file
load_dotenv()


# function to create Flask application
def create_app():
    # create Flask app
    app = Flask(__name__)

    # set environment variables for the database URI and secret key
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw")

    # connect to MongoDB database using the URI and get the default database
    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

    # register blueprint for routes
    app.register_blueprint(pages)

    # return the Flask app
    return app
