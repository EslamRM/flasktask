class PostService:
    def __init__(self, db):
        self.db = db

    def create_post(self, user_id, content):
        cursor = self.db.cursor()
        query = "INSERT INTO posts (user_id, content) VALUES (%s, %s)"
        cursor.execute(query, (user_id, content))
        self.db.commit()
        return cursor.lastrowid

    def update_post(self, post_id, content):
        cursor = self.db.cursor()
        query = "UPDATE posts SET content = %s WHERE id = %s"
        cursor.execute(query, (content, post_id))
        self.db.commit()

    def delete_post(self, post_id):
        cursor = self.db.cursor()
        query = "DELETE FROM posts WHERE id = %s"
        cursor.execute(query, (post_id,))
        self.db.commit()

    def get_post(self, post_id):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(query, (post_id,))
        return cursor.fetchone()

    def get_all_posts(self):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM posts"
        cursor.execute(query)
        return cursor.fetchall()
