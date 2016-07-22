This python script is not coded by me, I couldn't find the original one, so I'm not able to give credits to person who code this.

**In this version, if you write "donotpull" to commit message, auto deploy will not fetch the source.**


## INSTALLATION

Open GitAutoDeploy.conf.json and fill all the necessary fields.


key | value
--- | ---
[LOCAL_IP] | 199.199.199.199 (Your server ip address)
[LOCAL_PORT_TO_LISTEN] | 3434 (You will write ip and port address to Webhook in Gitlab etc.)
[GIT_REPO_URL] | http://blabla.com/bla.git
[BRANCH_NAME_TO_PULL] | Like: "development" , "master"
[PROJECT_FOLDER] | "/var/www/html/bla.com/"
[AFTER_COMMANDS] | Like: "cd /var/www/html/bla.com/ && ./vendor/bin/db_migrate migrate"

## START IT

In daemon mode:

```
/usr/bin/python /blabla/GitAutoDeploy.py --config /blabla/GitAutoDeploy.conf.json --daemon-mode --quiet
```

In foreground: (to see logs)

```
/usr/bin/python /blabla/GitAutoDeploy.py --config /blabla/GitAutoDeploy.conf.json
```


## ADD TO STARTUP

```
crontab -e
```

Write this:

```
@reboot /usr/bin/python /blabla/GitAutoDeploy.py --config /blabla/GitAutoDeploy.conf.json --daemon-mode --quiet
```


## ADD WEBHOOK IN GITLAB PROJECT SETTING'S AREA


![alt text](http://i.imgur.com/bfDf72C.png "Webhook in GitLab")


curl -A git-oschina-hook -H "Expect:"-H "X-Git-Oschina-Event: Push Hook" -d "hook=%7B%22password%22%3A%22%22%2C%22hook_name%22%3A%22push_hooks%22%2C%22push_data%22%3A%7B%22before%22%3A%220000000000000000000000000000000000000000%22%2C%22after%22%3A%22ec7159240a346fa5988913aa3057b902a4acb126%22%2C%22ref%22%3A%22refs%2Fheads%2Fmaster%22%2C%22user_id%22%3A811894%2C%22user_name%22%3A%22rootky%22%2C%22user%22%3A%7B%22id%22%3A811894%2C%22email%22%3A%22rootky%40163.com%22%2C%22name%22%3A%22rootky%22%2C%22time%22%3A%222016-07-22T14%3A15%3A10%2B08%3A00%22%7D%2C%22repository%22%3A%7B%22name%22%3A%22yyg%22%2C%22url%22%3A%22https%3A%2F%2Fgit.oschina.net%2Fkeyixinxi%2Fyyg.git%22%2C%22description%22%3A%22%5Cu4e00%5Cu5143%5Cu8d2d%22%2C%22homepage%22%3A%22http%3A%2F%2Fgit.oschina.net%2Fkeyixinxi%2Fyyg%22%7D%2C%22commits%22%3A%5B%7B%22id%22%3A%22ec7159240a346fa5988913aa3057b902a4acb126%22%2C%22message%22%3A%22A%20Test%20For%20WebHooks%22%2C%22timestamp%22%3A%222015-11-06T13%3A21%3A07%2B08%3A00%22%2C%22url%22%3A%22http%3A%2F%2Fgit.oschina.net%2Fkeyixinxi%2Fyyg%2Fcommit%2Fec7159240a346fa5988913aa3057b902a4acb126%22%2C%22author%22%3A%7B%22name%22%3A%22rootky%22%2C%22email%22%3A%22rootky%40163.com%22%2C%22time%22%3A%222015-11-06T13%3A21%3A07%2B08%3A00%22%7D%7D%5D%2C%22total_commits_count%22%3A2%2C%22commits_more_than_ten%22%3Afalse%7D%7D" localhost:8001

{
    "password": "",
    "hook_name": "push_hooks",
    "push_data": {
        "before": "0000000000000000000000000000000000000000",
        "after": "ec7159240a346fa5988913aa3057b902a4acb126",
        "ref": "refs/heads/master",
        "user_id": 811894,
        "user_name": "rootky",
        "user": {
            "id": 811894,
            "email": "rootky@163.com",
            "name": "rootky",
            "time": "2016-07-22T14:15:10+08:00"
        },
        "repository": {
            "name": "yyg",
            "url": "https://git.oschina.net/keyixinxi/yyg.git",
            "description": "一元购",
            "homepage": "http://git.oschina.net/keyixinxi/yyg"
        },
        "commits": [
            {
                "id": "ec7159240a346fa5988913aa3057b902a4acb126",
                "message": "A Test For WebHooks",
                "timestamp": "2015-11-06T13:21:07+08:00",
                "url": "http://git.oschina.net/keyixinxi/yyg/commit/ec7159240a346fa5988913aa3057b902a4acb126",
                "author": {
                    "name": "rootky",
                    "email": "rootky@163.com",
                    "time": "2015-11-06T13:21:07+08:00"
                }
            }
        ],
        "total_commits_count": 2,
        "commits_more_than_ten": false
    }
}