from app import db
import datetime

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64))
    heading = db.Column(db.String)
    post_text = db.Column(db.String)
    post_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
