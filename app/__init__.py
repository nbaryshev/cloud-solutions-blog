import flask
import os
import flask_sqlalchemy
import flask_migrate

# basedir = os.path.abspath(os.path.dirname(__file__))

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'sdjhgsjghlakjf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, "app.db")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from app import routes, models