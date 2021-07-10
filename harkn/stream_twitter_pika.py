import json
import os

import pika
from TwitterAPI import TwitterAPI

from harkn import stream_twitter

if __name__ == "__main__":
    env = os.environ

    parameters = pika.ConnectionParameters(host=env["RABBITMQ_HOST"], port=5672)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="twitter", exchange_type="fanout")

    track_query_str = env["TRACK_QUERY"]
    track_query = json.loads(track_query_str)

    api = TwitterAPI(
        env["CONSUMER_KEY"],
        env["CONSUMER_SECRET"],
        env["ACCESS_TOKEN_KEY"],
        env["ACCESS_TOKEN_SECRET"],
    )
    stream = stream_twitter.query_to_msgs(api, track_query)

    for item in stream:
        msg = json.dumps(item)
        channel.basic_publish(exchange="twitter", routing_key="", body=msg)
