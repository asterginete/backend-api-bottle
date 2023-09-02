/backend-api-bottle
|-- /app
|   |-- /models
|   |   |-- __init__.py
|   |   |-- user.py
|   |   |-- item.py
|   |   |-- category.py
|   |   |-- image.py
|   |   |-- comment.py
|   |   |-- notification.py
|   |
|   |-- /routes
|   |   |-- __init__.py
|   |   |-- auth_routes.py
|   |   |-- item_routes.py
|   |   |-- category_routes.py
|   |   |-- comment_routes.py
|   |   |-- notification_routes.py
|   |
|   |-- /services
|   |   |-- __init__.py
|   |   |-- email_service.py
|   |   |-- image_upload_service.py
|   |
|   |-- /static
|   |   |-- /images
|   |
|   |
|   |-- __init__.py
|   |-- config.py (For configurations like DB connection, email settings, etc.)
|   |-- utils.py (For utility functions like password hashing, token generation, etc.)
|
|
|-- /tests
|   |-- conftest.py
|   |-- test_auth.py
|   |-- test_items.py
|   |-- test_categories.py
|
|-- README.md
|-- requirements.txt
|-- run.py
