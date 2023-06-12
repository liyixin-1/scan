from flask import Blueprint
attack_bp = Blueprint('attack_bp',__name__)
from app.attack import routes
