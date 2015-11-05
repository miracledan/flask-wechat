from flask import Blueprint

main = Blueprint('main', __name__)

from . import error, restful, utils, index