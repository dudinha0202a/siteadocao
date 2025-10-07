from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from ...utils import admin_required
from ...extensions import db
from ...models import Animal

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    animals = Animal.query.filter_by(is_adopted=False)\
                          .order_by(Animal.created_at.desc())\
                          .limit(6).all()
    return render_template("index.html", animals=animals)

@bp.route("/<int:animal_id>/delete", methods=["POST"])
@login_required
def delete(animal_id):
    """Excluir um animal (somente admin)."""
    admin_required()
    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()
    flash("Animal excluído com sucesso!", "success")
    return redirect(url_for("animals.list_animals"))