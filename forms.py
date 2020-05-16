from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, \
    DateTimeField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL, Length, Regexp, \
    AnyOf, ValidationError
from enums import State, Genre

# Custom validators
# https://wtforms.readthedocs.io/en/stable/validators/#custom-validators


def validate_genres(genres):
    def _validate(form, field):
        error = False

        for value in field.data:
            if value not in genres:
                error = True

        if error:
            raise ValidationError('Not valid option')

    return _validate


#  Show Form
#  ----------------------------------------------------------------


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


#  Venue Form
#  ----------------------------------------------------------------


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            AnyOf([item.value for item in State])
        ],
        choices=State.items()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone',
        validators=[Regexp(
            r'^[0-9\-\+]+$', 0,
            message='The phone must be valid'
        )]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(),
            validate_genres([item.value for item in Genre])
        ],
        choices=Genre.items()
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = TextAreaField(
        'seeking_description', validators=[Length(min=10, max=500)]
    )


#  Artirts Form
#  ----------------------------------------------------------------


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            AnyOf([item.value for item in State])
        ],
        choices=State.items()
    )
    phone = StringField(
        'phone',
        validators=[Regexp(
            r'^[0-9\-\+]+$', 0,
            message='The phone must be valid'
        )]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(),
            validate_genres([item.value for item in Genre])
        ],
        choices=Genre.items()
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_venue = BooleanField(
        'seeking_venue',
    )
    seeking_description = TextAreaField(
        'seeking_description', validators=[Length(min=10, max=500)]
    )
