import flask_wtf
import wtforms
from wtforms.validators import DataRequired

from app import models

topics = ['History', 'Building']
choices = [(topic, topic) for topic in topics]

class NewPost(flask_wtf.FlaskForm):
    topic = wtforms.SelectField('Choose the topic', choices=choices, validators=[DataRequired()])
    heading = wtforms.StringField('Heading')
    post_text = wtforms.StringField('Post text')
    submit = wtforms.SubmitField('Post')

    def create_post_object(self):
        # Retrieve data from form
        topic = self.topic.data
        heading = self.heading.data
        post_text = self.post_text.data

        # Creating a post
        post = models.Post.create_post(topic=topic, heading=heading, post_text=post_text)

        return post

class SignUp(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name: ', validators=[DataRequired()])
    email = wtforms.StringField('E-mail: ', validators=[DataRequired()])
    pwd = wtforms.PasswordField('Password: ', validators=[DataRequired()])
    submit = wtforms.SubmitField('Sign Up')

class SignIn(flask_wtf.FlaskForm):
    email = wtforms.StringField('E-mail: ', validators=[DataRequired()])
    pwd = wtforms.PasswordField('Password', validators=[DataRequired()])