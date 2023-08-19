# Bottle CRUD Application with Authentication

This is a simple backend application built using the Bottle framework that provides CRUD (Create, Read, Update, Delete) functionality for managing a list of items. Additionally, it features user registration, login, and JWT-based authentication.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Testing](#testing)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install the required packages**:
   ```bash
   pip install bottle jwt bcrypt
   ```

## Usage

To start the server, run:

```bash
python app.py
```

The server will start on `localhost` at port `8080`.

## Authentication

### User Registration

- **URL**: `/register`
- **Method**: `POST`
- **Data**: `{"username": "your_username", "password": "your_password"}`

### User Login

- **URL**: `/login`
- **Method**: `POST`
- **Data**: `{"username": "your_username", "password": "your_password"}`

After logging in, the returned JWT token must be included in the `Authorization` header of subsequent requests to access protected endpoints.

## Endpoints

### 1. Create an item

- **URL**: `/items`
- **Method**: `POST`
- **Data**: `{"name": "item_name"}`

### 2. Get all items

- **URL**: `/items`
- **Method**: `GET`

### 3. Get a specific item by ID

- **URL**: `/items/<item_id>`
- **Method**: `GET`

### 4. Update an item by ID

- **URL**: `/items/<item_id>`
- **Method**: `PUT`
- **Data**: `{"name": "new_item_name"}`

### 5. Delete an item by ID

- **URL**: `/items/<item_id>`
- **Method**: `DELETE`

### 6. Get the count of items

- **URL**: `/items/count`
- **Method**: `GET`

### 7. Check if an item exists by name

- **URL**: `/items/exists/<name>`
- **Method**: `GET`

### 8. Clear all items

- **URL**: `/items/clear`
- **Method**: `DELETE`

### 9. Get the first item

- **URL**: `/items/first`
- **Method**: `GET`

### 10. Get the last item

- **URL**: `/items/last`
- **Method**: `GET`

## Testing

You can use tools like `curl` or Postman to test the endpoints. For example, to create a new item:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Sample Item"}' http://localhost:8080/items
```

To register a new user:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}' http://localhost:8080/register
```

To login and get a JWT token:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}' http://localhost:8080/login
```
