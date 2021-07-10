import json

import pika


def on_message(channel, method, properties, body):
    data = json.loads(body)
    print(json.dumps(data, indent=4, sort_keys=True))
    print()
    print()


if __name__ == "__main__":

    parameters = pika.ConnectionParameters()

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="twitter", exchange_type="fanout")
    channel.exchange_declare(exchange="reddit", exchange_type="fanout")

    queue_result = channel.queue_declare("", exclusive=True, auto_delete=True)
    queue = queue_result.method.queue

    channel.queue_bind(queue, "twitter")
    channel.queue_bind(queue, "reddit")

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)

    channel.start_consuming()
