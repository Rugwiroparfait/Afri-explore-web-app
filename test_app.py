import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from website import create_app, db
from website.models import User, Post

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """
        Set up the test client and database before each test.
        """
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Tear down the test client and database after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """
        Test if the home page is accessible.
        """
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_signup(self):
        """
        Test user signup.
        """
        response = self.client.post('/sign-up', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'password',
            'password2': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Created', response.data)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

    def test_login(self):
        """
        Test user login.
        """
        user = User(email='login@example.com', username='loginuser', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'email': 'login@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in!', response.data)

    def test_make_post(self):
        """
        Test creating a new post.
        """
        user = User(email='poster@example.com', username='poster', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        self.client.post('/login', data={
            'email': 'poster@example.com',
            'password': 'password'
        }, follow_redirects=True)
        response = self.client.post('/make-post', data={
            'text': 'This is a test post'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post created', response.data)
        post = Post.query.filter_by(text='This is a test post').first()
        self.assertIsNotNone(post)

    def test_delete_post(self):
        """
        Test deleting a post.
        """
        user = User(email='deleter@example.com', username='deleter', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        post = Post(text='This post will be deleted', author=user.id)
        db.session.add(post)
        db.session.commit()
        self.client.post('/login', data={
            'email': 'deleter@example.com',
            'password': 'password'
        }, follow_redirects=True)
        response = self.client.post(f'/delete-post/{post.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post deleted', response.data)
        post = Post.query.filter_by(text='This post will be deleted').first()
        self.assertIsNone(post)

if __name__ == '__main__':
    unittest.main()
