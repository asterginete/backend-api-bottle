from bottle import Bottle, run, request, response, HTTPError
import jwt
import bcrypt

app = Bottle()

# In-memory storage for items
items = {}
users = {}

SECRET_KEY = "your_secret_key_here"  # This should be kept secret and stored securely

def validate_item_name(name):
    if not name or not isinstance(name, str) or len(name) > 100:
        raise HTTPError(400, "Invalid item name. Ensure it's a string and less than 100 characters.")

# User registration
@app.route('/register', method='POST')
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if user already exists
    if username in users:
        raise HTTPError(400, "User already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users[username] = {
        'username': username,
        'password': hashed_password.decode('utf-8')
    }

    return {"message": "User registered successfully"}

# User login
@app.route('/login', method='POST')
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)

    if not user:
        raise HTTPError(401, "Invalid credentials")

    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # Generate JWT token
        token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
        return {"token": token}
    else:
        raise HTTPError(401, "Invalid credentials")

# JWT Middleware
@hook('before_request')
def check_authentication():
    # Exclude login and register routes from authentication check
    if request.path in ['/login', '/register']:
        return

    token = request.headers.get('Authorization')
    if not token:
        raise HTTPError(401, "Token missing")

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        request.user = decoded_token.get('username')
    except jwt.ExpiredSignatureError:
        raise HTTPError(401, "Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPError(401, "Invalid token")

# 1. Create an item
@app.route('/items', method='POST')
def create_item():
    try:
        data = request.json
        validate_item_name(data['name'])
        item_id = str(len(items) + 1)
        items[item_id] = data['name']
        return {"id": item_id, "name": data['name']}
    except:
        raise HTTPError(400, "Invalid data")

# 2. Get all items
@app.route('/items', method='GET')
def get_all_items():
    return items

# 3. Get a specific item by ID
@app.route('/items/<item_id>', method='GET')
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        raise HTTPError(404, "Item not found")
    return {"id": item_id, "name": item}

# 4. Update an item by ID
@app.route('/items/<item_id>', method='PUT')
def update_item(item_id):
    if item_id not in items:
        raise HTTPError(404, "Item not found")
    try:
        data = request.json
        validate_item_name(data['name'])
        items[item_id] = data['name']
        return {"id": item_id, "name": data['name']}
    except:
        raise HTTPError(400, "Invalid data")

# 5. Delete an item by ID
@app.route('/items/<item_id>', method='DELETE')
def delete_item(item_id):
    if item_id not in items:
        raise HTTPError(404, "Item not found")
    del items[item_id]
    return {"message": "Item deleted successfully"}

# 6. Get the count of items
@app.route('/items/count', method='GET')
def count_items():
    return {"count": len(items)}

# 7. Check if an item exists by name
@app.route('/items/exists/<name>', method='GET')
def item_exists(name):
    if name in items.values():
        return {"exists": True}
    return {"exists": False}

# 8. Clear all items
@app.route('/items/clear', method='DELETE')
def clear_items():
    items.clear()
    return {"message": "All items cleared"}

# 9. Get the first item
@app.route('/items/first', method='GET')
def get_first_item():
    if not items:
        raise HTTPError(404, "No items found")
    first_key = list(items.keys())[0]
    return {"id": first_key, "name": items[first_key]}

# 10. Get the last item
@app.route('/items/last', method='GET')
def get_last_item():
    if not items:
        raise HTTPError(404, "No items found")
    last_key = list(items.keys())[-1]
    return {"id": last_key, "name": items[last_key]}

if __name__ == '__main__':
    run(app, host='localhost', port=8080)
