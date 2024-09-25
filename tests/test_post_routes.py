import unittest
import time
import random
from app import create_app
import mysql.connector


class PostRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a fresh MySQL connection for each test
        self.conn = mysql.connector.connect(
            user="root", password="1234", host="localhost", database="PostsDB",port="3307"
        )
        self.cursor = self.conn.cursor()

        # Generate a unique email for each test run
        self.unique_email = (
            f"test{int(time.time())}{random.randint(1000, 9999)}@example.com"
        )

        # Create a user before testing post creation
        response = self.client.post(
            "/user",
            json={
                "name": "Test User",
                "email": self.unique_email,
                "password_hash": "hashedpassword",
            },
        )
        self.assertEqual(response.status_code, 201)

        # Get the user ID from the response
        self.user_id = response.get_json().get("id", 1)

    def tearDown(self):
        # Clean up the created user and close connection after each test
        if self.conn.is_connected():
            self.cursor.execute(
                "DELETE FROM users WHERE email = %s", (self.unique_email,)
            )
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def test_create_post(self):
        # Test creating a post
        response = self.client.post(
            "/post", json={"user_id": self.user_id, "content": "My first post"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        # Check if the response contains 'post_id' instead of 'id'
        self.assertIn("post_id", data)

    def test_get_post(self):
        # Create a post to get
        response = self.client.post(
            "/post", json={"user_id": self.user_id, "content": "My first post"}
        )
        post_id = response.get_json().get("post_id")

        # Test retrieving the created post
        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("content", data)

    def test_update_post(self):
        # Create a post to update
        response = self.client.post(
            "/post", json={"user_id": self.user_id, "content": "My first post"}
        )
        post_id = response.get_json().get("post_id")

        # Test updating the post
        response = self.client.put(
            f"/post/{post_id}", json={"content": "Updated content"}
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_post(self):
        # Create a post to delete
        response = self.client.post(
            "/post", json={"user_id": self.user_id, "content": "My first post"}
        )
        post_id = response.get_json().get("post_id")

        # Test deleting the post
        response = self.client.delete(f"/post/{post_id}")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
