#  -  -  -  -  -  -  #
# CS 334 - Project 3 #
#  -  -  -  -  -  -  #
# Imports
#from django.db import models
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, Integer, String, DateTime, Text, ForeignKey, Enum, or_, and_, func, desc
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.mysql import LONGTEXT, MEDIUMTEXT
import enum

#=====================
#Connect to database
#=====================

# > Install postgresql postgresql-contrib

# After install type into terminal

# psql postgres://avnadmin:v70nehaiku1m4p8f@pg-3efa34b9-pretorius-b301.aivencloud.com:23603/defaultdb?sslmode=require

# Constants
DB_URI = "postgresql+psycopg2://avnadmin:v70nehaiku1m4p8f@pg-3efa34b9-pretorius-b301.aivencloud.com:23603/findr?sslmode=require"

engine = create_engine(DB_URI, echo = False)

# IF the DB has not been made yet, create it
if not database_exists(engine.url):
    create_database(engine.url)

Model = declarative_base()


# Enum for categories
class catEnum(enum.Enum):
    conn = "Looking for connections"
    chat = "Just chatting"
    hottub = "Hot tub"
    lego = "Lego"
    mem = "Memories"
    social = "Social"
    rec = "Recommendation"
    other = "Other"


class noteType(enum.Enum):
    friend = "Friend"
    group = "Group"
    dev = "Dev"


class User(Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(127), nullable=False)
    password = Column(String(127), nullable=False)
    auth_token = Column(String(255))
    bio = Column(String)
    # relationship with posts table
    posts = relationship('Post', backref="user")
    # relationship with comments table
    comment = relationship('Comment', backref="user")
    # relationship with friends table
    friends = relationship('Friend', backref="user")
    # relationship with member table
    member = relationship('Member', backref="user")
    # relationship with note table
    note = relationship('Note', backref="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}', '{self.password}')"


class Post(Model):
    __tablename__ = 'post'
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    post_title = Column(String(50))
    post_desc = Column(String)
    post_likes = Column(Integer)
    post_loc = Column(String)  # Location
    post_time = Column(String, nullable=False, default=datetime.utcnow)
    post_cat = Column(Enum(catEnum))
    # relationship with comments table
    comments = relationship('Comment', backref="post")
    # Category enum

    def __init__(self, user_id, post_title, post_desc, post_loc):
        self.user_id = user_id
        self.post_title = post_title
        self.post_desc = post_desc
        self.post_loc = post_loc

    def __repr__(self):
        return f"Post( '{self.user_id}', '{self.post_title}', '{self.post_desc}', '{self.post_loc}')"


class Comment(Model):
    __tablename__ = 'comment'
    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.post_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    comment_content = Column(String)
    comment_time = Column(String, nullable=False, default=datetime.utcnow)

    def __init__(self, post_id, user_id, comment_content):
        self.post_id = post_id
        self.user_id = user_id
        self.comment_content = comment_content

    def __repr__(self):
        return f"Comment( '{self.post_id}', '{self.user_id}', '{self.comment_content}')"


class Group(Model):
    __tablename__ = 'group'
    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(50), unique=True, nullable=False)
    private = Column(Boolean, nullable=False) # true = private
    group_desc = Column(String)
    # relationship with members table
    member = relationship('Member', backref="group")

    def __init__(self, group_name, private, group_desc):
        self.group_name = group_name
        self.private = private
        self.group_desc = group_desc

    def __repr__(self):
        return f"Group( '{self.group_name}', '{self.private}', '{self.group_desc}')"


class Member(Model):
    __tablename__ = 'member'
    rel_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.group_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self):
        return f"Member( '{self.group_id}', '{self.user_id}')"


class Note(Model):
    __tablename__ = 'note'
    note_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    note_type = Column(Enum(noteType))  # 0 = friends; 1 = groups Enum
    note_status = Column(Boolean, nullable=False)  # true = read, false = unread
    note_desc = Column(String)
    note_birthday = Column(String, default=datetime)

    def __init__(self, user_id, note_type, note_status, note_desc, note_birthday):
        self.user_id = user_id
        self.note_type = note_type
        self.note_status = note_status
        self.note_desc = note_desc
        self.note_birthday = note_birthday

    def __repr__(self):
        return f"Note( '{self.user_id}', '{self.note_type}', '{self.note_status}', '{self.note_desc}', '{self.note_birthday}') "


class Friend(Model):
    __tablename__ = 'friend'
    user_id = Column(Integer, primary_key=True)
    friend_id = Column(Integer, ForeignKey('user.user_id'))
    rel_status = Column(Boolean, nullable=False)  # true = accepted; false = pending

    def __init__(self, user_id, friend_id, rel_status):
        self.user_id = user_id
        self.friend_id = friend_id
        self.rel_status = rel_status

    def __repr__(self):
        return f"Friend( '{self.user_id}', '{self.friend_id}', '{self.rel_status}')"


def commit_changes():
    session.commit()


# Insert's a user into the DB, only requires username, email and password
def insert_user(username, email, password):
    u = User(username, email, password)
    session.add(u)
    session.commit()
    return None


# Update username of user if they wish to change it
# Input - original username, updated_username
def update_userName(user_id, updated_username):
    u = session.query(User).filter(User.user_id == user_id).first()
    u.username = updated_username
    session.commit()
    return None


# Update user bio
# Input - username, bio
def update_userBio(user_id, bio):
    u = session.query(User).filter(User.user_id == user_id).first()
    u.bio = bio
    session.commit()
    return None


# Update user email
# Input - username, email
def update_userEmail(user_id, email):
    u = session.query(User).filter(User.user_id == user_id).first()
    u.email = email
    session.commit()
    return None


# Update user email
# Input - username, email
def update_userPassword(user_id, password):
    u = session.query(User).filter(User.user_id == user_id).first()
    u.password = password
    session.commit()
    return None


# Make a group
# Input - group_name, private [True = private, False = public], group_desc
def make_Group(group_name, private, group_desc):
    try:
        g = Group(group_name, private, group_desc)
        session.add(g)
        session.commit()
    except:
        return False


# Update group description
# Input - group_name, updated_description
def update_groupDesc(group_name, group_updateDesc):
    g = session.query(Group).filter(Group.group_name == group_name).first()
    g.group_desc = group_updateDesc
    session.commit()
    return None


# Update group name
# Input - group name, updated group name
def update_groupName(group_name, group_updateName):
    g = session.query(Group).filter(Group.group_name == group_name).first()
    g.group_name = group_updateName
    session.commit()
    return None


def update_groupPrivate(group_name, group_updatePrivate):
    g = session.query(Group).filter(Group.group_name == group_name).first()
    g.private = group_updatePrivate
    session.commit()
    return None


# Search a group
# Input - group_name
# Returns group object, can be accessed with
# e.g search_group("Group_name").group_name etc
def search_group(group_name):
    g = session.query(Group).filter(Group.group_name == group_name).first()
    return g


# token stored in database at user_id record
# Input - user_id (prim.key) and auth_token
# Return: True if user is there and stores auth token, else False
def store_token(user_id, token):
    u = session.query(User).get(user_id)
    if u == None:
        return False
    else:
        u.auth_token = token
        session.commit()
        return True


# token removed from database at user_id record
# Input - user_id (p.key), auth_token
# Return True if user and auth_token = tok, else False
def remove_token(user_id, token):
    print("user_id ", user_id)
    u = session.query(User).get(user_id)
    if u == None:
        return False
    else:
        print("Token: ", u.auth_token)
        if u.auth_token == token:
            u.auth_token = ''
            session.commit()
            return True
        else:
            return False


# query for user_id and fetch token
# Input - user_id (p.key)
# Return auth tok if True, else empty string
def fetch_token(user_id):
    u = session.query(User).get(user_id)
    if u == None:
        return None
    else:
        return u.auth_token


# Search user in DB
# Input - user_id (p.key)
# Output, User object if true, else None type
def search_user(user_id):
    u = session.query(User).get(user_id)
    return u


# Search user in DB by username
def search_username(username):
    u = session.query(User).filter(User.username == username).first()
    return u


# Search user in DB by email
def search_user_email(email):
    u = session.query(User).filter(User.email == email).first()
    return u


# -------------------------------
# COMMENTS
# -------------------------------
def post_exists(post_id):
    p = session.query(Post).get(post_id)
    return p is not None


def user_exists(user_id):
    u = session.query(User).get(user_id)
    return u is not None


def insert_comment(post_id, user_id, comment_content):
    new_comment = Comment(post_id=post_id, user_id=user_id, comment_content=comment_content)
    session.add(new_comment)
    session.commit()
    return


def load_comment(comment_id):
    c = session.query(Comment).get(comment_id)
    return c


def update_comment(comment_id, comment_content):
    c = session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if c is None:
        return False
    c.comment_content = comment_content
    session.commit()
    return True

def delete_comment(comment_id):
    session.query(Comment).filter(Comment.comment_id == comment_id).delete()
    session.commit()
    return

# -----------
# MAIN
# ------------
Model.metadata.create_all(engine)
#print(Model.metadata.tables.keys())
Session = sessionmaker(bind = engine)
session = Session()

# ------------
# Helper Functions
# ------------
#print(query_user("Babus_boy").email)
#insert_user("Baby_boy", "baby_boy@gmail.com", "Cheesiboy")
#update_userName("Baby_boy", "Babus_boy")
#update_userBio("Babus_boy", "I wanna send you to the realms!")

# TODO:
# TABLES: USER, POST, COMMENT, GROUP, MEMBER, NOTE, FRIEND
# Query insert: User(user_id, username, email, password, auth_token, bio)


# -------------------------------
# Helper Function's for posts.py
# -------------------------------

def search_user_by_id(user_id):
    try:
        u = session.query(User).get(user_id)
        if u is None:
            return -1
        return u
    except:
        return False


def create_post(user_id, group_id, post_title, post_body, post_location, post_cat):
    try:
        p = Post(user_id, post_title, post_body, post_location)
        p.post_likes = 0
        session.add(p)
        session.commit()
        # TODO: Initialise likes to 0
        return True
    except:
        return False


def remove_post(post_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).delete()
        session.commit()
        return True
    except:
        return False


# Still need to account for errors return False if commit is unsuccessful
def edit_post_desc(post_id, post_desc):
    p = session.query(Post).filter(Post.post_id == post_id).first()
    if p is None:
        return False
    p.post_desc = post_desc
    session.commit()
    return True


# Still need to account for errors return False if commit is unsuccessful
def edit_post_title(post_id, post_title):
    p = session.query(Post).filter(Post.post_id == post_id).first()
    if p is None:
        return False
    p.post_title = post_title
    session.commit()
    return True


def edit_post_location(post_id, post_location):
    p = session.query(Post).filter(Post.post_id == post_id).first()
    if p is None:
        return False
    p.post_loc = post_location
    session.commit()
    return True


def edit_post_category(post_id, post_category):
    p = session.query(Post).filter(Post.post_id == post_id).first()
    if p is None:
        return False
    p.post_loc = post_category
    session.commit()
    return True


# Still need to account for errors return False if commit is unsuccessful
def load_post(post_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        return p
    except:
        return False


def like_post(post_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        if p is None:
            return False
        p.post_likes += 1
        session.commit()
        return True
    except:
        return False


# FIXME - Not sure if this is correct
def post_comment(post_id, user_id, comment_content):
    c = Comment(post_id, user_id, comment_content)
    session.add(c)
    session.commit()
    return True
    # try:
    #     c = Comment(post_id, user_id, comment_content)
    #     session.add(c)
    #     session.commit()
    #     return True
    # except:
    #     return False


def remove_comments(post_id):
        try:
            c = session.query(Comment).filter(Comment.post_id == post_id)
            if c.first() is None:
                return True
            c.delete()
            session.commit()
            return True
        except:
            return False


def get_comments(post_id):
    try:
        c = session.query(Comment).filter(Comment.post_id == post_id)
        return c
    except:
        return False


# -------------------------------
# Helper Function's for groups.py
# -------------------------------

def create_group(group_name, private, group_desc):
    try:
        g = Group(group_name, private, group_desc)
        session.add(g)
        session.commit()
        return True
    except:
        return False


def search_group_by_name(group_name):
    try:
        g = session.query(Group).filter(Group.group_name == group_name).first()
        return g
    except:
        return False


def search_group_by_id(group_id):
    try:
        g = session.query(Group).filter(Group.group_id == group_id).first()
        return g
    except:
        return False


def delete_group(group_id):
    # Still need to implement
    try:
        g = session.query(Group).filter(Group.group_id == group_id)
        if g.first() is None:
            return -1
        else:
            g.delete()
        session.commit()
        return True
    except:
        return False


def update_group_desc(group_id, updated_desc):
    try:
        g = session.query(Group).filter(Group.group_id == group_id).first()
        g.group_desc = updated_desc
        session.commit()
        return True
    except:
        return False


def update_group_name(group_id, updated_name):
    try:
        g = session.query(Group).filter(Group.group_id == group_id).first()
        g.group_name = updated_name
        session.commit()
        return True
    except:
        return False


def update_group_private(group_id, updated_private):
    try:
        g = session.query(Group).filter(Group.group_id == group_id).first()
        g.private = updated_private
        session.commit()
        return True
    except:
        return False


def join_group(group_id, user_id):
    try:
        m = Member(group_id=group_id, user_id=user_id)
        session.add(m)
        session.commit()
        return True
    except:
        return False


def leave_group(group_id, user_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id and Member.user_id == user_id)
        if m.first() is None:
            return -1
        else:
            m.delete()
        session.commit()
        return True
    except:
        return False


def search_groups_by_name(search_term):
    try:
        m = session.query(Group).filter(Group.group_name.contains(search_term))
        return m
    except:
        return False


def search_groups_by_desc(search_term):
    try:
        m = session.query(Group).filter(Group.group_desc.contains(search_term))
        return m
    except:
        return False


def load_group_members(group_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id)
        return m
    except:
        return False


def load_group_posts(group_id):
    try:
        p = session.query(Post).filter(Post.group_id == group_id)
        return p
    except:
        return False


def remove_members(group_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id)
        if m.first() is None:
            return True
        m.delete()
        session.commit()
        return True
    except:
        return False

# def remove_posts(group_id):
#     try:
#         p = session.query(Member).filter(Member.group_id == group_id)
#         if m.first() is None:
#             return True
#         m.delete()
#         session.commit()
#         return True
#     except:
#         return False