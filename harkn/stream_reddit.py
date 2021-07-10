import datetime
import os

import praw


def on_comment(comment):
    if comment is None:
        return {
            "type": "reddit-comment-keepalive",
            "stamp": datetime.datetime.utcnow().isoformat(),
        }
    else:
        return {
            "type": "reddit-comment",
            "stamp": datetime.datetime.utcnow().isoformat(),
            "data": {
                "id": comment.id,
                "parent_id": comment.parent_id,
                "link_id": comment.link_id,
                "subreddit_id": comment.subreddit_id,
                "created_utc": comment.created_utc,
                "author": comment.author.name,
                "body": comment.body,
            },
        }


def on_submission(submission):
    if submission is None:
        return {
            "type": "reddit-submission-keepalive",
            "stamp": datetime.datetime.utcnow().isoformat(),
        }
    else:
        return {
            "type": "reddit-submission",
            "stamp": datetime.datetime.utcnow().isoformat(),
            "data": {
                "id": submission.id,
                "subreddit_id": submission.subreddit_id,
                "created_utc": submission.created_utc,
                "author": submission.author.name,
                "title": submission.title,
                "url": submission.url,
                "selftext": submission.selftext,
            },
        }


def query_to_msgs(reddit, subreddit):
    comment_stream = reddit.subreddit(subreddit).stream.comments(pause_after=-1)
    submission_stream = reddit.subreddit(subreddit).stream.submissions(pause_after=-1)

    streams = [comment_stream, submission_stream]
    callbacks = [on_comment, on_submission]

    yield {
        "type": "reddit-start",
        "stamp": datetime.datetime.utcnow().isoformat(),
        "subreddit": subreddit,
    }

    while True:
        for stream, callback in zip(streams, callbacks):
            for item in stream:
                yield callback(item)
                if item is None:
                    break


if __name__ == "__main__":
    env = os.environ

    reddit = praw.Reddit(
        client_id=env["REDDIT_CLIENT_ID"],
        client_secret=env["REDDIT_CLIENT_SECRET"],
        user_agent=env["REDDIT_USER_AGENT"],
    )

    subreddit = env["REDDIT_SUBREDDIT"]

    for message in query_to_msgs(reddit, subreddit):
        print(message)
