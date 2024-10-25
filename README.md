# ka-reviews
API for Kong Athurs Hotels værelsesreviews

```
docker build -t ka-reviews
```

```
docker run --rm -p 5003:5000 --name -ka-reviews -d ka-reviews
```

## API Endpoints
### Se alle Reviews
 - **URL** `/reviews`
 - **Method**: `GET`
 - **Response**
    - **200 OK**: Returns all reviews
