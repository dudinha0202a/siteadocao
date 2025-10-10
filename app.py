from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from config import DevConfig
from extensions import db, login_manager
from models import User, Role, Animal, AdoptionRequest
from utils import admin_required

def create_app(config_class=DevConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        animals = Animal.query.filter_by(is_adopted=False).order_by(Animal.created_at.desc()).all()
        return render_template('index.html', animals=animals)

    @app.route('/animals')
    def animals_list():
        animals = Animal.query.order_by(Animal.created_at.desc()).all()
        return render_template('animals/list.html', animals=animals)

    @app.route('/animals/<int:animal_id>')
    def animal_detail(animal_id):
        animal = Animal.query.get_or_404(animal_id)
        return render_template('animals/detail.html', animal=animal)

    @app.route('/animals/new', methods=['GET','POST'])
    @login_required
    def animal_new():
        admin_required()
        if request.method == 'POST':
            name = request.form.get('name') or 'Sem nome'
            species = request.form.get('species') or 'Cão'
            age = request.form.get('age') or ''
            description = request.form.get('description') or ''
            photo_url = request.form.get('photo_url') or ''
            animal = Animal(name=name, species=species, age=age, description=description, photo_url=photo_url, created_at=datetime.utcnow())
            db.session.add(animal)
            db.session.commit()
            flash('Animal cadastrado com sucesso!', 'success')
            return redirect(url_for('animals_list'))
        return render_template('animals/form.html')

    @app.route('/adopt/<int:animal_id>', methods=['POST'])
    def adopt_request(animal_id):
        animal = Animal.query.get_or_404(animal_id)
        requester_name = request.form.get('name')
        requester_contact = request.form.get('contact')
        if not requester_name or not requester_contact:
            flash('Preencha nome e contato.', 'warning')
            return redirect(url_for('animal_detail', animal_id=animal.id))
        req = AdoptionRequest(animal_id=animal.id, requester_name=requester_name, requester_contact=requester_contact, created_at=datetime.utcnow())
        db.session.add(req)
        db.session.commit()
        flash('Pedido de adoção enviado!', 'success')
        return render_template('animals/adopt_request_success.html', animal=animal)

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Bem-vindo(a)!', 'success')
                return redirect(url_for('dashboard'))
            flash('Credenciais inválidas.', 'danger')
        return render_template('auth/login.html')

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            if User.query.filter_by(email=email).first():
                flash('E-mail já cadastrado.', 'warning')
                return redirect(url_for('register'))
            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)

            role = Role.query.filter_by(name='user').first()
            if not role:
                role = Role(name='user')
                db.session.add(role)
                db.session.flush()
            user.roles.append(role)
            db.session.commit()
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login'))
        return render_template('auth/register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sessão encerrada.', 'info')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def dashboard():
        admin_required()
        stats = {
            "users": User.query.count(),
            "requests": AdoptionRequest.query.count(),
            "animals": Animal.query.count(),
        }
        recent_requests = AdoptionRequest.query.order_by(AdoptionRequest.created_at.desc()).limit(10).all()
        return render_template('admin/dashboard.html', stats=stats, recent_requests=recent_requests)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
