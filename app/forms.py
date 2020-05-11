import flask_wtf
import wtforms
from wtforms.validators import DataRequired
from app import models, images

topics = ['Microsoft Azure', 'AWS']
choices = [(topic, topic) for topic in topics]


class NewPost(flask_wtf.FlaskForm):
    topic = wtforms.SelectField('Choose the topic', choices=choices)
    heading = wtforms.TextAreaField('Heading')
    post_preview = wtforms.TextAreaField('Post preview')
    post_text = wtforms.TextAreaField('Post text')
    image = wtforms.FileField('Post image', [wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Create new post')

    def create_post_object(self):
        # Retrieve data from form
        topic = self.topic.data
        heading = self.heading.data
        post_preview = self.post_preview.data
        post_text = self.post_text.data
        image = images.save(self.image.data)

        # Creating a post
        post = models.Post.create_post(topic=topic, heading=heading, post_preview=post_preview, post_text=post_text,
                                       post_image=image)

        return post


class SignUp(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name: ', validators=[DataRequired()])
    email = wtforms.StringField('E-mail: ', validators=[DataRequired()])
    pwd = wtforms.PasswordField('Password: ', validators=[DataRequired()])
    submit = wtforms.SubmitField('Sign Up')

    def create_user(self):
        """
        Creates new user
        """
        # Retrieve data from form
        name = self.name.data
        email = self.email.data
        pwd = self.pwd.data

        new_user = models.User.create_user(name=name, email=email, pwd=pwd)
        sign_in_new_user_auto = models.User.sign_in(email, pwd, remember=True)

        return new_user


class SignIn(flask_wtf.FlaskForm):
    email = wtforms.StringField('E-mail: ', validators=[DataRequired()])
    pwd = wtforms.PasswordField('Password: ', validators=[DataRequired()])
    remember = wtforms.BooleanField('Remember me ')
    submit = wtforms.SubmitField('Sign In')

    def signin_user(self):
        email = self.email.data
        pwd = self.pwd.data
        remember = self.remember.data

        good = models.User.sign_in(email, pwd, remember)

        return good


class NewComment(flask_wtf.FlaskForm):
    comment = wtforms.TextAreaField('Comment')
    submit = wtforms.SubmitField('Comment')

    def get_comment(self, post_id):
        comment = self.comment.data
        new_comment = models.Comment.create_comment(comment, post_id)

        return new_comment


class UpdatePost(flask_wtf.FlaskForm):

    topic = wtforms.SelectField('Choose the topic', choices=choices)
    heading = wtforms.TextAreaField('Heading')
    post_preview = wtforms.TextAreaField('Post preview')
    post_text = wtforms.TextAreaField('Post text')
    image = wtforms.FileField('Post image', [wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Update post')

    # Pre-filling the form by data from the post
    def retrieve(self, topic, heading, post_preview, post_text, image):
        self.topic.data = topic
        self.heading.data = heading
        self.post_preview.data = post_preview
        self.post_text.data = post_text
        self.image.data = image

    # sending the updated data to the table
    def sending_updated_data(self):
        topic_n = self.topic.data
        heading_n = self.heading.data
        post_preview_n = self.post_preview.data
        post_text_n = self.post_text.data
        post_image_n = images.save(self.image.data)

        upd_data = models.Post.update_post(topic_n=topic_n, heading_n=heading_n, post_preview_n=post_preview_n, post_text_n=post_text_n, post_image_n=post_image_n)

        return upd_data
