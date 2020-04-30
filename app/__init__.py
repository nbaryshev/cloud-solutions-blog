import flask
import os
import flask_sqlalchemy
import flask_migrate
import flask_login
from flask_uploads import configure_uploads, IMAGES, UploadSet

basedir = os.path.abspath(os.path.dirname(__file__))

# if "ONHEROKU" in os.environ:
#     on_heroku = True
#
# else:
#     on_heroku = False

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'sdjhgsjghlakjf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, "app.db")

app.config['UPLOADED_IMAGES_DEST'] = os.path.join(basedir, 'static/images')
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# if on_heroku:
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/myblog'


db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

login_mngr = flask_login.LoginManager(app)

from app import routes, models