from flask import Blueprint
animals_bp = Blueprint("animals", __name__, url_prefix="/animals")
from . import routes  # noqa