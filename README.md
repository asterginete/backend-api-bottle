# CRUD Application with Bottle Framework

This application provides a simple backend CRUD functionality using the Bottle framework. It covers user authentication, item management, category management, comments, and notifications.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/asterginete/backend-api-bottle.git
    cd backend-api-bottle
    ```

2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python run.py initdb
    ```

5. **Run the application**:
    ```bash
    python run.py
    ```

## Usage

Once the application is running, you can access it at `http://localhost:8080`.

## API Endpoints

### Authentication

- **Register**: `POST /auth/register`
- **Login**: `POST /auth/login`
- **Request Password Reset**: `POST /auth/request-password-reset`
- **Reset Password**: `POST /auth/reset-password/<token>`
- **Get Profile**: `GET /auth/profile`
- **Update Profile**: `PUT /auth/profile`

### Items

- **List All Items**: `GET /items/`
- **Get Single Item**: `GET /items/<item_id>`
- **Create Item**: `POST /items/`
- **Update Item**: `PUT /items/<item_id>`
- **Delete Item**: `DELETE /items/<item_id>`

### Categories

- **List All Categories**: `GET /categories/`
- **Get Single Category**: `GET /categories/<category_id>`
- **Create Category**: `POST /categories/`
- **Update Category**: `PUT /categories/<category_id>`
- **Delete Category**: `DELETE /categories/<category_id>`

### Comments

- **List All Comments for an Item**: `GET /comments/item/<item_id>`
- **Create Comment**: `POST /comments/`
- **Update Comment**: `PUT /comments/<comment_id>`
- **Delete Comment**: `DELETE /comments/<comment_id>`

### Notifications

- **List All Notifications**: `GET /notifications/`
- **Mark Notification as Read**: `PUT /notifications/<notification_id>/read`
- **Delete Notification**: `DELETE /notifications/<notification_id>`

## Features

- User registration and authentication
- Password reset functionality
- CRUD operations for items
- CRUD operations for categories
- Commenting on items
- Notifications for users
- Image upload for items
- Email notifications
- Pagination support
- Search functionality
- Filtering and sorting of items
- User profiles with avatars
- Rate limiting for API requests
- Detailed logging

## Testing

Tests are written using `pytest`. To run the tests:

```bash
pytest tests/
```

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes and write tests.
4. Commit your changes.
5. Push to your branch.
6. Create a pull request.

## License

This project is licensed under the MIT License.
