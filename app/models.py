from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


class User(UserMixin,db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index =True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    subscription = db.Column(db.Boolean)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))

    # role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    role_id = db.relationship('Role',backref = 'user',lazy = "dynamic")

    posts = db.relationship('Post',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    name = db.Column(db.String(255))
    # users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='CASCADE'))
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)

    # comments = db.relationship('Comment',backref = 'post_id',lazy = 'dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def get_post(id):
        post = Post.query.filter_by(id=id).first()
        return post    

class Comment(db.Model):
    __tablename__= 'comments'

    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    post = db.Column(db.Integer,db.ForeignKey('posts.id',ondelete='CASCADE'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,post):
        comments = Comment.query.filter_by(post=post.id).all()
        return comments
