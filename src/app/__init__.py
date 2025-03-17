from flask import Flask

from src.database.database import db, ma, migrate
from src.app.routes import users_bp
from src.config.settings import Settings
from src.config.swagger_config import swagger_bp, SWAGGER_URL


def create_app(setting_config: type[Settings] = Settings) -> Flask:
    app = Flask(__name__, static_folder="../../static")
    app.config["DEBUG"] = True
    app.config.from_object(setting_config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    return app
