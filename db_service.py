import sqlite3
import os
import requests


# Get the database path from an environment variable, or use a default path
DATABASE_DIR = os.environ.get('DATABASE_DIR', '/app')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'reviews.db')


def init():
    # Ensure that the 'orders_data' directory exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    with sqlite3.connect(DATABASE_PATH) as con:

        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    ReviewId INTEGER PRIMARY KEY AUTOINCREMENT,
                    RoomId INTEGER,
                    GuestId INTEGER,
                    Review TEXT,
                    Rating DECIMAL(2,1)
                    )
                ''')
        
        cur.execute('SELECT COUNT(*) FROM reviews')
        row_count = cur.fetchone()[0]
        
        if row_count == 0:
            cur.execute(''' INSERT INTO reviews (RoomId, GuestId, Review, Rating) 
                        VALUES (1, 1, "Great place to stay!", 4.5)
                        ''')
    con.commit()

def read_all():
    with sqlite3.connect(DATABASE_PATH) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews')
        rows = cur.fetchall()

        # TODO: Excange guest ID with guest name from other microservice
        all_reviews = [{'ReviewId': row[0], 'RoomId': row[1], 'GuestId': row[2], 'Review': row[3], 'Rating': row[4]} for row in rows]
        
    
    return all_reviews


def read(id):
    with sqlite3.connect(DATABASE_PATH) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews WHERE ReviewId = ?', (id,))
        row = cur.fetchone()

        # /guests/id GET
        # TODO: Change request URL when guest microservice is ready
        guest_response = requests.get('http://guests:5000/guests/' + str(row[2]))

        if row is None:
            return None

        review = {'ReviewId': row[0], 'RoomId': row[1], 'Guest': guest_response.json()['name'], 'Review': row[3], 'Rating': row[4]}



    return review


def create(review):
    # Review should be a dictionary
    with sqlite3.connect(DATABASE_PATH) as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO reviews (RoomId, GuestId, Review, Rating) 
                    VALUES (:roomid,:guestid,:review,:rating)''', review)
    con.commit()

    return True
