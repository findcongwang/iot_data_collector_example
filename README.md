## IoT Data Collector Example

Small Python IoT sample app that collects simulated IoT device readings and stores into a Postgres database. A cache is available to optimize queries on the top 10 devices with highest feature values (i.e. Temperature, Pressure) over some time (i.e. All-Time, Past-Minute, Past-Hour).

#### Project Structure
```
│─── .gitignore
│─── device_simulator.py      # IoT device simulator
│─── Pipfile
│─── Pipfile.lock
│─── README.md
└─── backend
    │─── .env                 # Environment variables for configs
    │─── config.py            
    └─── app
        |─── models.py        # Data models for device data
        |─── routes.py        # API endpoints
        └─── __init__.py      # FLASK_APP entry point
```

#### Configuration

```bash
# Config ENV variables in backend/.env
# Create database `iot_data_collector` in local Postgres instance
export SQLALCHEMY_DATABASE_URI="postgresql://<user>:<pw>@localhost:5432/<database>"

# Config the number of top devices returned by dashboard route
export NUM_TOP_DEVICES=10
```

#### How To Run

```bash
# Setup virtual env and install packages
$ pipenv shell
$ pipenv install

# Start backend server
$ cd backend && flask run

# On separate terminal, start device simulator (remember to pipenv shell)
$ python device_simulator.py --num_devices=15

# Open browser or postman and test dashboard API endpoint, e.g.
# http://localhost:5000/dashboard
# http://localhost:5000/dashboard?features=pressure
# http://localhost:5000/dashboard?features=pressure&interval=past_minute

# Test histogram API endpoint
# http://localhost:5000/devices/device_1/histogram
```

#### Extensions and Tech Considerations
* ReactJS frontend web dashboard
* Use Alembic to track database migrations, BRIN on timestamps
* Use Redis for on-write cache, much more flexible
* Dockerize components, as well as Postgres/Kafka/Redis containers
* Use Apache Cassandra to store write-optimized sensor data
* Use Kafka to receive incoming data behind a load balancer
* Load balance dashboard clients with consistent hashing to Kafka topics
* Multiple workers on the backend per Kafka topic
* Use a repository pattern to inverse dependency on ORM (part of DDD)

#### Development Todos
- [x] Setup Postgres with SQLAlchemy, DeviceData Model
- [x] Make simulator to produce to data endpoint w/ device per thread
- [x] Make devicedata endpoint to receive data and update memcached/database
- [x] Make dashboard route to fetch from memcached or fallback to database
- [x] Make status histogram route for a given deviceId

#### Developer's Note =D

Did the project incorrectly on first pass which cached and returned top X __device readings__ as opposed to distinct on devices. Didn't click for me until the Nth I tested the application with 5 simulated devices are saw top 10 device readings being returned from dashboard. Fun stuff.
