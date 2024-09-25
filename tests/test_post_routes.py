import unittest
from app import create_app

class PostRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_post(self):
        response = self.client.post('/post', json={'user_id': 1, 'content': 'My first post'})
        self.assertEqual(response.status_code, 201)

    def test_get_post(self):
        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('content', data)

    def test_update_post(self):
        response = self.client.put('/post/1', json={'content': 'Updated content'})
        self.assertEqual(response.status_code, 204)

    def test_delete_post(self):
        response = self.client.delete('/post/1')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
