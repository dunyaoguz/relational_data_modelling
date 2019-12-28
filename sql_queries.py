# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY,
                                                                  start_time timestamp NOT NULL,
                                                                  user_id int NOT NULL,
                                                                  level varchar NOT NULL,
                                                                  song_id varchar NOT NULL,
                                                                  artist_id varchar NOT NULL,
                                                                  session_id int NOT NULL,
                                                                  location varchar,
                                                                  user_agent varchar)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users  (user_id int PRIMARY KEY NOT NULL,
                                                           first_name varchar,
                                                           last_name varchar,
                                                           gender varchar,
                                                           level varchar)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY NOT NULL,
                                                          title varchar,
                                                          artist_id varchar NOT NULL,
                                                          year int,
                                                          duration int)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY NOT NULL,
                                                              name varchar,
                                                              location varchar,
                                                              latitude int,
                                                              longitude int)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp PRIMARY KEY NOT NULL,
                                                         hour int,
                                                         day int,
                                                         week int,
                                                         month int,
                                                         year int)
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT
                            DO NOTHING;
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT
                        DO NOTHING;
""")

song_table_insert = ("""INSERT INTO songs (artist_id, song_id, title, duration, year)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT
                        DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, latitude, longitude, location, name)
                          VALUES (%s, %s, %s, %s, %s)
                          ON CONFLICT
                          DO NOTHING;
""")


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT
                        DO NOTHING;
""")

# FIND SONGS

song_select = ("""SELECT s.song_id
, s.artist_id
FROM songs AS s
JOIN artists AS a
ON s.artist_id = a.artist_id
WHERE s.title = (%s)
AND a.name = (%s)
AND s.duration = (%s)
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
