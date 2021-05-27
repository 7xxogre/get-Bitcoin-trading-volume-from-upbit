import requests
import json
import re
from tqdm import tqdm
import time
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
# 1시간단위의 candle의 데이터를 주는 url
url = "https://api.upbit.com/v1/candles/minutes/60"
vmp = [[] for _ in range(24)]     # 24시간으로 나눈 2차원 리스트
price = [[] for _ in range(24)]
volume = [[] for _ in range(24)]
d = datetime.now()
usersneed = int(input("How many days of data do you want?: "))
# 오늘부터 며칠간의 데이터를 받을 것인지.
p = str(d - timedelta(days=usersneed-1)).split()
print("Press any key when the program stops loading.\n")
for i in tqdm(range(usersneed)):
    plus = str(d - timedelta(days=i)).split()
    plus = plus[0]
    querystring = "market=KRW-BTC&to=" + plus + \
        "+00:00:00&count=24"                # 데이터를 가져올 날
    response = requests.request("GET", url, params=querystring)

    dicti = response.text.strip('[]')
    # '를 "로 바꿔줌
    dicti = re.sub("'", '"', dicti)
    dicti = dicti.split('}')

    # json으로 딕셔너리로 만들어주기위해 ','들 삭제후 '}'붙여줌
    for j in range(len(dicti)):
        dicti[j] = dicti[j].strip(',')
        dicti[j] += '}'
    if(i % 10 == 0):
        # 사이트에 너무 많은 요청을 보내지 않도록 늦춰줌 (안그럼 밴당함)
        time.sleep(1)

    for j in range(24):
        try:
            # 오류가 뜨면 알려줌
            diction = json.loads(dicti[j])
        except Exception as e:
            print(dicti)
        else:
            accprice = diction['candle_acc_trade_price']
            accvolume = diction['candle_acc_trade_volume']
            temp = accprice*accvolume
            timee = diction['candle_date_time_kst']
            timee = int(timee[-8:-6])

            price[timee].append(int(accprice))
            vmp[timee].append(int(temp))
            volume[timee].append(int(accvolume))

print()
for i in range(24):
    vmp[i].sort()  # 중간값을 얻기 위해 정렬
    price[i].sort()
    volume[i].sort()
mididx = int(usersneed/2)
vmpm = [[], []]
volm = [[], []]
prim = [[], []]

for i in range(24):
    vmpm[0].append(sum(vmp[i])/usersneed)
    vmpm[1].append(vmp[i][mididx])
    volm[0].append(sum(volume[i])/usersneed)
    volm[1].append(volume[i][mididx])
    prim[0].append(sum(price[i])/usersneed)
    prim[1].append(price[i][mididx])

# 그래프의 x좌표를 채워줄 시간을 나타내는 리스트
hours = [i for i in range(24)]
plt.title("Hourly graph (volume * price)")
plt.plot(hours, vmpm[0])
plt.plot(hours, vmpm[1])
plt.xlabel('hours')
plt.legend(['average', 'mid value'])
print("If you close the window, you will get an average graph of the volume value per hour.")
plt.show()

plt.title("Hourly graph (volume)")
plt.plot(hours, volm[0])
plt.plot(hours, volm[1])
plt.xlabel('hours')
plt.ylabel('coin')
plt.legend(['average', 'mid value'])
print("If you close the window, you get average graphs per hour of price values.")
plt.show()

plt.title("Hourly graph (price)")
plt.plot(hours, prim[0])
plt.plot(hours, prim[1])
plt.xlabel('hours')
plt.ylabel('hundred million dollar')
plt.legend(['average', 'mid value'])
print('Close the window and the program is over.')
plt.show()
