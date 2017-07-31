#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import sys
import json

import requests
import argparse


login_template = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
get_manifest_template = "https://registry.hub.docker.com/v2/{repository}/manifests/{tag}"


def pretty_print(d):
    print(json.dumps(d, indent=2))


def download_manifest_for_repo(repo, tag, username, password):
    """
    repo: string, repository (e.g. 'library/fedora')
    tag:  string, tag of the repository (e.g. 'latest')
    """
    if not username:
        response = requests.get(login_template.format(repository=repo), json=True)
    else:
        response = requests.get(login_template.format(repository=repo), json=True, auth=(username, password))

    response_json = response.json()
    token = response_json["token"]
    response = requests.get(
        get_manifest_template.format(repository=repo, tag=tag),
        headers={"Authorization": "Bearer {}".format(token)},
        json=True
    )
    manifest = response.json()
    if not response.status_code == requests.codes.ok:
        pretty_print(dict(response.headers))
    return manifest


def main():
    parser = argparse.ArgumentParser(description='Get Docker Repositry Manifest')
    parser.add_argument('repos', metavar='Repos', nargs='+', help='Registery e.g. library/fedora')
    parser.add_argument('--username', '-u', metavar='USERNAME')
    parser.add_argument('--password', '-p', metavar='PASSWORD')

    # repos = sys.argv[1:]
    args = parser.parse_args()
    username = args.username
    password = args.password
    repos = args.repos
    if not repos:
        return 1 # parser will not allow us to get here!
    for repo_tag in repos:
        if ":" in repo_tag:
            repo, tag = repo_tag.split(":")
        else:
            repo, tag = repo_tag, "latest"
        if "/" not in repo:
            repo = "library/" + repo
        pretty_print(download_manifest_for_repo(repo, tag, username, password))
        return 0


if __name__ == "__main__":
    sys.exit(main())

