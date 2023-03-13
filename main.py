import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument("token", help= "GitHub token of the account")
args = parser.parse_args()
TOKEN = args.token
ALL_REQUESTS_LIST = []


def register(*args, **kwargs):

    class Wrapper:

        def __init__(self, func):
           ALL_REQUESTS_LIST.append({'func': func,
                                   'name': kwargs['name'],
                                   'description': kwargs['description']})

    return Wrapper


class ApiTool:
    @staticmethod
    def api_get(url: str, token: str = TOKEN):
        headers = {'Accept': 'application/vnd.github+json'
                'Authorization' f'{token}',
                'X-GitHub-Api-Version': '2022-11-28'}
        response = requests.get(url, headers=headers,  timeout=30)
        response.raise_for_status()
        return json.loads(response.content)


@register(name="get_latest_releases",
          description="What are the latest 3 releases of CTFd?")
def get_latest_releases(num: int = 3):
        """ 3 latests releases """
        return ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/releases")


@register(name="get_forks_num", description="How many forks CTFd repo has?")
def get_forks_num():
    """ How many forks """
    return ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/forks")


@register(name="get_repo_stars_num", description="How many stars CTFd repo has")
def get_repo_stars_num():
    """ How many forks """
    return ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/stargazers")


@register(name="get_repo_contributors_num", description="How many contributors CTFd repo has?")
def get_repo_contributors_num():
    """ How many forks """
    return ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/contributors")


@register(name="get_repo_pulls_num", description="How many pull requests CTFd repo has?")
def get_repo_pulls_num():
    """ How many forks """
    return ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/pulls")


@register(name="get_repo_commits_num", description="How many commits CTFd repo has?")
def get_repo_commits_num():
    """ How many forks """
    return ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/commits")


def main():
    for item in ALL_REQUESTS_LIST:
        num = item['func']()
        print(num)
        print(f"{item['description']} - {len(num)}")


if __name__ == "__main__":
    main()



# Create a descending order list of contributors per amount of commits

# Create a descending order list of contributors per amount of pull requests
