import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymemcache.client.base import Client

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy()
db.init_app(app)

from .models import DeviceData

"""
We use memcached to cache the top 10 devices per feature on write.
Dashboard interval is one of ["all_time", "past_minute", "past_hour"]
    Memcached = {
        <feature>_<interval>: {timestamp, minheap}
    }
"""
intervals = ["all_time", "past_minute", "past_hour"]
memcached = Client('localhost')
for feature in DeviceData.features():
    for itv in intervals:
        key = "_".join([feature, itv])
        # initialize if nothing cached
        if memcached.get(key, None) is None:
            ts = datetime.fromtimestamp(0).isoformat()
            memcached.set(
                "_".join([feature, itv]),
                json.dumps({"timestamp": ts, "minmaxes": []})
            )

with app.app_context():
    db.create_all()
    from . import routes
