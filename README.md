## IoT Data Collector Example

Small Python IoT sample app that collects simulated IoT device readings via PubSub (Apache Kafka) and stores into a Postgres database. A cache is available to optimize queries on the top 10 devices with highest feature values (i.e. Temperature, Pressure) over some time (i.e. All-Time, Past-Minute, Past-Hour).

#### Prerequisites
* JRE, ZooKeeper, Kafka, Postgres, Python3

#### Configuration

Create database `iot_data_collector` in local Postgres instance.

#### How To Run

1. Run the simulator `test`
2. Run the backend service `test`
3. Run dashboard application `test`

#### Possible Tech Considerations
* ReactJS frontend web dashboard
* Add a Redis layer for on-write cache
* Dockerize components, as well as Postgres/Kafka containers
* Use Apache Cassandra to store write-optimized sensor data
* Load balance dashboard clients with consistent hashing to Kafka topics
* Multiple workers on the backend per Kafka topic

#### Development Todos
- [ ] Setup Postgres with SQLAlchemy, DeviceData Model
- [ ] Make simulator to produce to Kafka:"livedata" w/ device per thread
- [ ] Make data listener on "livedata" and update database + memcached
- [ ] Make dashboard route to fetch from memcached or fallback to database
- [ ] Setup server Procfile to bring up backend API and Kafka listener
- [ ] Make dashboard client to polling for top 10 devices
