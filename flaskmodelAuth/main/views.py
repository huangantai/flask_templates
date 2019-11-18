from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    return "index"
@main_bp.route('/explore')
def explore():
    return "explore"
@main_bp.route('/search')
def search():
    return "search"

