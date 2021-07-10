import csv
import os

from TwitterAPI import TwitterAPI


def get_screen_names(f):
    res = []
    reader = csv.DictReader(f)

    for row in reader:
        res.append(row["account"])
    return ",".join(sorted(res))


if __name__ == "__main__":
    env = os.environ

    api = TwitterAPI(
        env["CONSUMER_KEY"],
        env["CONSUMER_SECRET"],
        env["ACCESS_TOKEN_KEY"],
        env["ACCESS_TOKEN_SECRET"],
    )

    with open("news_twitter.csv", "r") as f:
        names = get_screen_names(f)

    names = names.replace("@", "")
    r = api.request("users/lookup", {"screen_name": names})

    ids = []
    for item in r.get_iterator():
        ids.append(item["id_str"])
    print(",".join(ids))
