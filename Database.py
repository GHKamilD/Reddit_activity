from sqlalchemy import create_engine, ForeignKey, Integer, String, Column, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from get_urls import reddit
from datetime import datetime
import uuid
import pandas as pd
import os

Base = declarative_base()


class urls(Base):
    __tablename__ = "urls"
    urlid = Column("urlID", String, primary_key=True)
    url_name = Column("url_name", String)
    used = Column("was_used", Boolean)

    def __init__(self, url_name):
        self.urlid = str(uuid.uuid4())
        self.url_name = url_name
        self.used = False

def add_urls(file_name):
    if os.path.exists('reddit.db'):
        urllist = set()
        with open (file_name, 'r', encoding='utf-8') as file:
            for line in file:
                urllist.add(line)
        engine = create_engine('sqlite:///reddit.db')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        # getting all the urls in the database ([0] is here because the elements in the list are tuples)
        existing_urls = set(url[0] for url in session.query(urls.url_name).all())
        urllist = urllist - existing_urls
        for url in urllist:
            new_url = urls(url)
            session.add(new_url)
        session.commit()
#add_urls('Polska_thread_comment_urls_lipiec.txt')
def add_comments_and_posts():
    class users(Base):
        __tablename__ = "users"
        userid = Column("userID", String, primary_key=True)
        username = Column("username", String)
        def __init__(self, username):
            self.userid = str(uuid.uuid4())
            self.username = username
    class posts(Base):
        __tablename__ = "posts"
        postid = Column("postID", String, primary_key=True)
        userid = Column("userID", String, ForeignKey("users.userID"))
        posttitle = Column("posttitle", String)
        dateposted = Column("dateposted", DateTime)
        postcontent = Column("postcontent", String)
        postflair = Column("postflair", String)
        postupvotes = Column("postupvotes", Integer)

        def __init__(self, userid, posttitle, dateposted,postcontent,postflair,postupvotes):
            self.postid = str(uuid.uuid4())
            self.userid = userid
            self.posttitle = posttitle
            self.dateposted = dateposted
            self.postcontent = postcontent
            self.postflair = postflair
            self.postupvotes = postupvotes
    class comments(Base):
        __tablename__ = "comments"
        commentid = Column("commentID", String, primary_key=True)
        userid = Column("userID", String, ForeignKey("users.userID"))
        dateposted = Column("dateposted", DateTime)
        commentcontent = Column("commentcontent", String)
        commentupvotes = Column("commentupvotes", Integer)
        def __init__(self, userid, dateposted,commentcontent,commentupvotes):
            self.commentid = str(uuid.uuid4())
            self.userid = userid
            self.dateposted = dateposted
            self.commentcontent = commentcontent
            self.commentupvotes = commentupvotes

    engine = create_engine('sqlite:///reddit.db')
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    """with open('Polska_thread_comment_urls_lipiec.txt', 'r', encoding='utf-8') as f:
        all_urls = set(line.strip() for line in f)
    all_database_urls = session.query(urls.url_name).all()
    all_database_urls = set(all_database_urls)
    all_urls = all_urls - all_database_urls"""
    all_urls = session.query(urls).filter_by(used=False).all()
    if len(all_urls)<900:
        x = len(all_urls)
    else:
        x = 900
    for i in range(x):
        print(900 - i)
        try:
            url = all_urls[i].url_name
            # Get the submission object
            submission = reddit.submission(url=f"https://www.reddit.com{url}")
            title = submission.title
            print(title)
            post_time = submission.created_utc
            post_time = datetime.utcfromtimestamp(post_time)
            post_text = submission.selftext
            author = getattr(submission.author, 'name', '[deleted]')
            flara = submission.link_flair_text
            post_votes = submission.score
            user = session.query(users).filter_by(username=author).first()
            if not user:
                new_user = users(author)
                session.add(new_user)
                session.commit()
                user = session.query(users).filter_by(username=author).first()
            author_id = user.userid
            new_post = posts(author_id, title, post_time, post_text, flara, post_votes)
            session.add(new_post)
            all_urls[i].used = True
            session.commit()

            # Iterate over comments in the submission
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                author = getattr(comment.author, 'name', '[deleted]')
                user = session.query(users).filter_by(username=author).first()
                if not user:
                    new_user = users(author)
                    session.add(new_user)
                    session.commit()
                    user = session.query(users).filter_by(username=author).first()
                author_id = user.userid
                comment_text = comment.body
                comment_time = comment.created_utc
                comment_time = datetime.utcfromtimestamp(comment_time)
                comment_votes = comment.score
                new_comment = comments(author_id, comment_time, comment_text, comment_votes)
                session.add(new_comment)
                session.commit()

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
add_comments_and_posts()
