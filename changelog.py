from datetime import datetime
from github import Github
from pprint import pprint
import os
import re
import requests
import subprocess
import sys

g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo('yourlabs/django-autocomplete-light')
tag = sys.argv[1]


with open('CHANGELOG', 'r') as f:
    CHANGELOG = f.read()

last_release = None
for line in CHANGELOG.split('\n'):
    if match := re.match('^(.+)', line):
        last_release = match.group(0)
        break

git_log = subprocess.check_output(
    f"git log --pretty=format:'%h %D' {last_release}..",
    shell=True,
).decode('utf8').split('\n')

tags = {}
tag_commits = []
for line in git_log:
    parts = line.split()
    if len(parts) == 1:
        tag_commits.append(parts[0])
        continue

    for i, part in enumerate(parts):
        if part == 'tag:':
            tags[tag] = tag_commits
            tag = parts[i + 1].strip(',')
            tag_commits = [parts[0]]

# add remaining commits to last seen tag
tags[tag] = tag_commits

lines = []
for tag, shas in tags.items():
    lines.append(tag)
    lines.append('')

    for sha in shas:
        line = []
        author, description = subprocess.check_output(
            f"git log --format='%an--sep--%B' -n1 {sha}",
            shell=True,
        ).decode('utf8').split('\n')[0].split('--sep--')
        if description.startswith('Release '):
            date = subprocess.check_output(
                f"git log --format='%as' -n1 {sha}",
                shell=True,
            ).decode('utf8').strip()
            lines.append(f'    {date} {description}')
            continue
        try:
            commit = repo.get_commit(sha)
            pulls = [*commit.get_pulls()]
        except:  # commit not found
            lines.append(f'    {sha} {description} by {author}')
            continue
        numbers = []
        users = []
        for pull in pulls:
            numbers.append(pull.number)
            users.append(pull.user.login)
        for number in numbers:
            line.append(f'#{number}'.ljust(7))
        if not numbers:
            line.append(sha)

        line.append(description)
        line.append('by')
        for user in users:
            line.append(f'@{user}')
        if not users:
            line.append(author)
        lines.append('    ' + ' '.join(line))

    lines.append('')


print('\n'.join(lines))
