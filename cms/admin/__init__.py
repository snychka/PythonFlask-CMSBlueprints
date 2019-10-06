from flask import Blueprint

# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint
# https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints
# admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
