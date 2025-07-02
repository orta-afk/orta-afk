import os
import requests
from lxml import etree
from datetime import datetime
from dateutil import relativedelta
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "orta-afk"

HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

def get_uptime(birthday):
    today = datetime.today()
    diff = relativedelta.relativedelta(today, birthday)

    parts = []
    if diff.years > 0:
        parts.append(f"{diff.years} year{'s' if diff.years != 1 else ''}")
    if diff.months > 0:
        parts.append(f"{diff.months} month{'s' if diff.months != 1 else ''}")
    return ", ".join(parts)

def get_commit_count():
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          totalCommitContributions
        }
      }
    }
    """
    variables = {"login": "orta-afk"}
    response = requests.post(
        'https://api.github.com/graphql',
        json={"query": query, "variables": variables},
        headers=HEADERS
    )
    return response.json()["data"]["user"]["contributionsCollection"]["totalCommitContributions"]

def get_basic_stats():
    query = """
    query($login: String!) {
      user(login: $login) {
        repositories {
          totalCount
        }
        followers {
          totalCount
        }
        starredRepositories {
          totalCount
        }
      }
    }
    """
    variables = {"login": USERNAME}
    response = requests.post(
        'https://api.github.com/graphql',
        json={"query": query, "variables": variables},
        headers=HEADERS
    )

    result = response.json()

    if "errors" in result:
        raise Exception("GraphQL error: ", result["errors"])
    if "data" not in result or result["data"]["user"] is None:
        raise Exception("User not found. Check your USERNAME and TOKEN.")

    data = result["data"]["user"]
    return {
        "repo_data": data["repositories"]["totalCount"],
        "follower_data": data["followers"]["totalCount"],
        "star_data": data["starredRepositories"]["totalCount"]
    }

def update_svg(filename, stats):
    tree = etree.parse(filename)
    root = tree.getroot()
    for key, val in stats.items():
        el = root.find(f".//*[@id='{key}']")
        if el is not None:
            el.text = f"{val:,}" if isinstance(val, int) else str(val)
    tree.write(filename)

if __name__ == "__main__":
    basic_stats = get_basic_stats()
    commit_data = get_commit_count()
    uptime = get_uptime(datetime(2007, 3, 17)) 

    stats = {
        **basic_stats,
        "commit_data": commit_data,
        "age_data": uptime
    }

    update_svg("profile.svg", stats)
