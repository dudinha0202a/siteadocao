import os
from flask import Flask, render_template
from .extensions import db, login_manager
from .models import User, Role

def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class or "config.DevConfig")

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)

    from .blueprints.main.routes import bp as main_bp
    from .blueprints.auth.routes import bp as auth_bp
    from .blueprints.animals.routes import bp as animals_bp
    from .blueprints.admin.routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(animals_bp, url_prefix="/animals")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()
        ensure_default_roles()

    return app

def ensure_default_roles():
    if not Role.query.filter_by(name="admin").first():
        db.session.add(Role(name="admin"))
    if not Role.query.filter_by(name="user").first():
        db.session.add(Role(name="user"))
    db.session.commit()
