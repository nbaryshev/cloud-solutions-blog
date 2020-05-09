import flask
import os
import flask_sqlalchemy
import flask_migrate
import flask_login
from flask_uploads import configure_uploads, IMAGES, UploadSet

basedir = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'sdjhgsjghlakjf'

if "ON_HEROKU" in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL_LOCAL')

app.config['UPLOADED_IMAGES_DEST'] = os.path.join(basedir, 'static/images')
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

login_mngr = flask_login.LoginManager(app)

from app import routes, models

# sqlite:////Users/nikita/Desktop/DevInst/Heroku/My_blog/app/app.db