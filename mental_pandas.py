import pandas
import matplotlib.pyplot as plt

csv_data = pandas.read_csv("I:\\09_ジャンクボックス\\094_ナレッジ・体調ログ\\体調ログ\\2023-09.csv", encoding="utf-8")

ax = csv_data.plot(y="mental")
csv_data.plot(figsize=(16, 9), x="date", y="body",ax=ax)
# plt.show()
plt.savefig('I:\\09_ジャンクボックス\\094_ナレッジ・体調ログ\\体調ログ\\data.png')
plt.close('all')
