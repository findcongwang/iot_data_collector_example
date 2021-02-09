## IoT Data Collector Example

Small Python IoT sample app that collects simulated IoT device readings and stores into a Postgres database. A cache is available to optimize queries on the top 10 devices with highest feature values (i.e. Temperature, Pressure) over some time (i.e. All-Time, Past-Minute, Past-Hour).

#### Configuration

1. Create database `iot_data_collector` in local Postgres instance.

#### How To Run

```
python simulator/device_simulator.py --num_devices=20
```
1. Run the simulator `test`
2. Run the backend service `test`
3. Run dashboard application `test`

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
- [ ] Setup server Procfile to bring up backend API and Kafka listener

#### Developer's Note =D

Did the project incorrectly on first pass which cached and returned top X __device readings__ as opposed to distinct on devices. Didn't click for me until the Nth I tested the application with 5 simulated devices are saw top 10 device readings being returned from dashboard. Fun stuff.
