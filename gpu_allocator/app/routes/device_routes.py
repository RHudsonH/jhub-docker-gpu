from flask import Blueprint, request, jsonify, current_app
from app.models import get_database_instance

# Create a Blueprint for device_routes
device_routes = Blueprint('device_routes', __name__)

def get_db():
    db_type = current_app.get_config_value('DATABASE_TYPE')
    return get_database_instance(db_type)


@device_routes.route('/devices', methods=['GET', 'POST'])
def devices():
    db = get_db()
    if request.method == 'POST':
        devices = request.json['devices']
        db.update_devices(devices)
        return jsonify({"message": "Devices updated successfully"}), 200
    else:
        device_list = db.list_devices()
        return jsonify({"devices": device_list }), 200
    
@device_routes.route('/device/<uuid>', methods=['GET', 'POST', 'DELETE'])
def device(uuid):
    db = get_db()
    if request.method == 'POST':
        device_info = db.allocat_device(uuid)
        if device_info:
            return jsonify(device_info), 200
        else:
            return jsonify({"erro": f"Device {uuid} allocation failed"}), 400
    elif request.method == 'DELETE':
        success = db.release_device(uuid)
        if success:
            return jsonify({"message": f"Device {uuid} released successfully"}), 200
        else:
            return jsonify({"error": f"Device {uuid} failed to release"}), 400
    else:
        device_info = db.get_device(uuid)
        if device_info:
            return jsonify(device_info), 200
        else:
            return jsonify({"error": f"No such device: {uuid}"}), 404
        
@device_routes.route('/device/request_next', methods=['POST'])
def request_next():
    db = get_db()
    device_info = db.allocate_device()
    if device_info:
        return jsonify(device_info), 200
    else:
        return jsonify({"error": "No available devices"}), 400