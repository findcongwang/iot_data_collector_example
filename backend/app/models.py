import enum
from . import db

class DeviceStatus(enum.Enum):
    ON = "ON"
    OFF = "OFF"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class DeviceData(db.Model):
    __tablename__ = "deivcedata"

    # composite primary key with deviceid and timestamp
    deviceId = db.Column(db.String(64), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, primary_key=True, nullable=False)

    status = db.Column(db.Enum(DeviceStatus), nullable=False)
    pressure = db.Column(db.Float, index=True, nullable=False)
    temperature = db.Column(db.Float, index=True, nullable=False)

    def to_dict(self):
        return {
            "deviceId": self.deviceId,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "pressure": self.pressure,
            "temperature": self.temperature,
        }

    @classmethod
    def features(cls):
        return ["pressure", "temperature"]
