# MyCandidate API Documentation

## Endpoints

### GET /api/v1/wards/{ward_id}/candidates

Retrieves all candidates standing for election in the specified ward.

#### Parameters

- `ward_id` (integer, path parameter): The unique identifier of the ward

#### Response

**Success (200 OK)**
```json
{
  "ward_id": 1,
  "ward_name": "Ward 1",
  "candidates": [
    {
      "id": 1,
      "name": "Someone Awesome",
      "party": "Democratic Party",
      "age": 45,
      "occupation": "Developer"
    },
    {
      "id": 2,
      "name": "Someone Better",
      "party": "Republican Party",
      "age": 38,
      "occupation": "Engineer"
    }
  ]
}
```

**Error Responses**

- **404 Not Found**: Ward with specified ID does not exist
```json
{
  "error": "Ward not found"
}
```

- **500 Internal Server Error**: Server error
```json
{
  "error": "Internal server error"
}
```

#### Example Usage

```bash
curl -X GET http://localhost:5000/api/v1/wards/1/candidates

{
  "ward_id": 1,
  "ward_name": "Central Ward",
  "candidates": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "party": "Progressive Party",
      "age": 42,
      "occupation": "Community Organizer"
    }
  ]
}
```

## Testing

Run the API tests with:
```bash
pytest tests/test_api.py -v
```