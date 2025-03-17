from flask_testing import TestCase
from src.app import create_app
from src.database.database import db

from src.config.settings import TestSettings


class TestUserAPI(TestCase):
    def create_app(self):
        """
        Create and configure the Flask application for testing.
        """
        app = create_app(TestSettings)

        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user_success(self):
        """
        Test case for successfully creating a user.
        """
        user_data = {"name": "Exemple name", "email": "email@example.com"}

        response = self.client.post("/users", json=user_data)

        assert response.status_code == 201
        assert "name" in response.json
        assert "email" in response.json
        assert response.json["name"] == "Exemple name"
        assert response.json["email"] == "email@example.com"

    def test_create_user_invalid_data(self):
        """
        Test case for creating a user with invalid data.
        """
        invalid_data = {"name": "Invalid"}

        response = self.client.post("/users", json=invalid_data)

        assert response.status_code == 400
        assert "error" in response.json
        assert "Invalid input data" in response.json["error"]

    def test_create_user_duplicate_email(self):
        """
        Test case for creating a user with a duplicate email.
        """
        user_data = {"name": "Test name", "email": "email@example.com"}
        self.client.post(
            "/users", json={"name": "Exemple name", "email": "email@example.com"}
        )

        response = self.client.post("/users", json=user_data)

        assert response.status_code == 409
        assert "error" in response.json
        assert response.json["error"] == "Email email@example.com already exists"

    def test_get_users(self):
        """
        Test case for retrieving the list of users.
        """
        user_data = {"name": "Exemple name", "email": "email@example.com"}
        self.client.post("/users", json=user_data)

        response = self.client.get("/users")

        assert response.status_code == 200
        assert len(response.json) == 1

    def test_get_users_no_users(self):
        """
        Test case for retrieving the list of users when no users exist.
        """
        response = self.client.get("/users")
        assert response.status_code == 200
        assert response.json == []

    def test_get_user(self):
        """
        Test case for retrieving a user by ID.
        :return:
        """
        user_data = {"name": "Exemple name", "email": "email@example.com"}
        response = self.client.post("/users", json=user_data)
        user_id = response.json["id"]

        response = self.client.get(f"/users/{user_id}")

        assert response.status_code == 200
        assert response.json["name"] == "Exemple name"

    def test_get_user_not_found(self):
        response = self.client.get("/users/9999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_user(self):
        """
        Test case for updating an existing user.
        """
        user_data = {"name": "Exemple name", "email": "email@example.com"}
        response = self.client.post("/users", json=user_data)
        user_id = response.json["id"]
        update_data = {"name": "User 2", "email": "email2@example.com"}

        response = self.client.put(f"/users/{user_id}", json=update_data)

        assert response.status_code == 200
        assert response.json["name"] == "User 2"
        assert response.json["email"] == "email2@example.com"

    def test_create_user_invalid_email(self):
        """
        Test case for creating a user with an invalid email.
        """
        invalid_email_data = {"name": "User name", "email": "invalid-email"}

        response = self.client.post("/users", json=invalid_email_data)

        assert response.status_code == 400
        assert "error" in response.json
        assert "Invalid input data" in response.json["error"]

    def test_update_user_not_found(self):
        """
        Test case for updating a user that does not exist.
        """
        update_data = {"name": "User 2", "email": "email2@example.com"}

        response = self.client.put("/users/9999", json=update_data)

        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_user(self):
        """
        Test case for deleting an existing user.
        """
        user_data = {"name": "Exemple name", "email": "email@example.com"}
        response = self.client.post("/users", json=user_data)
        user_id = response.json["id"]
        response = self.client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert "message" in response.json
        assert response.json["message"] == "User deleted successfully"

    def test_delete_user_not_found(self):
        """
        Test case for deleting a user that does not exist.
        """
        response = self.client.delete("/users/9999")
        assert response.status_code == 404
        assert "error" in response.json
