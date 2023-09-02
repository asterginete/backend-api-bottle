def test_register_new_user(client, init_database):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'User registered successfully!' in response.data

def test_register_existing_user(client, init_database):
    # Register the user once
    client.post('/register', json={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password123'
    })
    # Try registering again
    response = client.post('/register', json={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'Username already exists' in response.data

def test_login_valid_user(client, init_database):
    # Register the user first
    client.post('/register', json={
        'username': 'testuser3',
        'email': 'test3@example.com',
        'password': 'password123'
    })
    # Now, try logging in
    response = client.post('/login', json={
        'username': 'testuser3',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data

def test_login_invalid_user(client, init_database):
    response = client.post('/login', json={
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data

def test_login_wrong_password(client, init_database):
    # Register the user first
    client.post('/register', json={
        'username': 'testuser4',
        'email': 'test4@example.com',
        'password': 'password123'
    })
    # Now, try logging in with wrong password
    response = client.post('/login', json={
        'username': 'testuser4',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data
