import os
import csv
import datetime
from typing import Callable
import requests


# 気象情報取得
def get_meteorological(now_raw: datetime.datetime) -> tuple[float, float, int]:
    now_meteorological = now_raw.strftime('%Y%m%d%H')
    url = "https://www.jma.go.jp/bosai/amedas/data/map/" + now_meteorological + "0000.json"
    header = {"content-type": "application/json"}
    response = requests.get(url, headers=header)
    data = response.json()

    temp = data["50331"]["temp"]  # 気温（静岡）
    pres = data["50331"]["pressure"]  # 気圧（静岡）
    hum = data["50331"]["humidity"]  # 湿度（静岡）

    return temp[0], pres[0], hum[0]


# メンタルデータを書き込む
def data_input() -> tuple[str, str, str]:
    def _input_validated(ask_msg: str, err_msg: str, valid_func: Callable[[str], bool]):
        while not valid_func(input_msg := input(ask_msg)):
            print(err_msg)
        return input_msg

    input_body = _input_validated(
        ask_msg="今のカラダの調子を数値化（1～5）してください：",
        err_msg="エラーだよ！もう一度カラダの調子を入力してね",
        valid_func=lambda s: s in list("12345"),
    )

    input_mental = _input_validated(
        ask_msg="今のココロの調子を数値化（1～5）してください：",
        err_msg="エラーだよ！もう一度ココロの調子を入力してね",
        valid_func=lambda s: s in list("12345"),
    )

    input_comment = input("今の気分・コメントを書いてください：")
    return input_body, input_mental, input_comment


# CSV書き込み
def write_csv(out_body: str, out_mental: str, out_comment: str, dst_path: str):
    now = datetime.datetime.now()
    temperature, pressure, humidity = get_meteorological(now)
    now_format = now.strftime("%Y-%m-%d %H:%M")

    with open(dst_path, mode="a", encoding='utf8', newline='') as f:
        csvwriter = csv.writer(f)
        if os.stat(dst_path).st_size == 0:
            columns = ["date","temperature","pressure","humidity","body","mental","comment"]
            csvwriter.writerow(columns)
        new_data = [[now_format, temperature, pressure, humidity, out_body, out_mental, out_comment]]
        csvwriter.writerows(new_data)


def main():
    # ファイルパス
    root_dir = "I:\\09_ジャンクボックス\\094_ナレッジ・体調ログ\\体調ログ"
    month_date = datetime.datetime.today()  # datetime.date.today() でも可
    month_file = f"{month_date:%Y-%m}.csv"
    full_path = os.path.join(root_dir, month_file)

    # 実行
    body, mental, comment = data_input()
    write_csv(body, mental, comment, full_path)


if __name__ == '__main__':
    main()
