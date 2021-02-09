import bisect
import json
from . import app
from . import intervals, memcached
from .models import db, DeviceData
from datetime import datetime as dt
from datetime import timedelta
from flask import request, jsonify
from os import environ
from sqlalchemy import func, tuple_


@app.route('/devicedata', methods=['POST'])
def devicedata():
    """
    Endpoint to receive new device datapoint, updates top devices cache.
    """
    data = request.get_json()

    dd = DeviceData(**data)
    db.session.add(dd)
    db.session.commit()

    # update cache when write is confirmed, updates corresponding maxheaps
    num_top_devices = int(environ.get('NUM_TOP_DEVICES'))
    for feature in DeviceData.features():
        # negate feature value to keep list reversed for efficient .pop()
        device_item = [-getattr(dd, feature), dd.deviceId, dd.to_dict()]
        for itv in intervals:
            key = "_".join([feature, itv])
            cache = json.loads(memcached.get(key))

            # if device already in cache, replace val if larger (pop & insort)
            try:
                idx = [dd_dict["deviceId"]
                    for _, _, dd_dict in cache["minmaxes"]].index(dd.deviceId)
                if device_item > cache["minmaxes"][idx]:
                    cache["minmaxes"].pop(idx)
                    bisect.insort(cache["minmaxes"], device_item)

            # otherwise, insort new item if len(cache) < NUM_TOP_DEVICES
            # OR if device_item > minmaxes[0]. -> insort and pop last
            except ValueError:
                if len(cache["minmaxes"]) < num_top_devices:
                    bisect.insort(cache["minmaxes"], device_item)
                    cache["timestamp"] = dd.timestamp.isoformat()
                    memcached.set(key, json.dumps(cache))
                elif device_item > cache["minmaxes"][0]:
                    bisect.insort(cache["minmaxes"], device_item)
                    cache["minmaxes"].pop()
                    cache["timestamp"] = dd.timestamp.isoformat()
                    memcached.set(key, json.dumps(cache))

    return jsonify(dd.to_dict())


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Retrieve top devices per feature over interval
    Params:
        features: list of features, default: all
        interval: query interval, default: all_time

    Returns from cache on-hit, based on:
        - interval is all_time or cache[timestamp] < cutoff_time
    On miss, queries from database, update cache
    """
    features = request.args.get('features', None)
    interval = request.args.get('interval', "all_time")
    features = DeviceData.features() if features is None else features.split(",")

    if interval == "past_minute":
        cutoff_time = dt.now() - timedelta(minutes=1)
    elif interval == "past_hour":
        cutoff_time = dt.now() - timedelta(minutes=60)
    else:
        cutoff_time = None

    response = {}
    for feature in features:
        key = "_".join([feature, interval])
        cache = json.loads(memcached.get(key))

        # cache hit based on timestamp of oldest record
        cache_timestamp = dt.fromisoformat(cache["timestamp"])
        if cutoff_time and cache_timestamp >= cutoff_time:
            top_readings = [dd_dict for _, _, dd_dict in cache["minmaxes"]]

        # cache miss, query and update memcached
        else:
            num_top_devices = int(environ.get('NUM_TOP_DEVICES'))
            # get the records by max feature value, distinct on deviceId
            # max value over all time
            if cutoff_time is None:
                tr_query = db.session.query(
                    DeviceData.deviceId,
                    func.max(getattr(DeviceData, feature))
                ).group_by(DeviceData.deviceId)
            else:
                tr_query = db.session.query(
                    DeviceData.deviceId,
                    func.max(getattr(DeviceData, feature))
                ).group_by(
                    DeviceData.deviceId
                ).filter(DeviceData.timestamp >= cutoff_time)

            # get the full records to return
            top_records = tr_query.limit(num_top_devices).all()
            device_data = DeviceData.query.filter(
                tuple_(DeviceData.deviceId, getattr(DeviceData, feature)).in_(top_records)
            )
            top_readings = sorted(
                [dd.to_dict() for dd in device_data],
                reverse=True,
                key=(lambda x: x[feature])
            )
            # update memcached values with db query results
            timestamp, array = dt.now().isoformat(), []
            if len(top_readings) > 0:
                timestamp = min(x["timestamp"] for x in top_readings)
                array = [
                    [-dd_dict[feature], dd_dict["deviceId"], dd_dict]
                    for dd_dict in top_readings]
            memcached.set(
                key,
                json.dumps({"timestamp": timestamp, "minmaxes": array})
            )
        response[feature] = top_readings

    return jsonify(response)
