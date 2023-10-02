
import datetime
import requests

now_raw = datetime.datetime.now()
now = now_raw.strftime('%Y%m%d%H')
url = "https://www.jma.go.jp/bosai/amedas/data/map/" + now + "0000.json"
header = {"content-type": "application/json"}
response = requests.get(url, headers=header)
data = response.json()

temperature = data["50331"]["temp"]  # 気温
pressure = data["50331"]["pressure"]  # 気圧
humidity = data["50331"]["humidity"]  # 湿度

print(f"静岡市の天候状況\n温度：{temperature[0]}℃\n気圧：{pressure[0]}hPa\n湿度：{humidity[0]}％")