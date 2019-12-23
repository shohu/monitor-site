# coding: UTF-8
from datetime import datetime, timedelta, timezone
import os

import requests
from requests.auth import HTTPBasicAuth

import slackweb
from slack import WebClient

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

START_TIME = int(os.getenv("START_TIME", 8))
END_TIME = int(os.getenv("END_TIME", 19))
CHECK_URL = os.getenv("CHECK_URL")
MONITOR_CHANNEL_ID = os.getenv("CHANNEL_ID")
AUTH_ID = os.getenv("AUTH_USER_ID")
AUTH_PASS = os.getenv("AUTH_USER_PASS")

slackmanage = slackweb.Slack(
    url=os.getenv("SLACK_POST_URL"))
slack_token = os.getenv("SLACK_API_TOKEN")
client = WebClient(slack_token)


def post(msg):
    slackmanage.notify(text=msg)


def health_check():
    try:
        r = requests.get(CHECK_URL,
                         auth=HTTPBasicAuth(AUTH_ID, AUTH_PASS))
        return True if r.status_code == 200 else False
    except Exception as e:
        print(e)
        return False


def is_site_check():
    current_datetime = datetime.now(JST)
    current_hour = int(current_datetime.strftime('%H'))
    if current_hour < START_TIME or current_hour >= END_TIME:
        print('[PASS] current_hour < {} or current_hour >= {}. current_hour = {}'.format(
            START_TIME,
            END_TIME,
            current_hour))
        return False

    current_day = int(current_datetime.strftime('%d'))
    messages = client.groups_history(
        channel=MONITOR_CHANNEL_ID, count=10)["messages"]
    for message in messages:
        message_time = datetime.fromtimestamp(float(message["ts"]), JST)
        # 日付が同じで
        message_day = int(message_time.strftime('%d'))
        if current_day != message_day:
            print('[PASS] current_day[{}] != message_day[{}]'.format(
                current_day, message_day))
            continue

        # 1日で19:00前までで
        message_hour = int(message_time.strftime('%H'))
        if message_hour >= END_TIME:
            print('[PASS] current_day[{}] != message_day[{}]'.format(
                current_day, message_day))
            continue

        # [workreport]の文字があればサイトチェック
        if '[workreport]' in message["text"]:
            print('[FOUND] workreport message. datetime = {}'.format(
                message_time.strftime('%Y年%m月%d日 %H:%M:%S')))
            return True
    return False


def lambda_handler(event, context):
    if is_site_check():
        # サイト動いてなければpost
        if not health_check():
            post('[BOT] サイト[{}]が動いてません'.format(CHECK_URL))
        else:
            print('[BOT] サイト[{}]から200ステータスが確認できました'.format(CHECK_URL))


if __name__ == "__main__":
    lambda_handler({}, None)
