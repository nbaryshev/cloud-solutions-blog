from app import db, models, login_mngr
import datetime, flask_login
from werkzeug.security import check_password_hash, generate_password_hash

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    heading = db.Column(db.String)
    post_preview = db.Column(db.String)
    post_text = db.Column(db.String)
    post_image = db.Column(db.String)
    post_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comment', backref='post') # one Post may have many comments(one-to-many with Comments table) ?

    @classmethod
    def create_post(cls, topic=None, heading=None, post_preview=None, post_text=None, post_time=None, post_image=None):
        # Apply filters
        topic = topic.lower()

        # Create obj
        new_post = models.Post(topic=topic, heading=heading, post_preview=post_preview, post_text=post_text, post_time=post_time, post_image=post_image)
        db.session.add(new_post)
        db.session.commit()

        return new_post

    #Retrieve a posting time for specific post in a readable format
    def get_human_time(self):
        return "{}-{}-{} at {}:{}".format(
            self.post_time.day,
            self.post_time.month,
            self.post_time.year,
            self.post_time.hour,
            self.post_time.minute
        )

    def add_comment(self, comment):
        self.comments.append(comment)
        db.session.commit()


@login_mngr.user_loader
def load_user(user_id):
    user_id = int(user_id)
    return User.query.get(user_id)


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    pwd = db.Column(db.String(128))
    user_image = db.Column(db.String(128))
    comments = db.relationship('Comment', backref='user') # one User may have many comments(one-to-many with Comments table)

    def change_pwd(self, pwd):
        hashed_pwd = generate_password_hash(pwd)
        self.pwd = hashed_pwd
        db.session.commit()

    def check_pwd(self, pwd):
        """
        :param pwd:
        :return: Boolean
        """
        return check_password_hash(self.pwd, pwd)

    def get_id(self):
        return self.id

    def add_comment(self, comment):
        self.comments.append(comment)
        db.session.commit()

    @classmethod
    def create_user(cls, name=None, email=None, pwd=None, user_image=None):
        """
        creates new user
        """

        new_user = cls(name=name, email=email, user_image=user_image)
        new_user.change_pwd(pwd)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @classmethod
    def sign_in(cls, email, pwd, remember=False):
        user = cls.get_by_email(email=email)
        good_pwd = user.check_pwd(pwd)
        if good_pwd:
            flask_login.login_user(user, remember=remember)

        return good_pwd

    @classmethod
    def get_by_email(cls, email):
        """
        Retrieves User by pwd for Sign In
        """
        user = User.query.filter_by(email=email).first()

        return user

    @classmethod
    def signout(cls):
        flask_login.logout_user()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    comment_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def create_comment(cls, users_comment, post_id):
        """
        Create new comment
        """
        new_comment = cls(users_comment=users_comment, post_id=post_id)

        db.session.add(new_comment)
        db.session.commit()

        return new_comment

    def get_comment_time(self):
        return "{}-{}-{} at {}:{}".format(
            self.comment_time.day,
            self.comment_time.month,
            self.comment_time.year,
            self.comment_time.hour,
            self.comment_time.minute
        )