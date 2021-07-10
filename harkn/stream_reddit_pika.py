import json
import os

import pika
import praw

from harkn import stream_reddit

if __name__ == "__main__":
    env = os.environ

    parameters = pika.ConnectionParameters(host=env["RABBITMQ_HOST"], port=5672)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="reddit", exchange_type="fanout")

    reddit = praw.Reddit(
        client_id=env["REDDIT_CLIENT_ID"],
        client_secret=env["REDDIT_CLIENT_SECRET"],
        user_agent=env["REDDIT_USER_AGENT"],
    )

    subreddit = env["REDDIT_SUBREDDIT"]

    for item in stream_reddit.query_to_msgs(reddit, subreddit):
        msg = json.dumps(item)
        channel.basic_publish(exchange="reddit", routing_key="", body=msg)
