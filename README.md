# PKV_Event_Bot

Im Moment bauen einige Funktionen (Forum-Fetch, Vote-Reminder, Post Votes to Forum) auf einem cronjob auf. 
Manches davon könnte man wahrscheinlich mit einem Webhook optimieren.

Für den python-telegram bot: 

    pip install python-telegram-bot --upgrade
    
Momentaner crontab:

    * * * * * python /[PATH]/fetch.py >> pkv.log 2>&1
    0 12 * * 2 python /[PATH]/vote_remind.py >> pkv.log 2>&1
    0 14 * * 2 python /[PATH]/post.py >> pkv.log 2>&1
    0 9 * * 0 python /[PATH]/vote_remind.py >> pkv.log 2>&1
    0 11 * * 0 python /[PATH]/post.py >> pkv.log 2>&1
