from flask import Blueprint

posts = Blueprint('posts', __name__)

from kopykraft.posts import routes