from application.database import db
from datetime import date
from flask_security import RoleMixin, UserMixin

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin): 
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(), nullable=False)
    lname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    lists = db.relationship('List', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'User-{self.fname} {self.lname}'


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(),nullable=False, unique=True)
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime(), nullable=False,default=date.today())
    # foreign key
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    cards = db.relationship('Card', backref='list', lazy=True)

    def __repr__(self):
        return f'List-{self.name}'


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(),nullable=False, unique=True)
    content = db.Column(db.String())
    deadline = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False,default=date.today())
    date_completed = db.Column(db.DateTime())
    completed_status = db.Column(db.Boolean(), nullable=False)
    # foreign key
    list_id = db.Column(db.Integer(), db.ForeignKey(
        'list.id',ondelete='CASCADE'))

    def __repr__(self):
        return f'Card-{self.title}'


