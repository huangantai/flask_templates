from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from utils import rename_image, resize_image, redirect_back, flash_errors
from decorators import confirm_required, permission_required
from flask_login import login_required, current_user
import os
from extensions import db

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
@main_bp.route('/show_notifications')
def show_notifications():
    return "show_notifications"
@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)

@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
@main_bp.route('/upload')
def upload():
    return "upload"