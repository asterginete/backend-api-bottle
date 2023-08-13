from bottle import Bottle, run, request, response, HTTPError

app = Bottle()

# In-memory storage for items
items = {}

# 1. Create an item
@app.route('/items', method='POST')
def create_item():
    try:
        data = request.json
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
