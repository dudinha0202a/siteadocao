from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ...extensions import db
from ...utils import admin_required
from ...models import User, Role, Campaign, Event, AdoptionRequest

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
        "campaigns": Campaign.query.count(),
        "events": Event.query.count()
    }
    recent_requests = AdoptionRequest.query.order_by(AdoptionRequest.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", stats=stats, recent_requests=recent_requests)

@bp.route("/users")
@login_required
def users():
    items = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", items=items)

@bp.route("/campaigns", methods=["GET", "POST"])
@login_required
def campaigns():
    if request.method == "POST":
        c = Campaign(
            title=request.form.get("title"),
            description=request.form.get("description"),
            link=request.form.get("link"),
            start_date=_parse_date(request.form.get("start_date")),
            end_date=_parse_date(request.form.get("end_date")),
        )
        db.session.add(c)
        db.session.commit()
        flash("Campanha cadastrada!", "success")
        return redirect(url_for("admin.campaigns"))
    items = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template("admin/campaigns.html", items=items)

@bp.route("/events", methods=["GET", "POST"])
@login_required
def events():
    if request.method == "POST":
        e = Event(
            title=request.form.get("title"),
            description=request.form.get("description"),
            location=request.form.get("location"),
            date=_parse_date(request.form.get("date")),
        )
        db.session.add(e)
        db.session.commit()
        flash("Evento cadastrado!", "success")
        return redirect(url_for("admin.events"))
    items = Event.query.order_by(Event.date.desc()).all()
    return render_template("admin/events.html", items=items)

def _parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date() if s else None
    except Exception:
        return None
