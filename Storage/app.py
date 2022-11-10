from inspect import trace
from platform import python_branch
import connexion
from connexion import NoContent
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from exercise_data import ExerciseData
from user_parameters import UserParameters
import json
import KafkaClient from pykafka
import OffsetType from pykafka.common
import Thread from threading

from base import Base
import logging
import logging
import logging.config
import datetime

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    DB_USER = app_config['datastore']['user']
    DB_PW = app_config['datastore']['password']
    DB_HNAME = app_config['datastore']['hostname']
    DB_PORT = app_config['datastore']['port']
    DB_NAME = app_config['datastore']['db']

DB_ENGINE = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HNAME}:{DB_PORT}/{DB_NAME}', pool_pre_ping=True)

# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def report_exercise_data(body):
    """ Receives exercise data """
    session = DB_SESSION()
    print(body['user_id'],
                    body['device_name'],
                    body['heart_rate'],
                    body['date_created'],
                    body['recording_id'],
                    body['trace_id'],
                    body['trace_time'])
    ed = ExerciseData(body['user_id'],
                    body['device_name'],
                    body['heart_rate'],
                    body['date_created'],
                    body['recording_id'],
                    body['trace_id'],
                    body['trace_time'])


    session.add(ed)

    session.commit()
    session.close()

    trace_id = body['trace_id']

    logger.debug(f'Stored event exerciseData request with a trace id of { trace_id}')
    

    return NoContent, 201

def get_exercise_data(timestamp):
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    readings = session.query(ExerciseData).filter(ExerciseData.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Exercise Data %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200


def report_user_parameters(body):
    """ Receives a heart rate (pulse) reading """

    session = DB_SESSION()
    up = UserParameters(body['user_id'],
                   body['age'],
                   body['weight'],
                   body['device_name'],
                   body['exercise'],
                   body['reps'],
                   body['met'],
                   body['date_created'],
                   body['recording_id'],
                   body['trace_id'],
                   body['trace_time'])

    session.add(up)

    session.commit()
    session.close()

    trace_id = body['trace_id']

    logger.debug(f'Stored event userParameters request with a trace id of { trace_id}')

    return NoContent, 201

def get_user_parameters(timestamp):
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    readings = session.query(UserParameters).filter(UserParameters.date_created >= timestamp_datetime)
    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for User Parameters %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200



def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                        reset_offset_on_start=False,
                                        auto_offset_reset=OffsetType.LATEST)
    
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        
        payload = msg["payload"]
        
        if msg["type"] == "event1": # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
        elif msg["type"] == "event2": # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
        
        # Commit the new message as being read
        consumer.commit_offsets()
    

# with open('app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
