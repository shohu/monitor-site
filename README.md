Installation
=====

```
git clone https://github.com/shohu/monitor-site.git
pip install -r requirements.txt
export CHECK_URL=http://examile.com/
export CHANNEL_ID=XXXXXXXX  # for slack channel id
export AUTH_USER_ID=hoge  # Basic auth
export AUTH_USER_PASS=fuga  # Basic auth
export SLACK_POST_URL=https://hooks.slack.com/services/XXXXX
export SLACK_API_TOKEN=xoxp-XXXXXx
```

Launch

```
python ./lambda_function.py
```

Set up AWS Lambda
=====

```
zip -r monitor.zip ./*
```

upload monitor.zip to AWS Lambda
Set up following Environment variable at AWS Lambda

```
export CHECK_URL=http://examile.com/
export CHANNEL_ID=XXXXXXXX  # for slack channel id
export AUTH_USER_ID=hoge  # Basic auth
export AUTH_USER_PASS=fuga  # Basic auth
export SLACK_POST_URL=https://hooks.slack.com/services/XXXXX
export SLACK_API_TOKEN=xoxp-XXXXXx
```