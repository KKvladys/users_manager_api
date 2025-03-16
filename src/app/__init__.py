from flask import Flask

from src.database.database import db, ma, migrate
from src.app.routes import users_bp
from src.config.settings import settings
from src.config.swagger_config import swagger_bp, SWAGGER_URL


def create_app():
    app = Flask(__name__, static_folder="../../static")
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(users_bp)
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    return app
