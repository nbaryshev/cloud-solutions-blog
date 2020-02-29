from app import db, models, login_mngr
import datetime, flask_login
from werkzeug.security import check_password_hash, generate_password_hash

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64))
    heading = db.Column(db.String)
    post_text = db.Column(db.String)
    post_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def create_post(cls, topic=None, heading=None, post_text=None, post_time=None):
        # Apply filters
        topic = topic.lower()

        # Create obj
        new_post = models.Post(topic=topic, heading=heading, post_text=post_text, post_time=post_time)
        db.session.add(new_post)
        db.session.commit()

        return new_post

    #Retrieve a posting time for specific post in a readable format
    def get_human_time(self):
        return "{}/{}/{} at {}:{}".format(
            self.post_time.day,
            self.post_time.month,
            self.post_time.year,
            self.post_time.hour,
            self.post_time.minute
        )


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    @classmethod
    def create_user(cls, name=None, email=None, pwd=None):
        """
        creates new user
        """

        new_user = User(name=name, email=email, pwd=pwd)
        db.session.add(new_user)
        db.session.commit()

        return new_user
