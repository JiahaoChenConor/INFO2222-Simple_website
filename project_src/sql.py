import sys
import mariadb
import hashlib

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase:
    """
        Our SQL Database

    """

    # Get the database running
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="admin",
                host="localhost",
                port=3306,
                database='Excelsior')
        except mariadb.Error as e:
            print("Error connecting to Database {e}".format(e=e))
            sys.exit(1)
        self.cur = self.conn.cursor()

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    # Rollback changes to the database
    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0):
        self.cur.execute("select * from Users where username = ?", (username, ))
        if self.cur.fetchone():
            return "Username already exists"
        self.cur.execute("insert into Users(username, password, admin) values (?, ?, ?)",
                         (username, password, admin))
        try:
            self.commit()
        except mariadb.Error:
            self.rollback()
            return "Database error"
        return "Done"

    def mute_user(self, user_id):
        query = "update Users set muted = case when muted = 0 then 1 else 0 end where Id = ?"
        self.cur.execute(query, (user_id,))
        try:
            self.commit()
        except mariadb.Error:
            self.rollback()
            return "Database error"
        return "Done"

    # -----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        query = "select * from Users where username = ? and password = ?"
        self.cur.execute(query, (username, password))
        # If our query returns
        response = self.cur.fetchone()
        if response:
            return response
        else:
            return None

    # Check if cookie for user is correct
    def cookie(self, cookie):
        if cookie is None:
            return None
        self.cur.execute("select * from Users where username = ?", (cookie, ))
        # If our query returns
        result = self.cur.fetchone()
        return result

    # Create Post
    # New post: thread_id == 0, means the first thread of such post
    # Reply: topic_id == the thread's id
    def create_post(self, subject, body, topic_id, user_id, thread_id=0):
        if int(topic_id) == 0:
            self.cur.execute("select max(topic_id) from Posts")
            result = self.cur.fetchall()
            # must initialize database with a post
            topic_id = result[0][0] + 1
        else:
            self.cur.execute("select max(thread_id) from Posts")
            result = self.cur.fetchall()
            # must initialize database with a post
            thread_id = result[0][0] + 1
        query = "insert into Posts(subject, topic_id, body, thread_id, user_id) values(?, ?, ?, ?, ?)"
        self.cur.execute(query, (subject, topic_id, body, thread_id, user_id))
        try:
            self.commit()
        except mariadb.Error:
            self.rollback()
            return False
        return True

    # Return subject of all post with thread_id = 0
    def query_post_by_id(self):
        query = "select topic_id, subject, created_at, deleted from Posts where thread_id = 0"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    # Return all post from same Id's thread
    def query_post_by_thread(self, thread_id):
        query = "select Posts.subject, Posts.body, Posts.created_at, Posts.topic_id, Users.username, Posts.deleted from Posts " \
                "inner join Users on Posts.user_id = Users.Id where topic_id = ? order by created_at"
        self.cur.execute(query, (thread_id,))
        result = self.cur.fetchall()
        return result

    # Delete a post or restore it
    def delete_post_by_thread(self, thread_id):
        query = "update Posts set deleted = case when deleted = 0 then 1 else 0 end where topic_id = ?"
        self.cur.execute(query, (thread_id,))
        try:
            self.commit()
        except mariadb.Error:
            self.rollback()
            return "Database error"
        return "Done"

    # Return subject of all post with related topic_id
    def query_all_users(self):
        query = "select Id, username, admin, muted from Users order by Id"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def update_hashed_database(self):
        password_query = "select Id, password from Users order by Id"
        self.cur.execute(password_query)
        passwords = self.cur.fetchall()

        for column in passwords:
            Id = column[0]
            password = column[1]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            query = "update Users set password = ? where Id = ?"
            self.cur.execute(query, (hashed_password, Id))

        try:
            self.commit()
        except mariadb.Error:
            self.rollback()
            return "Database error"
        return "Done"


if __name__ == "__main__":
    sql = SQLDatabase()
    sql.update_hashed_database()
    sql.close()
