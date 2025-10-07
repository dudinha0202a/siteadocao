from flask import Blueprint, render_template
from ...models import Animal

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    animals = Animal.query.filter_by(is_adopted=False)\
                          .order_by(Animal.created_at.desc())\
                          .limit(6).all()
    return render_template("index.html", animals=animals)