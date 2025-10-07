from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ...extensions import db
from ...models import Animal, AdoptionRequest
from ...utils import admin_required

bp = Blueprint("animals", __name__, template_folder="../../templates/animals")

@bp.route("/")
def list_animals():
    q = request.args.get("q", "").strip()
    species = request.args.get("species", "")
    city = request.args.get("city", "")
    query = Animal.query.filter_by(is_adopted=False)

    if q:
        like = f"%{q}%"
        query = query.filter(Animal.name.ilike(like) | Animal.description.ilike(like) | Animal.breed.ilike(like))
    if species:
        query = query.filter_by(species=species)
    if city:
        query = query.filter(Animal.city.ilike(f"%{city}%"))

    animals = query.order_by(Animal.created_at.desc()).all()
    return render_template("animals/list.html", animals=animals)

@bp.route("/<int:animal_id>")
def detail(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return render_template("animals/detail.html", animal=animal)

@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    admin_required()
    if request.method == "POST":
        data = {k: request.form.get(k) for k in ["name","species","breed","age","sex","size","city","state","description","photo_url"]}
        animal = Animal(**data)
        db.session.add(animal)
        db.session.commit()
        flash("Animal cadastrado!", "success")
        return redirect(url_for("animals.list_animals"))
    return render_template("animals/form.html", mode="new")

@bp.route("/<int:animal_id>/edit", methods=["GET", "POST"])
@login_required
def edit(animal_id):
    admin_required()
    animal = Animal.query.get_or_404(animal_id)
    if request.method == "POST":
        for field in ["name","species","breed","age","sex","size","city","state","description","photo_url","is_adopted"]:
            val = request.form.get(field)
            if field == "is_adopted":
                animal.is_adopted = bool(val)
            elif val is not None:
                setattr(animal, field, val)
        db.session.commit()
        flash("Animal atualizado!", "success")
        return redirect(url_for("animals.detail", animal_id=animal.id))
    return render_template("animals/form.html", mode="edit", animal=animal)

@bp.route("/<int:animal_id>/adopt", methods=["POST"])
def adopt_request(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    req = AdoptionRequest(
        animal_id=animal.id,
        applicant_name=request.form.get("name"),
        applicant_email=request.form.get("email"),
        applicant_phone=request.form.get("phone"),
        message=request.form.get("message")
    )
    db.session.add(req)
    db.session.commit()
    return render_template("animals/adopt_request_success.html", animal=animal)
