import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from website import create_app, db
from website.models import User, Post

class FlaskTestCase(unittest.TestCase):
    """
    Test case for the Flask application, including setup and teardown 
    methods and individual tests for signup, login, making posts, 
    deleting posts, and accessing the home page.
    """

    def setUp(self):
        """
        Set up the test client and database before each test.
        This method is called before each test method.
        """
        self.app = create_app()
        # Enable testing mode
        self.app.config['TESTING'] = True
        # Use in-memory database for tests
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all database tables
        db.create_all()
        # Create test client
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Tear down the test client and database after each test.
        This method is called after each test method.
        """
        db.session.remove()
        # Drop all database tables
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """
        Test if the home page is accessible.
        This checks if the home page redirects to the login page 
        (since the user is not logged in).
        """
        response = self.client.get('/home')
        # Check for redirect status code: The status code of redirect is 302.
        self.assertEqual(response.status_code, 302)

    def test_signup(self):
        """
        Test user signup.
        This checks if a new user can sign up and is successfully added 
        to the database with the correct avatar URL.
        """
        response = self.client.post('/sign-up', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'password',
            'password2': 'password'
        }, follow_redirects=True)
        # Check for OK status code
        self.assertEqual(response.status_code, 200)
        # Check for success message
        self.assertIn(b'User created successfully!', response.data)
        user = User.query.filter_by(email='test@example.com').first()  # Query for the new user
        self.assertIsNotNone(user)  # Check that the user is not None
        self.assertTrue(user.avatar_url.startswith('https://avatars.dicebear.com/api/initials/'))  # Check avatar URL

    def test_login(self):
        """
        Test user login.
        This checks if an existing user can log in successfully.
        """
        # Create and add a test user to the database
        user = User(email='login@example.com', username='loginuser', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        # Attempt to log in with the test user's credentials
        response = self.client.post('/login', data={
            'email': 'login@example.com',
            'password': 'password'
        }, follow_redirects=True)
        # Check for OK status code
        self.assertEqual(response.status_code, 200)  
        # Check for success message
        self.assertIn(b'Logged in!', response.data)  

    def test_make_post(self):
        """
        Test creating a new post.
        This checks if a logged-in user can create a new post.
        """
        # Create and add a test user to the database
        user = User(email='poster@example.com', username='poster', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        # Log in with the test user's credentials
        self.client.post('/login', data={
            'email': 'poster@example.com',
            'password': 'password'
        }, follow_redirects=True)
        # Attempt to create a new post
        response = self.client.post('/make-post', data={
            'text': 'This is a test post'
        }, follow_redirects=True)
        # Check for OK status code
        self.assertEqual(response.status_code, 200)  
        # Check for success message
        self.assertIn(b'Post created', response.data)  
        
        # Query for the new post
        post = Post.query.filter_by(text='This is a test post').first()  
        # Check that the post is not None
        self.assertIsNotNone(post)  

    def test_delete_post(self):
        """
        Test deleting a post.
        This checks if a logged-in user can delete a post they created.
        """
        # Create and add a test user to the database
        user = User(email='deleter@example.com', username='deleter', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        # Create and add a test post to the database
        post = Post(text='This post will be deleted', author=user.id)
        db.session.add(post)
        db.session.commit()
        # Log in with the test user's credentials
        self.client.post('/login', data={
            'email': 'deleter@example.com',
            'password': 'password'
        }, follow_redirects=True)
        # Attempt to delete the post
        response = self.client.post(f'/delete-post/{post.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Check for OK status code
        self.assertIn(b'Post deleted', response.data)  # Check for success message
        post = Post.query.filter_by(text='This post will be deleted').first()  # Query for the deleted post
        self.assertIsNone(post)  # Check that the post is None (i.e., deleted)

if __name__ == '__main__':
    unittest.main()
