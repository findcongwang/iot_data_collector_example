from . import db

class DeviceData(db.Model):
    __tablename__ = "deivcedata"

    # composite primary key with deviceid and timestamp
    deviceId = db.Column(db.String(64), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, primary_key=True, nullable=False)

    status = db.Column(db.String(64), nullable=False)
    pressure = db.Column(db.Float, index=True, nullable=False)
    temperature = db.Column(db.Float, index=True, nullable=False)

    def __repr__(self):
        return "Device<{}>: ({}, {}, {}, {})".format(
            self.deviceId,
            self.timestamp.isoformat(""),
            pressure,
            temperature,
        )
