from starlette import status
from .test_config import client, test_todo, test_user

#-----SUCCESS-----
def test_get_todo_list(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== [{
        "id":1,
        "title":"Learn to code.",
        "description":"Need to learn everyday.",
        "priority":5,
        "completed":False,
        "owner":1,
    }]

def test_get_todo_by_id(test_todo):
    response = client.get("/admin/todo/1")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== {
        "id":1,
        "title":"Learn to code.",
        "description":"Need to learn everyday.",
        "priority":5,
        "completed":False,
        "owner":1,
    }

def test_get_user_list(test_user):
    response = client.get("/admin/user")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== [{
        "id":1,
        "email": "tushar@example.com",
        "username":"tushar",
        "first_name":"tushar",
        "last_name":"jaiswal",
        "hashed_password":"stringstring1",
        "is_active":True,
        "role":"admin"
    }]

def test_get_user_by_id(test_user):
    response = client.get("/admin/user/1")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== {
        "id":1,
        "email": "tushar@example.com",
        "username":"tushar",
        "first_name":"tushar",
        "last_name":"jaiswal",
        "hashed_password":"stringstring1",
        "is_active":True,
        "role":"admin"
    }


#-----EXCEPTIONS-----

# def test_unauthorized_user(test_user):
#     response = client.get("/admin")