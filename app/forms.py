import flask_wtf
import wtforms
from wtforms.validators import data_required

topics = ['History', 'Building']
choices = [(topic, topic) for topic in topics]

class NewPost(flask_wtf.FlaskForm):
    topic = wtforms.SelectField('Choose the topic', choices=choices, validators=[data_required()])
    heading = wtforms.StringField('Heading')
    post_text = wtforms.StringField('Post text')

    submit = wtforms.SubmitField('Post')