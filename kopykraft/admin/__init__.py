from flask import Blueprint

admin = Blueprint('admin', __name__)

from kopykraft.admin import routes