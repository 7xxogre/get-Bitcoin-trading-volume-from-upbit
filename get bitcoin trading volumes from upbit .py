import requests, json, re, time
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
url = "https://api.upbit.com/v1/candles/minutes/60"                                 # 1시간단위의 candle의 데이터를 주는 url
vmp = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]     # 24시간으로 나눈 2차원 리스트
price = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
volume = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
d = datetime.now()
usersneed = int(input("며칠간의 데이터를 받을지 입력 해주세요.: "))
p = str(d - timedelta(days = usersneed-1)).split()                                  # 오늘부터 며칠간의 데이터를 받을 것인지.
print(p[0],"가 되면 확인이 끝납니다.\n중간에 프로그램이 멈추면 아무키나 눌러주십시오.\n", sep = "")
for i in range(usersneed):
    plus = str(d - timedelta(days = i)).split()
    plus = plus[0]
    print(plus)
    querystring = "market=KRW-BTC&to=" + plus + "+00:00:00&count=24"                # 데이터를 가져올 날
    response = requests.request("GET", url, params = querystring)
    
    dicti = response.text.strip('[]')
    dicti = re.sub("'",'"', dicti)                                  # '를 "로 바꿔줌
    dicti = dicti.split('}')


    for j in range(len(dicti)):                                    # json으로 딕셔너리로 만들어주기위해 ','들 삭제후 '}'붙여줌
        dicti[j] = dicti[j].strip(',')
        dicti[j] += '}'
    if(i%10 == 0):
        time.sleep(1)                                              # 사이트에 너무 많은 요청을 보내지 않도록 늦춰줌 (안그럼 밴당함)
   
   
    for j in range(24):
        try:
            diction = json.loads(dicti[j])                              # 오류가 뜨면 알려줌
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
    vmp[i].sort()                                                        #중간값을 얻기 위해 정렬
    price[i].sort()
    volume[i].sort()
mididx = int(usersneed/2)
vmpm = [[],[]]
volm = [[],[]]
prim = [[],[]]

for i in range(24):
    vmpm[0].append(sum(vmp[i])/usersneed)
    vmpm[1].append(vmp[i][mididx])  
    volm[0].append(sum(volume[i])/usersneed)
    volm[1].append(volume[i][mididx])
    prim[0].append(sum(price[i])/usersneed)
    prim[1].append(price[i][mididx])

hours = [i for i in range(24)]                                          # 그래프의 x좌표를 채워줄 시간을 나타내는 리스트
plt.title("Hourly graph (volume * price)")
plt.plot(hours, vmpm[0])
plt.plot(hours, vmpm[1])
plt.xlabel('hours')
plt.legend(['average', 'mid value'])
print("창을 닫으시면 volume값의 시간당 평균 그래프가 나옵니다.")
plt.show()

plt.title("Hourly graph (volume)")
plt.plot(hours, volm[0])
plt.plot(hours, volm[1])
plt.xlabel('hours')
plt.ylabel('coin')
plt.legend(['average', 'mid value'])
print("창을 닫으시면 price값의 시간당 평균 그래프가 나옵니다.")
plt.show()

plt.title("Hourly graph (price)")
plt.plot(hours, prim[0])
plt.plot(hours, prim[1])
plt.xlabel('hours')
plt.ylabel('hundred million dollar')
plt.legend(['average', 'mid value'])
print('창을 닫으시면 프로그램이 끝납니다.')
plt.show()