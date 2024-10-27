import sqlite3, logging
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

# Read one review by ID
def read(id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews WHERE ReviewId = ?', (id,))
        row = cur.fetchone()

        guest_response = requests.get('http://ka-guests:5000/guests/' + str(row[2]))
        
        if row is None:
            return None

        review = {'ReviewId': row[0], 'RoomId': row[1], 'Guest': guest_response.json()['name'], 'Review': row[3], 'Rating': row[4]}

    return review

# Get all reviews for a room by room ID
def read_by_room(room_id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews WHERE RoomId = ?', (room_id,))
        rows = cur.fetchall()

        guests = requests.get('http://ka-guests:5000/guests').json()

        def get_guest_name(guest_id):
            for guest in guests:
                if guest['guestId'] == guest_id:
                    return guest['name']
            return 'Guest not found'
        

        all_reviews = [{'ReviewId': row[0], 'RoomId': row[1], 'GuestId': row[2], 'Review': row[3], 'Rating': row[4]} for row in rows]

    return all_reviews  

# Get all reviews for a guest by guest ID  
def read_by_guest(guest_id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM reviews WHERE GuestId = ?', (guest_id,))
        rows = cur.fetchall()

        res_url = 'http://ka-guests:5000/guests/' + str(guest_id)
        guest = requests.get(res_url).json()



        all_reviews = [{'ReviewId': row[0], 'RoomId': row[1], 'GuestName': guest['name'], 'Review': row[3], 'Rating': row[4]} for row in rows]

    return all_reviews


def create(review):
    # Review should be a dictionary
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO reviews (RoomId, GuestId, Review, Rating) 
                    VALUES (:RoomId,:GuestId,:Review,:Rating)''', review)
    con.commit()

    return True
