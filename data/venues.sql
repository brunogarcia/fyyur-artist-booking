INSERT INTO "venues"(
  name,
  genres,
  address,
  city,
  state,
  phone,
  website,
  facebook_link,
  seeking_talent,
  seeking_description,
  image_link
)
VALUES (
  'The Musical Hop',
  ARRAY['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
  '1015 Folsom Street',
  'San Francisco',
  'CA',
  '123-123-1234',
  'https://www.themusicalhop.com',
  'https://www.facebook.com/TheMusicalHop',
  True,
  'We are on the lookout for a local artist to play every two weeks. Please call us.',
  'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
);

INSERT INTO "venues"(
  name,
  genres,
  address,
  city,
  state,
  phone,
  website,
  facebook_link,
  seeking_talent,
  image_link
)
VALUES (
  'The Dueling Pianos Bar',
  ARRAY['Classical', 'R&B', 'Hip-Hop'],
  '335 Delancey Street',
  'New York',
  'NY',
  '914-003-1132',
  'https://www.theduelingpianos.com',
  'https://www.facebook.com/theduelingpianos',
  False,
  'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
);

INSERT INTO "venues"(
  name,
  genres,
  address,
  city,
  state,
  phone,
  website,
  facebook_link,
  seeking_talent,
  image_link
)
VALUES (
  'Park Square Live Music & Coffee',
  ARRAY['Rock n Roll', 'Jazz', 'Classical', 'Folk'],
  '34 Whiskey Moore Ave',
  'San Francisco',
  'CA',
  '415-000-1234',
  'https://www.parksquarelivemusicandcoffee.com',
  'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
  False,
  'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
);