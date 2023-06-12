from flask import Blueprint
ipscan_bp = Blueprint('ipscan_bp',__name__)
from app.ipscan import routes
