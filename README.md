# ka-reviews
API for Kong Athurs Hotels værelsesreviews

```
docker build -t ka-reviews
```

```
docker run --rm -p 5003:5000 -v /path/to/db/dir:/app/app-db --name -ka-reviews -d ka-reviews
```

## API Endpoints
### Se alle Reviews
 - **URL:** `/reviews`
 - **Method**: `GET`
 - **Response**
    - **200 OK**: Returns all reviews


### Se enkelt Review
   - **URL** `/reviews/<review id>`
   - **Method:** `GET`
   - **Response**
      - **200 OK:** Returns chosen review
      - **404 Not Found:** Review id not found


### Lav et nyt review
   - **URL:** `/reviews`
   - **MEthod:** `POST`
   - **Request Body:**
   ```
   {
    "RoomId": room_id,
    "GuestId": guest_id,
    "Review": "Review body",
    "Rating": rating
   }
   ```
   Rating is a ``double`` value 
   - **Response:**
      - **201 OK:** Review created
      - **404 Not Found:** Room- or Guest ID not found
      - **400 Bad Request:** Guest Already reviewed the room


## For internal use
### Get all reviews for a room
- **URL:** `/reviews/room/<room id>`
   - **Method:** `GET`
   - **Response**
      - **200 OK:** Returns chosen reviews
      - **404 Not Found:** Room id not found

### Get all reviews for a room
- **URL:** `/reviews/guest/<guest id>`
   - **Method:** `GET`
   - **Response**
      - **200 OK:** Returns chosen reviews
      - **404 Not Found:** Guest id not found