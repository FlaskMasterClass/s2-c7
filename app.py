import os
import pathlib
import flask
from flask import Flask
from flask import jsonify
from flask import current_app 
import click


from init import db
from init import ma

from flask.cli import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


from config import ProductionConfig
from config import DevelopmentConfig
from config import TestingConfig


profiles = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'testing': TestingConfig()
}


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        fields = ['name']


def create_app(profile):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(profiles[profile])
    app.config.from_pyfile("config.py", silent=True)


    db.init_app(app)
    ma.init_app(app)

    if profile != "testing":
        app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.shell_context_processor
    def shell():
        return {
            "db": db,
        }


    @app.route('/')
    def home():
        # --- demo purposes --
        try:
            db.create_all()
        except:
            pass 
        return 'Please query /<id> or /all'


    @app.route('/<int:user_id>', methods=['GET'])
    def user_id(user_id):
        user = User.query.get(user_id)
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user))

    @app.route('/all', methods=['GET'])
    def user_all():
        user_schema = UserSchema()
        return jsonify(user_schema.dump(User.query.all(), many=True))

    return app


flask_env = os.environ.get("FLASK_ENV", default="development")
app = create_app(flask_env)

if __name__ == '__main__':   
    app.run(host='0.0.0.0', port=5010, debug=True, ssl_context='adhoc')