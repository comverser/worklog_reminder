import os
import json
import urllib.request
from datetime import datetime, timezone, timedelta
import holidays

KST = timezone(timedelta(hours=9))
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_holiday_status(date):
    """Check if date is a Korean public holiday."""
    kr_holidays = holidays.KR(years=date.year)
    holiday_name = kr_holidays.get(date)
    if holiday_name:
        return f"Public Holiday ({holiday_name})"
    return "Weekday" if date.weekday() < 5 else "Weekend"


def build_message(now):
    """Build the reminder message."""
    date_str = now.strftime("%Y-%m-%d")
    day_of_week = DAYS_OF_WEEK[now.weekday()]
    holiday_status = get_holiday_status(now.date())
    return f"Reminder: Post your daily worklog\n{date_str} ({day_of_week}) - {holiday_status}"


def send_to_slack(webhook_url, text):
    """Send message to Slack via webhook."""
    data = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)


def main():
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    now = datetime.now(KST)
    message = build_message(now)
    send_to_slack(webhook_url, message)
    print("Slack message sent successfully")


if __name__ == "__main__":
    main()
