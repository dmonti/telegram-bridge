# telegram-bridge

## Configuring and running:

1. Install dependencies:
> $ pip3 install -r requirements.txt

2. Creating your Telegram Application at:
> https://core.telegram.org/api/obtaining_api_id

3. Creating your KVDB bucket
> https://kvdb.io/

4. Find your group IDs (source and target groups)
> https://stackoverflow.com/questions/45414021/get-telegram-channel-group-id

5. Create application.ini on project base path
```
[betty]
source_group_id=
target_group_id=

[kvdb]
bucket_id=

[telegram]
api_id=
api_hash=
session_path=telegram.session
```

6. Execute de application
> $ py ./src/main.py