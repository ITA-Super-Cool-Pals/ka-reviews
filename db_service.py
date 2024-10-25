import sqlite3
import os
import requests



db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app-db', 'reviews.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)


def init():
    # Ensure that the 'orders_data' directory exists


    with sqlite3.connect(db_path) as con:

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
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews')
        rows = cur.fetchall()

        # TODO: Excange guest ID with guest name from other microservice
        all_reviews = [{'ReviewId': row[0], 'RoomId': row[1], 'GuestId': row[2], 'Review': row[3], 'Rating': row[4]} for row in rows]
        
    
    return all_reviews

# Read one revieew
def read(id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews WHERE ReviewId = ?', (id,))
        row = cur.fetchone()

        guest_response = requests.get('http://ka-guests:5003/guests/1') #+ str(row[2]))

        if row is None:
            return None

        review = {'ReviewId': row[0], 'RoomId': row[1], 'Guest': 'test', 'Review': row[3], 'Rating': row[4]}

    return review


def create(review):
    # Review should be a dictionary
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO reviews (RoomId, GuestId, Review, Rating) 
                    VALUES (:roomid,:guestid,:review,:rating)''', review)
    con.commit()

    return True
