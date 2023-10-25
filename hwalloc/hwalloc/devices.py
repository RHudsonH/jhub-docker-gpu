from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from hwalloc.db import get_db
from hwalloc.model import get_device, get_device_list, release_device

bp = Blueprint('devices', __name__)

@bp.route('/')
def index():
    devices = get_device_list()
    return render_template('devices/index.html', devices=devices, oversubscribe=current_app.config['DEVICE_OVERSUBSCRIBE'])

@bp.route('/<uuid>/release', methods=('POST',))
def release(uuid):
    release_device(uuid)
    return redirect(url_for('devices.index'))

# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post

# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('devices.index'))
        
#     return render_template('devices/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST',))
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('devices.index'))