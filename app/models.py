#  -  -  -  -  -  -  #
# CS 334 - Project 3 #
#  -  -  -  -  -  -  #
# Imports
#from django.db import models
from datetime import datetime
from sqlalchemy import create_engine, Column, Boolean, Integer, String, ForeignKey, Enum, desc, or_, and_
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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
    avatar = Column(String(255), nullable=False, default="https://storage.googleapis.com/findr-316018_bucket/default.PNG")
    bio = Column(String)
    # relationship with posts table
    posts = relationship('Post', backref="user")
    # relationship with comments table
    comment = relationship('Comment', backref="user")
    #friends = relationship('Friend', primaryjoin='User.user_id==Friend.user_a_id')
    # relationship with friends table
    #friend = relationship('Friend', foreign_keys='Friend.rel_id', backref='friend_rel', lazy='dynamic')
    #friend = relationship('Friend', foreign_keys='Friend.rel_id', backref='friend_rel', lazy='dynamic')
    #friend_2 = relationship('Friend', foreign_keys='Friend.user_a_id', backref='friend_b_user_id', lazy='dynamic')
    # relationship with member table
    member = relationship('Member', backref="user")
    # relationship with note table
    note = relationship('Note', backref="user")
    #sub_id = relationship('Note', backref="subject")

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
    group_id = Column(Integer, ForeignKey('group.group_id'))
    post_title = Column(String(50))
    post_desc = Column(String)
    post_likes = Column(Integer)
    post_loc = Column(String)  # Location
    post_time = Column(String, nullable=False, default=datetime.utcnow)
    post_cat = Column(Enum(catEnum))
    # relationship with comments table
    comments = relationship('Comment', backref="post")
    # Category enum

    def __init__(self, user_id, group_id, post_title, post_desc, post_loc, post_cat):
        self.user_id = user_id
        self.post_title = post_title
        self.post_desc = post_desc
        self.post_loc = post_loc
        self.group_id = group_id
        self.post_cat = post_cat

    def __repr__(self):
        return f"Post( '{self.user_id}', '{self.group_id}', {self.post_title}', '{self.post_desc}', '{self.post_loc}', " \
               f"'{self.post_cat}')"


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
    membership = Column(Integer, nullable=False) # 0 = Pending, 1 = Member, 2 = Admin

    def __init__(self, group_id, user_id, membership):
        self.group_id = group_id
        self.user_id = user_id
        self.membership = membership

    def __repr__(self):
        return f"Member( '{self.group_id}', '{self.user_id}', '{self.membership}')"


class Note(Model):
    __tablename__ = 'note'
    note_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    group_id = Column(Integer, ForeignKey('group.group_id')) # Needed for loading all group requests
    #subject_id = Column(Integer, ForeignKey('user.user_id')) # Needed for subjects
    note_type = Column(Enum(noteType))  # 0 = friends; 1 = groups Enum
    note_status = Column(Boolean, nullable=False)  # true = read, false = unread
    note_desc = Column(String)
    note_birthday = Column(String, default=datetime)

    def __init__(self, user_id, group_id, note_type, note_status, note_desc, note_birthday):
        self.user_id = user_id
        self.group_id = group_id
        self.note_type = note_type
        self.note_status = note_status
        self.note_desc = note_desc
        self.note_birthday = note_birthday

    def __repr__(self):
        return f"Note( '{self.user_id}', '{self.group_id}', {self.note_type}', '{self.note_status}', '{self.note_desc}', '{self.note_birthday}') "


class Friend(Model):
    __tablename__ = 'friend'
    rel_id = Column(Integer, primary_key=True)
    pal_id = Column(Integer, ForeignKey("user.user_id"))
    friend_id = Column(Integer, ForeignKey("user.user_id"))
    rel_type = Column(Integer, nullable=False)

    pal = relationship("User", foreign_keys=[pal_id])
    friend = relationship("User", foreign_keys=[friend_id])

    def __init__(self, pal_id, friend_id, rel_type):
        self.pal_id = pal_id
        self.friend_id = friend_id
        self.rel_type = rel_type


class Like(Model):
    __tablename__ = 'like'
    like_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.post_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return f"Like( '{self.post_id}', '{self.user_id}')"


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


def search_users_by_name(search_term):
    try:
        u = session.query(User).filter(User.username.contains(search_term)).all()
        return u
    except:
        return None

# -------------------------------
# COMMENTS
# -------------------------------
def post_exists(post_id):
    p = session.query(Post).get(post_id)
    return p is not None


def user_exists(user_id):
    u = session.query(User).get(user_id)
    return u is not None


def group_exists(group_id):
    g = session.query(Group).get(group_id)
    return g is not None


def note_exists(note_id):
    print(note_id)
    n = session.query(Note).get(note_id)

    return n is not None


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

def has_liked(user_id, post_id):
    try:
        l = session.query(Like).filter(Like.user_id == user_id).filter(Like.post_id == post_id).first()
        if l is None:
            return False
        return True
    except:
        return -1


def search_user_by_id(user_id):
    try:
        u = session.query(User).get(user_id)
        if u is None:
            return -1
        return u
    except:
        return False


def search_user_by_username(username):
    try:
        u = session.query(User).filter(User.username == username).first()
        if u is None:
            return -1
        return u
    except:
        return False


def create_post(user_id, group_id, post_title, post_body, post_location, post_cat):
    try:
        p = Post(user_id, group_id, post_title, post_body, post_location, post_cat)
        p.post_likes = 0
        session.add(p)
        session.commit()
        return p.post_id
    except:
        return False


def remove_post(post_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).delete()
        session.commit()
        return True
    except:
        return False


def edit_post_desc(post_id, post_desc):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        if p is None:
            return False
        p.post_desc = post_desc
        session.commit()
        return True
    except:
        return False


def edit_post_title(post_id, post_title):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        if p is None:
            return -1
        p.post_title = post_title
        session.commit()
        return True
    except:
        return False


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


def load_post(post_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        return p
    except:
        return False


def like_post(post_id, user_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        if p is None:
            return False
        p.post_likes += 1
        if session.query(Like).filter(Like.post_id == post_id).filter(Like.user_id == user_id).first() is None:
            l = Like(post_id=post_id, user_id=user_id)
            session.add(l)
        session.commit()
        return True
    except:
        return False


def unlike_post(post_id, user_id):
    try:
        p = session.query(Post).filter(Post.post_id == post_id).first()
        if p is None:
            return False
        p.post_likes -= 1
        session.query(Like).filter(Like.post_id == post_id).filter(Like.user_id == user_id).delete()
        session.commit()
        return True
    except:
        return False


def post_comment(post_id, user_id, comment_content):
    try:
        c = Comment(post_id, user_id, comment_content)
        session.add(c)
        session.commit()
        return True
    except:
        return False


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
        c = session.query(Comment).filter(Comment.post_id == post_id).all()
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


def join_group(group_id, user_id, membership):
    try:
        m = Member(group_id=group_id, user_id=user_id, membership=membership)
        session.add(m)
        session.commit()
        return True
    except:
        return False


def leave_group(group_id, user_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id).filter(Member.user_id == user_id)
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
        m = session.query(Group).filter(Group.group_name.contains(search_term)).all()
        return m
    except:
        return False


def search_groups_by_desc(search_term):
    try:
        m = session.query(Group).filter(Group.group_desc.contains(search_term)).all()
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
        p = session.query(Post).filter(Post.group_id == group_id).order_by(desc(Post.post_time)).all()
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


def get_group_member(user_id, group_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id).filter(Member.user_id == user_id).first()
        return m
    except:
        return False


def promote_user(user_id, group_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id).filter(Member.user_id == user_id).first()
        m.membership = 2
        session.commit()
        return True
    except:
        return False


def demote_user(user_id, group_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id).filter(Member.user_id == user_id).first()
        m.membership = 1
        session.commit()
        return True
    except:
        return False


def get_group_admins(group_id):
    try:
        m = session.query(Member).filter(Member.membership == 2).filter(Member.group_id == group_id).all()
        return m
    except:
        return False


def delete_group_posts(group_id):
    try:
        p = session.query(Post).filter(Post.group_id == group_id)
        if p.first() is None:
            return True
        p.delete()
        session.commit()
        return True
    except:
        return False


def delete_group_members(group_id):
    try:
        m = session.query(Member).filter(Member.group_id == group_id)
        if m.first() is None:
            return True
        m.delete()
        session.commit()
        return True
    except:
        return False


def load_join_request(group_id):
    try:
        m = session.query(Member).filter(Member.membership == 0).filter(Member.group_id == group_id).all()
        return m
    except:
        return False


def request_group_invite(group_id, user_id):
    try:
        m = Member(group_id=group_id, user_id=user_id, membership=0)
        session.add(m)
        session.commit()
    except:
        return False


def accept_join_request(group_id, user_id):
    try:
        m = session.query(Member).filter(Member.user_id == user_id).filter(Member.group_id == group_id).\
            filter(Member.membership == 0).first()
        if m is None:
            return -1
        m.membership = 1
        session.commit()
        return True
    except:
        return False


def decline_join_request(group_id, user_id):
    try:
        m = session.query(Member).filter(Member.user_id == user_id).filter(Member.group_id == group_id).\
            filter(Member.membership == 0)
        if m is None:
            return -1
        m.delete()
        session.commit()
        return True
    except:
        return False


def get_users_groups(user_id):
    try:
        m = session.query(Member).filter(Member.user_id == user_id).filter(Member.membership != 0).all()
        return m
    except:
        return False


def get_posts_from_user(user_id, group_id):
    try:
        p = session.query(Post).filter(Post.user_id == user_id).filter(Post.group_id == group_id).all()
        return p
    except:
        return False


def get_posts_from_category(category, group_id):
    try:
        p = session.query(Post).filter(Post.post_cat == category).filter(Post.group_id == group_id).all()
        return p
    except:
        return False


# -------------------------------
# Helper Function's for notes.py
# -------------------------------


def load_notifications(user_id):
    try:
        n = session.query(Note).filter(Note.user_id == user_id).all()
        return n
    except:
        return False


def load_notification(note_id):
    try:
        n = session.query(Note).get(note_id)
        return n
    except:
        return None


def create_notification(user_id, subject_id, group_id, note_type, status, note_desc):
    try:
        n = Note(user_id, subject_id, group_id, note_type, status, note_desc, datetime.now())
        session.add(n)
        session.commit()
        return True
    except:
        return False


def delete_notification(note_id):
    try:
        n = session.query(Note).filter(Note.note_id == note_id).delete()
        session.commit()
        return True
    except:
        return False


def update_notification(note_id):
    try:
        n = session.query(Note).filter(Note.note_id == note_id).first()
        n.note_status = True
        session.commit()
        return True
    except:
        return False

# -------------------------------
# Helper Function's for friends
# -------------------------------

def invite_friend(user_a_id, user_b_id):
    f = session.query(Friend).filter(or_(and_(Friend.pal_id == user_a_id, Friend.friend_id == user_b_id), and_(Friend.friend_id == user_a_id, Friend.pal_id == user_b_id))).first()
    if f == None:
        f = Friend(user_a_id, user_b_id, 0)
        return True
    else:
        return False

def accept_friend(user_b_id, user_a_id):
    f = session.query(Friend).filter(or_(and_(Friend.pal_id == user_a_id, Friend.friend_id == user_b_id), and_(Friend.friend_id == user_a_id, Friend.pal_id == user_b_id))).first()
    if f == None:
        return False
    else:
        f1 = session.query(Friend).filter(and_(Friend.pal_id == user_a_id, Friend.friend_id == user_b_id)).first()
        f2 = session.query(Friend).filter(and_(Friend.friend_id == user_a_id, Friend.pal_id == user_b_id)).first()

        if f1 == None:
            f2.rel_type = 1
            session.commit()

        elif f2 == None:
            f1.rel_type = 1
            session.commit()

        return True

# Returns None if no relation exists between user A and B, else returns the type, i.e False == Pending and True == Friends
def get_rel_type(user_a_id, user_b_id):
    f = session.query(Friend).filter(or_(and_(Friend.pal_id == user_a_id, Friend.friend_id == user_b_id), and_(Friend.friend_id == user_a_id, Friend.pal_id == user_b_id))).first()
    if f == None:
        return None
    else:
        f1 = session.query(Friend).filter(and_(Friend.pal_id == user_a_id, Friend.friend_id == user_b_id)).first()
        f2 = session.query(Friend).filter(and_(Friend.friend_id == user_a_id, Friend.pal_id == user_b_id)).first()

        if f1 == None:
            return f2.rel_type

        elif f2 == None:
            return f1.rel_type


# -------------------------------
# Helper Function's for avatar
# -------------------------------

def update_user_avatar(user_id, avatar):
    try:
        u = session.query(User).filter(User.user_id == user_id).first()
        u.avatar = avatar
        session.commit()
        return True
    except:
        return False


# -------------------------------
# Helper Function's for Feed
# -------------------------------

def load_feed(user_id):
    try:
        posts = session.query(Post).filter(Post.group_id == Member.group_id).filter(Member.user_id == user_id).all()
        return posts
    except:
        return False


def load_feed_by_time(user_id):
    try:
        posts = session.query(Post).filter(Post.group_id == Member.group_id).filter(Member.user_id == user_id).order_by(desc(Post.post_time)).all()
        return posts
    except:
        return False


def load_feed_by_category(category, user_id):
    try:
        posts = session.query(Post).filter(Post.group_id == Member.group_id).filter(Post.post_cat == category).filter(Member.user_id == user_id).all()
        return posts
    except:
        return False


def load_feed_by_group(user_id, group_id):
    try:
        posts = session.query(Post).filter(Post.group_id == group_id).all()
        return posts
    except:
        return False


def load_feed_by_user(user_id, filter_user_id):
    try:
        posts = session.query(Post).filter(Post.group_id == Member.group_id).filter(Post.user_id == filter_user_id).filter(
        Member.user_id == user_id).all()
        return posts
    except:
        return False

#print(invite_friend(1,2))
#print(accept_friend(2,1))
#print(get_rel_type(1,2))
#f = Friend(1, 2, 0)
#session.add(f)
#session.commit()
#invite_friend(1,2)
