#!/usr/bin/env python

"""butterfree

Usage:
    butterfree.py configure 
    butterfree.py issue tact

Options:
    -h --help    Show this screen.
    --version    Show version.

"""

import sys
import configparser
import datetime

from docopt import docopt
import github


def get_all_issues(repo):
    paged_open_issues = repo.get_issues()
    paged_closed_issues = repo.get_issues(state='closed')
    issues = []

    pages = 0
    while True:
        iss = paged_open_issues.get_page(pages)
        if iss == []:
            break
        else:
            issues += iss
            pages += 1

    pages = 0
    while True:
        iss = paged_closed_issues.get_page(pages)
        if iss == []:
            break
        else:
            issues += iss
            pages += 1

    return sorted(issues, key=lambda i: i.number)


def get_test_status(issues):
    not_written = []
    not_run = []
    not_resolved = []

    for i in issues:
        name_str = '|'.join([l.name for l in i.labels])
        if config['test-states']['not_run'] in name_str:
            not_run.append(str(i.number))
        elif config['test-states']['not_written'] in name_str:
            not_written.append(str(i.number))
        elif config['test-states']['not_resolved'] in name_str:
            not_resolved.append(str(i.number))

    return ','.join([datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), '|'.join(not_written), '|'.join(not_run), '|'.join(not_resolved)])


if __name__ == '__main__':
    arguments = docopt(__doc__, version="butterfree 1")

    try:
        config = configparser.ConfigParser()
        config.read('butterfree.ini')
    except:
        print("Please create butterfree.ini in the working directory of butterfree")
        sys.exit(1)

    G = github.Github(
        config['credentials']['user'],
        config['credentials']['password'])
    U = G.get_user()
    R = [r for r in U.get_repos() if r.name == 'rorschach'][0]


    if arguments['issue']:
        issues = get_all_issues(R)
        if arguments['tact']:
            print(get_test_status(issues))
    else:
        print(__doc__)
