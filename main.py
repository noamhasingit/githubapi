import argparse
import requests
import json
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("token", help="GitHub token of the account")
args = parser.parse_args()
TOKEN = args.token

# there is a limitation on number of requests per day/min
PAGINATION_DEMO_FUSE = 2
# list of all prob functions
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
    def get_next_page(page: str):
        return page if page.headers.get('link') is not None else None


    def api_get(url: str, token: str = TOKEN):
        headers = {'Accept': 'application/vnd.github+json',
                   'Authorization': token,
                   'X-GitHub-Api-Version': '2022-11-28',
                   }
        response = requests.get(f'{url}', headers=headers, timeout=30)
        response_all = []
        new_content = json.loads(response.content)
        if type(new_content) is dict:
            response_all.append(json.loads(response.content))
        else:
            response_all.extend(json.loads(response.content))
        limitation_fuse = PAGINATION_DEMO_FUSE
        while ApiTool.get_next_page(response) is not None and limitation_fuse > 0:
            limitation_fuse -= 1
            try:
                next_page_url = response.links['next']['url']
                response = requests.get(next_page_url, timeout=30, headers=headers)
                response.raise_for_status()
                new_content = json.loads(response.content)
                if type(new_content) is dict:
                    response_all.append(json.loads(response.content))
                else:
                    response_all.extend(json.loads(response.content))
            except KeyError:
                break
        return response_all


@register(name="get_latest_releases",
          description="What are the latest 3 releases of CTFd?")
def get_latest_releases(num: int = 3):
        """ 3 latests releases """
        releases = ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/releases")
        published_at_list = [{'date': datetime.fromisoformat(release['published_at']),
                              'id': release['id']} for release in releases]

        published_at_list.sort(key=lambda x : x['date'], reverse=True)
        return [item['id'] for item in published_at_list[:num]]


@register(name="get_forks_num", description="How many forks CTFd repo has?")
def get_forks_num():
    """ How many forks """
    return len(ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/forks"))


@register(name="get_repo_stars_num", description="How many stars CTFd repo has")
def get_repo_stars_num():
    """ How many stars """
    all_repo = ApiTool.api_get("https://api.github.com/search/repositories?q=org:CTFd&sort=stars&order=desc")
    single_repo = [item for item in all_repo[0]['items'] if 'CTFd' in item['name']]
    return single_repo[0]['stargazers_count']


@register(name="get_repo_contributors_num", description="How many contributors CTFd repo has?")
def get_repo_contributors_num():
    """ How many contributors """
    return len(ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/contributors"))


@register(name="get_repo_pulls_num", description="How many pull requests CTFd repo has?")
def get_repo_pulls_num():
    """ How many forks """
    return len(ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/pulls"))


@register(name="get_repo_commits_num", description="How many commits CTFd repo has?")
def get_repo_commits_num():
    """ How many commits """
    return len(ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/commits"))


# TODO
@register(name="get_repo_commits_contributors_num", description="descending order list of contributors per amount of commits")
def get_repo_commits_contributors_num():
    """ descending order list of contributors per amount of commits """
    return len(ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/commits"))


# TODO
@register(name="get_repo_pulls_contributors_num", description="descending order list of contributors per amount of pull requests")
def get_repo_pulls_contributors_num():
    """ How many forks """
    return len(ApiTool.api_get("https://api.github.com/repos/CTFd/CTFd/pulls"))


def main():
    for item in ALL_REQUESTS_LIST:
        result = item['func']()
        print(f"{item['description']} - {result}")


if __name__ == "__main__":
    main()
