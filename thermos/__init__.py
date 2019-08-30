from flask import Blueprint

thermos = Blueprint('thermos', __name__)

from . import views
