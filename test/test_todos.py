from starlette import status
from .test_config import client, test_todo

def test_todo_page_redirects_to_login_without_access_token():
	response = client.get("/todo/todo-page", follow_redirects=False)

	assert response.status_code == status.HTTP_302_FOUND
	assert response.headers["location"] == "/auth/login-page"
	assert "access_token" in response.headers["set-cookie"]



