

from flask import Blueprint
core_blueprint = Blueprint('core', __name__)

@core_blueprint.app_template_filter('replace_under_score')
def replace_under_score(text):
    return text.replace('_', ' ')