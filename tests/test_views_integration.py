import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure our app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session


class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def testAddPost(self):
        self.simulate_login()
        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Test Post")
        # Removed HTML tags since the posts are in a text format
        self.assertEqual(post.content, "Test content")
        self.assertEqual(post.author, self.user)

# Authored testing for edit post by Michael Nickey
    def testEditPost(self):
        # Simulate a login
        self.simulate_login()
        # Create a post
        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"})
        # make sure that the response code is 302
        self.assertEqual(response.status_code, 302)
        # Query the post
        posts = session.query(models.Post).all()
        # Make sure the post length is only 1, I only added one post
        self.assertEqual(len(posts), 1)
        #using prints to make sure i know what I am seeing, that it is actually creating a post.
        # print posts[0]
        # print "\nContent is: ", posts[0].content
        # posts = posts.get(models.Post.id)
        response = self.client.post("/post/" + str(posts[0].id) + "/edit", data={
            "title": "EDIT Test Post",
            "content": "EDIT Test content"})
        self.assertEqual(response.status_code, 302)

# Authored testing for DELETING a post
    def testDeletePost(self):
        # Simulate a login
        self.simulate_login()
        # Create a post
        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"})
        # make sure that the response code is 302
        self.assertEqual(response.status_code, 302)
        # Query the post
        posts = session.query(models.Post).all()
        # Make sure the post length is only 1, I only added one post
        self.assertEqual(len(posts), 1)
        #using prints to make sure i know what I am seeing, that it is actually creating a post.
        # print posts[0]
        # print "\nContent is: ", posts[0].content
        # posts = posts.get(models.Post.id)
        response = self.client.post("/post/" + str(posts[0].id) + "/delete", data={
            "title": "",
            "content": ""})
        posts = session.query(models.Post).all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(posts), 0)

if __name__ == "__main__":
    unittest.main()
