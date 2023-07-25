from flask import Blueprint

home = Blueprint('home', __name__)

from kopykraft.home import routes