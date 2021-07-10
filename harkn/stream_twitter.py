import datetime
import json
import os
import time

from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import TwitterConnectionError


def iterate_msgs(stream):
    """
    Adapted from the twitterapi source; need to emit keepalives to mark periods
    with data
    """
    while True:
        item = None
        buf = bytearray()
        stall_timer = None

        while True:
            # read bytes until item boundary reached
            buf += stream.read(1)
            if not buf:
                # check for stall (i.e. no data for 90 seconds)
                if not stall_timer:
                    stall_timer = time.time()
                elif time.time() - stall_timer > TwitterAPI.STREAMING_TIMEOUT:
                    raise TwitterConnectionError("Twitter stream stalled")
            elif stall_timer:
                stall_timer = None
            if buf[-2:] == b"\r\n":
                item = buf[0:-2]
                if item.isdigit():
                    # use byte size to read next item
                    nbytes = int(item)
                    item = None
                    item = stream.read(nbytes)
                    yield item
                else:
                    yield b""  # keepalive
                break


def query_to_msgs(api, track_query):
    twitter_response = api.request("statuses/filter", track_query)
    response = twitter_response.response
    assert response.status_code == 200
    assert twitter_response.options["is_stream"]
    stream = response.raw

    yield {
        "type": "twitter-start",
        "stamp": datetime.datetime.utcnow().isoformat(),
        "track_query": track_query,
    }

    for a in iterate_msgs(stream):
        if len(a) == 0:
            yield {
                "type": "twitter-keepalive",
                "stamp": datetime.datetime.utcnow().isoformat(),
            }
        else:
            data = json.loads(a.decode("utf8"))
            yield {
                "type": "twitter-message",
                "stamp": datetime.datetime.utcnow().isoformat(),
                "data": data,
            }


if __name__ == "__main__":
    env = os.environ

    track_query_str = env["TRACK_QUERY"]
    track_query = json.loads(track_query_str)

    api = TwitterAPI(
        env["CONSUMER_KEY"],
        env["CONSUMER_SECRET"],
        env["ACCESS_TOKEN_KEY"],
        env["ACCESS_TOKEN_SECRET"],
    )

    for msg in query_to_msgs(api, track_query):
        print(json.dumps(msg, indent=4))
