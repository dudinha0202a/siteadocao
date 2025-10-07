from flask import Blueprint, render_template
from ...models import Animal, Campaign, Event

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    animals = Animal.query.filter_by(is_adopted=False).order_by(Animal.created_at.desc()).limit(6).all()
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).limit(3).all()
    events = Event.query.order_by(Event.date.desc()).limit(3).all()
    return render_template("index.html", animals=animals, campaigns=campaigns, events=events)
