from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ...extensions import db
from ...utils import admin_required
from ...models import User, Role, AdoptionRequest

bp = Blueprint("admin", __name__, template_folder="../../templates/admin")

@bp.before_request
def _guard():
    admin_required()

@bp.route("/")
@login_required
def dashboard():
    stats = {
        "users": User.query.count(),
        "requests": AdoptionRequest.query.count(),
    }
    recent_requests = AdoptionRequest.query.order_by(AdoptionRequest.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", stats=stats, recent_requests=recent_requests)

@bp.route("/users")
@login_required
def users():
    items = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", items=items)
