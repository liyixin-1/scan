from flask import Blueprint
portscan_bp = Blueprint('portscan_bp',__name__)
from app.portscan import routes
