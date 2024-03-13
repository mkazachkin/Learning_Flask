from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_firstname = db.Column(db.String(128), unique=False, nullable=False, index=True)
    user_lastname = db.Column(db.String(128), unique=False, nullable=False, index=True)
    user_email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    user_password_hash = db.Column(db.String, unique=False, nullable=False)
    user_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_firstname: str, user_lastname: str, user_email: str, user_password: str):
        """
        User class
        :param user_firstname:  User firstname name. Not unique
        :param user_lastname:  User lastname name. Not unique
        :param user_email: User email. Unique
        :param user_password: User password
        """
        self.user_firstname = user_firstname
        self.user_lastname = user_lastname
        self.user_email = user_email
        self.user_password_hash = hashlib.sha256(user_password.encode()).hexdigest()

    def get_user_id(self) -> int:
        """
        Returns user id
        :return: user_id: int
        """
        return self.user_id

    def get_user_firstname(self) -> str:
        """
        Returns user firstname
        :return: user_firstname: str
        """
        return self.user_firstname

    def set_user_firstname(self, user_firstname: str):
        """
        Sets user firstname
        """
        self.user_firstname = user_firstname

    def get_user_lastname(self) -> str:
        """
        Returns user lastname
        :return: user_lastname: str
        """
        return self.user_lastname

    def set_user_lastname(self, user_lastname: str):
        """
        Sets user lastname
        """
        self.user_lastname = user_lastname

    def get_user_email(self) -> str:
        """
        Returns user e-mai
        :return: user_email: str
        """
        return self.user_email

    def set_user_email(self, user_email: str):
        """
        Sets user email
        """
        self.user_email = user_email

    def set_user_password(self, password: str):
        """
        Sets user password
        """
        self.user_password_hash = hashlib.sha256(password.encode()).hexdigest()

    def password_is_valid(self, password: str) -> bool:
        """
        Checks user passwords.
        :param password: user password string
        :return: True if it valid or False if it invalid
        """
        return self.user_password_hash == hashlib.sha256(password.encode()).hexdigest()
