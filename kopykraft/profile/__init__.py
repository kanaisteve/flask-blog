from flask import Blueprint

profile = Blueprint('profile', __name__)

from kopykraft.profile import routes