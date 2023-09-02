def test_create_item(client, init_database):
    # Assuming a user and category have been created for this test
    response = client.post('/items', json={
        'name': 'Test Item',
        'description': 'This is a test item',
        'category_id': 1
    })
    assert response.status_code == 200
    assert b'Item created successfully!' in response.data

def test_get_existing_item(client, init_database):
    # Create an item first
    client.post('/items', json={
        'name': 'Test Item 2',
        'description': 'This is another test item',
        'category_id': 1
    })
    response = client.get('/items/2')
    assert response.status_code == 200
    assert b'Test Item 2' in response.data

def test_get_nonexistent_item(client, init_database):
    response = client.get('/items/9999')
    assert response.status_code == 404
    assert b'Item not found' in response.data

def test_update_existing_item(client, init_database):
    # Create an item first
    client.post('/items', json={
        'name': 'Test Item 3',
        'description': 'This is yet another test item',
        'category_id': 1
    })
    response = client.put('/items/3', json={
        'name': 'Updated Item 3',
        'description': 'This is an updated test item'
    })
    assert response.status_code == 200
    assert b'Item updated successfully!' in response.data

def test_update_nonexistent_item(client, init_database):
    response = client.put('/items/9999', json={
        'name': 'Nonexistent Item',
        'description': 'Trying to update a nonexistent item'
    })
    assert response.status_code == 404
    assert b'Item not found' in response.data

def test_delete_existing_item(client, init_database):
    # Create an item first
    client.post('/items', json={
        'name': 'Test Item 4',
        'description': 'This is one more test item',
        'category_id': 1
    })
    response = client.delete('/items/4')
    assert response.status_code == 200
    assert b'Item deleted successfully!' in response.data

def test_delete_nonexistent_item(client, init_database):
    response = client.delete('/items/9999')
    assert response.status_code == 404
    assert b'Item not found' in response.data
