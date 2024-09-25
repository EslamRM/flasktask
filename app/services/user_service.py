class UserService:
    def __init__(self, db):
        self.db = db

    def create_user(self, name, email, password_hash):
        cursor = self.db.cursor()
        query = "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password_hash))
        self.db.commit()
        return cursor.lastrowid

    def get_user(self, user_id):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
