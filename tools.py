from datetime import datetime, timedelta
import pytz


def get_yesterday():
    kst = pytz.timezone("Asia/Seoul")
    now = datetime.now(pytz.utc).astimezone(kst)
    yesterday = now - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    return yesterday_str
