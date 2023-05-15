import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel


class TrafficCounter(BaseModel):
    timestamp: datetime
    daily: int
    monthly: int


def get_traffic_counter(
    router_url: str,
    timeout: float,
    timezone: str | ZoneInfo,
) -> TrafficCounter:
    router_home_url = urljoin(router_url, 'cgi-bin/luci/')

    tz = ZoneInfo(key=timezone) if isinstance(timezone, str) else timezone
    now = datetime.now(tz=tz)

    r = requests.get(
        router_home_url,
        timeout=timeout,
    )
    bs = BeautifulSoup(r.text, 'html5lib')

    daily_string = bs.find(id='Traffic_Counter_daily_Lbl').attrs.get('value')
    monthly_string = bs.find(id='Traffic_Counter_monthly_Lbl').attrs.get('value')

    return TrafficCounter(
        timestamp=now,
        daily=int(daily_string),
        monthly=int(monthly_string),
    )
