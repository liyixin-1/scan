from flask import Blueprint
blowup_bp = Blueprint('blowup_bp',__name__)
from app.blowup import routes
