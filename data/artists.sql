INSERT INTO "artists"(
  id, 
  name, 
  genres, 
  city, 
  state, 
  phone, 
  website, 
  facebook_link, 
  seeking_venue, 
  seeking_description, 
  image_link 
)
VALUES (
  4,
  'Guns N Petals',
  ARRAY['Rock n Roll'],
  'San Francisco',
  'CA',
  '326-123-5000',
  'https://www.gunsnpetalsband.com',
  'https://www.facebook.com/GunsNPetals',
  True,
  'Looking for shows to perform at in the San Francisco Bay Area!',
  'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
);

INSERT INTO "artists"(
  id, 
  name, 
  genres, 
  city, 
  state, 
  phone,
  facebook_link, 
  seeking_venue, 
  image_link 
)
VALUES (
  5,
  'Matt Quevedo',
  ARRAY['Jazz'],
  'New York',
  'NY',
  '300-400-5000',
  'https://www.facebook.com/mattquevedo923251523',
  False,
  'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
);

INSERT INTO "artists"(
  id, 
  name, 
  genres, 
  city, 
  state, 
  phone, 
  seeking_venue, 
  image_link 
)
VALUES (
  6,
  'The Wild Sax Band',
  ARRAY['Jazz', 'Classical'],
  'San Francisco',
  'CA',
  '432-325-5432',
  False,
  'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
);