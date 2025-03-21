## URL shortener

Run it locally
```bash
docker compose up --build
```

Tests
```bash
./backend/command.sh test
```

## API Documentation

### Create Short URL
- **Endpoint**: `POST /api/urls/`
- **Description**: Create a new shortened URL
- **Request Body**:
  ```json
  {
    "url": "https://example.com"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "original_url": "https://example.com",
    "short_code": "abc123",
    "short_url": "http://localhost:8000/api/urls/abc123",
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Rate Limiting**: Throttled with "url_create" scope

### Retrieve URL Info
- **Endpoint**: `GET /api/urls/{short_code}/`
- **Description**: Retrieve information about a shortened URL
- **Parameters**: short_code (in path)
- **Response**: 200 OK
  ```json
  {
    "original_url": "https://example.com",
    "short_code": "abc123",
    "short_url": "http://localhost:8000/api/urls/abc123",
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Caching**: Responses are cached for 24 hours
- **Rate Limiting**: Throttled with "url_retrieve" scope

Note: All API endpoints support trailing slash as optional.