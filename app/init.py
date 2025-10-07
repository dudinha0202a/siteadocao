from flask import Flask, render_template
from .extensions import db, login_manager
from .models import User, Animal
from .auth import auth_bp
from .animals import animals_bp
from .community import community_bp
from .events import events_bp
from .admin import admin_bp
from ..config import Config

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)

    # home
    @app.route("/")
    def index():
        animals = Animal.query.order_by(Animal.created_at.desc()).limit(8).all()
        return render_template("index.html", animals=animals)

    # CLI – criar tabelas e admin
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Banco criado.")

    @app.cli.command("create-admin")
    def create_admin():
        from .models import User
        if User.query.filter_by(email="admin@adocao.org").first():
            print("Admin já existe.")
            return
        u = User(name="Admin", email="admin@adocao.org", is_admin=True)
        u.set_password("admin123")
        db.session.add(u)
        db.session.commit()
        print("Admin criado: admin@adocao.org / admin123")

    return app
