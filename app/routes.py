from bottle import Bottle, request, HTTPError

app = Bottle()

# In-memory storage for items
items = {}

def validate_item_name(name):
    if not name or not isinstance(name, str) or len(name) > 100:
        raise HTTPError(400, "Invalid item name. Ensure it's a string and less than 100 characters.")

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

# Additional endpoints remain unchanged...
