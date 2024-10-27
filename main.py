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

# Create a review
@app.route('/reviews', methods=['POST'])
def create_review():
    review = request.get_json()

    # Check if the guest already reviewed this room
    

    db_service.create(review)
    return 'Review created', 201

if __name__ == '__main__':
    db_service.init()  # Ensure the database is initialized before running
    app.run(host='0.0.0.0')

    