from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ...extensions import db
from ...models import User, Role

bp = Blueprint("auth", __name__, template_folder="../../templates/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Bem-vindo de volta!", "success")
            return redirect(url_for("main.index"))
        flash("Credenciais inválidas.", "danger")
    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "warning")
            return redirect(url_for("auth.register"))

        user = User(full_name=full_name, email=email)
        user.set_password(password)
        user_role = Role.query.filter_by(name="user").first()
        user.roles.append(user_role)
        db.session.add(user)
        db.session.commit()
        flash("Cadastro realizado! Faça o login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Até logo!", "info")
    return redirect(url_for("main.index"))
