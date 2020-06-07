import requests
import getpass
import click
from tabulate import tabulate


@click.command()
@click.option("-o", "--organization", required=True,
              help="Name of the organization you want to inspect")
@click.option("-u", "--username", required=True,
              help="Username of your gitHub account")
def process(organization, username):
    """ This tool gets gitHub account username,
        Name of gitHub organization,
        and gitHub access token,
        And Prints the names of the repos in the organization
        and the number of branched in each of them.
    """
    git_token = getpass.getpass("Enter gitHub token for organization: ")
    username = username
    org_name = organization

    org_url = ("https://api.github.com/orgs/%s/repos?simple=yes&per_page=100&page=1" % org_name)
    org_data = []

    res = requests.get(org_url, auth=(username, git_token))
    repos = res.json()

    while 'next' in res.links.keys():
        res = requests.get(res.links['next']['url'], auth=(username, git_token))
        repos.extend(res.json())

    for repo in repos:
        repo_name = repo["name"]
        branches_url = repo["branches_url"].split("{/branch}")[0]
        res = requests.get(branches_url, auth=(username, git_token))
        branches = res.json()
        branches_num = len(branches)
        org_data.append([repo_name, branches_num])

    table = tabulate(org_data, headers=["Repo Name", "Number Of Branches"], tablefmt="orgtbl")
    print("\n gitHub organization %s data: \n" % org_name)
    print(table)


if __name__ == "__main__":
    process()
