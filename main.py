import db_service
from flask import Flask, jsonify

db_service.init()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

# Get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    
    return jsonify(db_service.read_all()), 200

if __name__ == '__main__':
    db_service.init()  # Ensure the database is initialized before running
    app.run(host='0.0.0.0', port=5000)

    