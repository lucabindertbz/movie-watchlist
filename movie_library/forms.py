# Import FlaskForm class from the flask_wtf library
from flask_wtf import FlaskForm

# Import various field types and validators from the wtforms library
from wtforms import (
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
)
from wtforms.validators import (
    InputRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
)


# Define LoginForm class as a subclass of FlaskForm
class LoginForm(FlaskForm):
    # Define email field with a label "Email" and validators InputRequired and Email
    email = StringField("Email", validators=[InputRequired(), Email()])
    # Define password field with a label "Password" and validator InputRequired
    password = PasswordField("Password", validators=[InputRequired()])
    # Define submit button with a label "Login"
    submit = SubmitField("Login")


# Define RegisterForm class as a subclass of FlaskForm
class RegisterForm(FlaskForm):
    # Define email field with a label "Email" and validators InputRequired and Email
    email = StringField("Email", validators=[InputRequired(), Email()])
    # Define password field with a label "Password" and validators InputRequired and Length
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=4,
                max=20,
                message="Your password must be between 4 and 20 characters long.",
            ),
        ],
    )
    # Define confirm_password field with a label "Confirm Password" and validators InputRequired and EqualTo
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password",
                message="This password did not match the one in the password field.",
            ),
        ],
    )
    # Define submit button with a label "Register"
    submit = SubmitField("Register")


# Define MovieForm class as a subclass of FlaskForm
class MovieForm(FlaskForm):
    # Define title field with a label "Title" and validator InputRequired
    title = StringField("Title", validators=[InputRequired()])
    # Define director field with a label "Director" and validator InputRequired
    director = StringField("Director", validators=[InputRequired()])
    # Define year field with a label "Year" and validators InputRequired and NumberRange
    year = IntegerField(
        "Year",
        validators=[
            InputRequired(),
            NumberRange(min=1878, message="Please enter a year in the format YYYY."),
        ],
    )
    # Define submit button with a label "Add Movie"
    submit = SubmitField("Add Movie")


# Class definition for `StringListField` which is a subclass of `TextAreaField`.
class StringListField(TextAreaField):
    # Method to convert the data stored in `self.data` into a string representation.
    # Returns a string that is a concatenation of the elements in `self.data` separated by line breaks.
    def _value(self):
        # If there is data stored in `self.data`.
        if self.data:
            # Return a string that is a concatenation of the elements in `self.data` separated by line breaks.
            return "\n".join(self.data)
        # If there is no data stored in `self.data`.
        else:
            # Return an empty string.
            return ""

    # Method to process the data passed in `valuelist` and store it in `self.data`.
    def process_formdata(self, valuelist):
        # If `valuelist` is a non-empty list and the first element of `valuelist`
        # is not falsy (i.e. not an empty string).
        if valuelist and valuelist[0]:
            # Split the first element of `valuelist` by line breaks and strip whitespace from each line.
            # Store the resulting list of strings in `self.data`.
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        # If `valuelist` is an empty list or the first element of `valuelist` is falsy.
        else:
            # Store an empty list in `self.data`.
            self.data = []


# Class definition for `ExtendedMovieForm` which is a subclass of `MovieForm`.
class ExtendedMovieForm(MovieForm):
    # Class-level attribute representing a `StringListField` for the "Cast" data.
    cast = StringListField("Cast")
    # Class-level attribute representing a `StringListField` for the "Series" data.
    series = StringListField("Series")
    # Class-level attribute representing a `StringListField` for the "Tags" data.
    tags = StringListField("Tags")
    # Class-level attribute representing a `TextAreaField` for the "Description" data.
    description = TextAreaField("Description")
    # Class-level attribute representing a `URLField` for the "Video link" data.
    video_link = URLField("Video link")

    # Class-level attribute representing a `SubmitField` for the form submission button.
    submit = SubmitField("Submit")
