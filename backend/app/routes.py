from . import app
from datetime import datetime as dt
from flask import request, jsonify
from .models import db, DeviceData

@app.route('/devicedata', methods=['POST'])
def devicedata():
    data = request.get_json()
    return jsonify(data)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    interval = request.args.get('interval', "all_time")

    device_data = DeviceData.query.filter_by(
        deviceId="test"
    ).limit(5).all()

    return jsonify(device_data)
