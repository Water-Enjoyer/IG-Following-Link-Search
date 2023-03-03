# IG-Following-Link-Search
Python script that searches for links among Instagram accounts.

Uses [instagrapi](https://github.com/adw0rd/instagrapi) to search a given list of accounts for the accounts they follow, and then searches those accounts for bio links.

`pip install instagrapi`

Plug in your instagram sessionid

`SESSIONID = " sessionid here "`

Use with a list of accounts
```
    with open("people_i_follow.json", "r") as f:
        accounts = [p['uid'] for p in json.load(f)]
```

Or with a single
```
    accounts = [cl.user_id_from_username(" username here ")]
```

Includes options to save json files of people followed, and of links detected.
```
    check_followings_for_link(user_id, save_follows=True, save_detections=True)
```

Default directories are
```
    USER_FOLLOWINGS_DIR = os.path.join(os.getcwd(), "user_followings")
    DETECTIONS_DIR = os.path.join(os.getcwd(), "detections")
```
