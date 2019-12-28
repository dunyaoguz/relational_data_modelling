import os
import glob
import psycopg2
import pandas as pd
import json
from sql_queries import *

def process_song_file(cur, filepath):
    """
    For a given JSON file from the songs dataset, extracts information on the song and the artist, and loads it on the songs and artists tables.
    """
    # open song file
    with open(filepath) as file:
        song_dict = json.load(file)

    # insert song record
    song_data = {k:v for (k,v) in song_dict.items() if k in ['song_id', 'title', 'artist_id', 'year', 'duration']}
    try:
        cur.execute(song_table_insert, list(song_data.values()))
    except:
        t = song_data['title']
        print(f'Could not insert {t} due to unique constraint of the primary key song_id')

    # insert artist record
    artist_data = {k:v for (k,v) in song_dict.items() if k in ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']}
    try:
        cur.execute(artist_table_insert, list(artist_data.values()))
    except:
        t = artist_data['artist_name']
        print(f'Could not insert {t} due to unique constraint of the primary key artist_id')

def process_log_file(cur, filepath):
    """
    For a given JSON file from the logs dataset, extracts information on the time, user and the songplay activity, and load it on the time, users and songplays tables.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'])

    # insert time data records
    time_data = [list(df.ts), list(df.ts.dt.hour), list(df.ts.dt.day), list(df.ts.dt.week), list(df.ts.dt.month), list(df.ts.dt.year)]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year']
    time_df = pd.DataFrame({c:d for c, d in zip(column_labels, time_data)})

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except:
            print(f'Could not insert time data {row.start_time} due to unique constraint of the primary key start_time')

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except:
            print(f'Could not insert user with user_id {row.userId} due to unique constraint of the primary key user_id')

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Finds all the files in the directories, and processes each one through the two functions above. 
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=dunya port=5432")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
