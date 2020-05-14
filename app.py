# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import sys
import babel
import logging
import dateutil.parser
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from forms import VenueForm, ArtistForm, ShowForm
from flask import Flask, render_template, request, flash, redirect, \
  url_for, abort

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(
      db.Integer,
      db.ForeignKey('Venue.id'),
      nullable=False,
    )
    artist_id = db.Column(
      db.Integer,
      db.ForeignKey('Artist.id'),
      nullable=False,
    )
    start_time = db.Column(
      db.DateTime,
      nullable=False,
    )


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref="venue", lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref="artist", lazy=True)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # data = [{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }

    data = []

    # Get areas
    areas = Venue.query.with_entities(Venue.city, Venue.state).all()

    # Get city and state
    for city, state in dict(areas).items():
        venues = Venue.query \
          .with_entities(Venue.id, Venue.name) \
          .filter(Venue.city == city) \
          .filter(Venue.state == state) \
          .all()

        # Map data
        data.append({
          'city': city,
          'state': state,
          'venues': venues
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # response = {
    #   "count": 1,
    #   "data": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }
    # Get search data
    search_term = request.form['search_term']
    search = "%{}%".format(search_term)

    # Search venues
    response = Venue.query \
        .with_entities(Venue.id, Venue.name) \
        .filter(Venue.name.match(search)) \
        .all()

    # Map data
    results = {
        'data': response,
        'count': len(response)
    }

    return render_template(
      'pages/search_venues.html',
      results=results,
      search_term=search_term
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1 = {
    #   "past_shows": [{
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }

    data = Venue.query.filter(Venue.id == venue_id).first()
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False

    # Get data
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']

    try:
        # Create model
        venue = Venue(
          name=name,
          city=city,
          state=state,
          address=address,
          phone=phone,
          genres=genres,
          image_link=image_link,
          facebook_link=facebook_link,
          website=website,
          seeking_talent=seeking_talent,
          seeking_description=seeking_description,
        )

        # Update DB
        db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    # Show banner
    if error:
        abort(400)
        flash(
          'An error occurred. Venue '
          + name
          + ' could not be listed.',
          'danger'
        )
    if not error:
        flash(
          'Venue '
          + name
          + ' was successfully listed!',
          'success'
        )

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.

    # BONUS CHALLENGE:
    # Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it
    # from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query \
      .with_entities(Artist.id, Artist.name) \
      .order_by('id') \
      .all()

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # response = {
    #   "count": 1,
    #   "data": [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "num_upcoming_shows": 0,
    #   }]
    # }
    # Get search data
    search_term = request.form['search_term']
    search = "%{}%".format(search_term)

    # Search artist
    response = Artist.query \
        .with_entities(Artist.id, Artist.name) \
        .filter(Artist.name.match(search)) \
        .all()

    # Map data
    results = {
        'data': response,
        'count': len(response)
    }

    return render_template(
      'pages/search_artists.html',
      results=results,
      search_term=search_term
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1 = {
    #   "past_shows": [{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }

    data = Artist.query.filter(Artist.id == artist_id).first()
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # Request artist data
    artist = Artist.query.filter(Artist.id == artist_id).first()

    # Fill artist form
    form = ArtistForm()
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False

    # Get data
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']

    try:
        # Request artist by id
        artist = Artist.query.get(artist_id)

        # Update artist data
        artist.name = name
        artist.city = city
        artist.state = state
        artist.phone = phone
        artist.genres = genres
        artist.image_link = image_link
        artist.facebook_link = facebook_link
        artist.website = website
        artist.seeking_talent = seeking_talent
        artist.seeking_description = seeking_description

        # Update DB
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(400)
        flash(
          'An error occurred. Artist '
          + name
          + ' could not be updated.',
          'danger'
        )
    if not error:
        flash(
          'Artist '
          + name
          + ' was successfully updated!',
          'success'
        )

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # Request venue data
    venue = Venue.query.filter(Venue.id == venue_id).first()

    # Fill venue form
    form = VenueForm()
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.website.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False

    # Get data
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']

    try:
        # Request venue by id
        venue = Venue.query.get(venue_id)

        # Update venue data
        venue.name = name
        venue.city = city
        venue.state = state
        venue.address = address
        venue.phone = phone
        venue.genres = genres
        venue.image_link = image_link
        venue.facebook_link = facebook_link
        venue.website = website
        venue.seeking_talent = seeking_talent
        venue.seeking_description = seeking_description

        # Update DB
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    # Show banner
    if error:
        abort(400)
        flash(
          'An error occurred. Venue '
          + name
          + ' could not be updated.',
          'danger'
        )
    if not error:
        flash(
          'Venue '
          + name
          + ' was successfully updated!',
          'success'
        )

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False

    # Get data
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_venue = True if 'seeking_venue' in request.form else False
    seeking_description = request.form['seeking_description']

    try:
        # Create model
        artist = Artist(
          name=name,
          city=city,
          state=state,
          phone=phone,
          genres=genres,
          image_link=image_link,
          facebook_link=facebook_link,
          website=website,
          seeking_venue=seeking_venue,
          seeking_description=seeking_description,
        )

        # Update DB
        db.session.add(artist)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    # Show banner
    if error:
        abort(400)
        flash(
          'An error occurred. Artist '
          + name
          + ' could not be listed.',
          'danger'
        )
    if not error:
        flash(
          'Artist '
          + name
          + ' was successfully listed!',
          'success'
        )

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []

    # Get data
    shows = db.session \
        .query(
          Venue.name,
          Artist.name,
          Artist.image_link,
          Show.venue_id,
          Show.artist_id,
          Show.start_time
        ) \
        .filter(Venue.id == Show.venue_id, Artist.id == Show.artist_id)

    # Map data
    for show in shows:
        data.append({
          'venue_name': show[0],
          'artist_name': show[1],
          'artist_image_link': show[2],
          'venue_id': show[3],
          'artist_id': show[4],
          'start_time': str(show[5])
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET'])
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False

    # Get data
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    try:
        # Create model
        show = Show(
          artist_id=artist_id,
          venue_id=venue_id,
          start_time=start_time,
        )

        # Update DB
        db.session.add(show)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    # Show banner
    if error:
        abort(400)
        flash(
          'An error occurred. Show could not be listed.',
          'danger'
        )
    if not error:
        flash(
          'Show was successfully listed!',
          'success'
        )

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
          '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
