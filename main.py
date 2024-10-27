import db_service, requests
from flask import Flask, jsonify, request

db_service.init()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Reviews service'

# Get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    
    return jsonify(db_service.read_all()), 200

# Get single review
@app.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = db_service.read(id)
    if review is None:
        return 'Review not found', 404
    return jsonify(review), 200


# Not public
# Get all reviews for a room
@app.route('/reviews/room/<int:room_id>', methods=['GET'])
def get_reviews_by_room(room_id):
    
    # check if room exists
    room = requests.get('http://ka-rooms:5000/rooms/' + str(room_id))
    if room.status_code != 200:
        return 'Room not found', 404

    reviews = db_service.read_by_room(room_id)
    return jsonify(reviews), 200

# Not public
# get all reviews for a guest
@app.route('/reviews/guest/<int:guest_id>', methods=['GET'])
def get_reviews_by_guest(guest_id):
    # check if guest exists
    guest = requests.get('http://ka-guests:5000/guests/' + str(guest_id))
    if guest.status_code != 200:
        return 'Guest not found', 404
    
    reviews = db_service.read_by_guest(guest_id)
    return jsonify(reviews), 200

# Create a review
@app.route('/reviews', methods=['POST'])
def create_review():
    review = request.get_json()

    # check if room exists
    room = requests.get('http://ka-rooms:5000/rooms/' + str(review['RoomId']))
    if room.status_code != 200:
        return 'Room not found', 404
    
    # check if guest exists
    guest = requests.get('http://ka-guests:5000/guests/' + str(review['GuestId']))
    if guest.status_code != 200:
        return 'Guest not found', 404
    
    # Check if the guest already reviewed this room
    reviews_for_room = db_service.read_by_room(review['RoomId'])
    for r in reviews_for_room:
        if r['GuestId'] == review['GuestId']:
            return 'Guest already reviewed this room', 400


    db_service.create(review)
    return 'Review created', 201

if __name__ == '__main__':
    db_service.init()  # Ensure the database is initialized before running
    app.run(host='0.0.0.0')

    