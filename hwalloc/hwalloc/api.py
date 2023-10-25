from flask import (
    Blueprint, jsonify, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from hwalloc.db import get_db
from hwalloc.model import (
    get_device_list, create_device, get_device, allocate_device, release_device
)

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/devices')
def list_devices():
    devices = get_device_list()
    return jsonify(devices), 200

@bp.route('/devices/batch-create', methods=('POST', ))
def batch_create():
    devices = request.json['devices']
    if request.json['devices'] is not None:
        db = get_db()
        for device in devices:
            create_device(device, db)
        db.commit()
    
    devices = get_device_list()
    return jsonify(devices), 200

@bp.route('devices/request_next')
def request_next():
    device, error = allocate_device()
    if error is not None:
        return jsonify({"error": error}), 400

    return jsonify(device), 200

@bp.route('/device/<uuid>')
def device_detail(uuid):
    device, error = get_device(uuid)
    if error is not None or device is None:
        return jsonify({"error": error}), 404
   
    return jsonify(device), 200

@bp.route('/device/<uuid>/request')
def allocate_by_uuid(uuid):
    device, error =  allocate_device(uuid)
    if error is not None:
        return jsonify({"error": error}), 400
    else:
        return jsonify(device), 200

@bp.route('device/<uuid>/release')
def release_by_uuid(uuid):
    """Release a device allocation"""
    device, error = release_device(uuid)
    if error is not None:
        return jsonify({"error": error}), 400
    else:  
        return jsonify(device), 200