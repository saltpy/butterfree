#!/usr/bin/env python

import os

from crontab import CronTab


butterfree_home = os.path.dirname(os.path.abspath(__file__))


cron = CronTab(user=True)
cron.remove_all()
issue_tact = cron.new(comment="butterfree issue tact", command=os.path.join(butterfree_home, 'tact.sh ' + butterfree_home))
issue_tact.minute.every(30)
issue_tact.enable()
cron.write_to_user(user=True)
