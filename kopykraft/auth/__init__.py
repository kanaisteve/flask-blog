from flask import Blueprint

auth = Blueprint('auth', __name__)

from kopykraft.auth import routes