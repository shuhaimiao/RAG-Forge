# API Best Practices

This document outlines the best practices for designing and implementing APIs.

## Authentication

All API endpoints must be protected by OAuth 2.0. API keys should be passed in the `Authorization` header.

## Versioning

API versions should be included in the URL, for example: `/api/v1/users`.

## Error Handling

APIs should return standard HTTP status codes. Error responses should be in JSON format with a clear error message.

Example:
```json
{
  "error": "Invalid API key"
}
```

## Pagination

For endpoints that return a list of items, pagination should be implemented using `limit` and `offset` query parameters. 