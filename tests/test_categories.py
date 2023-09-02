def test_create_category(client, init_database):
    response = client.post('/categories', json={
        'name': 'Test Category',
        'description': 'This is a test category'
    })
    assert response.status_code == 200
    assert b'Category created successfully!' in response.data

def test_create_existing_category(client, init_database):
    # Create a category first
    client.post('/categories', json={
        'name': 'Test Category 2',
        'description': 'This is another test category'
    })
    # Try creating again
    response = client.post('/categories', json={
        'name': 'Test Category 2',
        'description': 'Trying to create an existing category'
    })
    assert response.status_code == 400
    assert b'Category already exists' in response.data

def test_get_existing_category(client, init_database):
    # Create a category first
    client.post('/categories', json={
        'name': 'Test Category 3',
        'description': 'This is yet another test category'
    })
    response = client.get('/categories/3')
    assert response.status_code == 200
    assert b'Test Category 3' in response.data

def test_get_nonexistent_category(client, init_database):
    response = client.get('/categories/9999')
    assert response.status_code == 404
    assert b'Category not found' in response.data

def test_update_existing_category(client, init_database):
    # Create a category first
    client.post('/categories', json={
        'name': 'Test Category 4',
        'description': 'This is one more test category'
    })
    response = client.put('/categories/4', json={
        'name': 'Updated Category 4',
        'description': 'This is an updated test category'
    })
    assert response.status_code == 200
    assert b'Category updated successfully!' in response.data

def test_update_nonexistent_category(client, init_database):
    response = client.put('/categories/9999', json={
        'name': 'Nonexistent Category',
        'description': 'Trying to update a nonexistent category'
    })
    assert response.status_code == 404
    assert b'Category not found' in response.data

def test_delete_existing_category(client, init_database):
    # Create a category first
    client.post('/categories', json={
        'name': 'Test Category 5',
        'description': 'This is the last test category'
    })
    response = client.delete('/categories/5')
    assert response.status_code == 200
    assert b'Category deleted successfully!' in response.data

def test_delete_nonexistent_category(client, init_database):
    response = client.delete('/categories/9999')
    assert response.status_code == 404
    assert b'Category not found' in response.data
